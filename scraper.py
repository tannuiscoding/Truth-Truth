import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
from config import (
    REQUEST_TIMEOUT, 
    MAX_QUESTIONS_PER_SOURCE, 
    CACHE_DURATION_HOURS,
    USER_AGENT,
    QUESTION_SOURCES,
    ALTERNATIVE_SOURCES,
    FILTER_WORDS
)

class QuestionScraper:
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_duration = timedelta(hours=CACHE_DURATION_HOURS)
        self.fallback_questions = self._load_fallback_questions()
    
    def _load_fallback_questions(self):
        """Load fallback questions in case web scraping fails"""
        return {
            'truth': [
                "What's the most embarrassing thing that happened to you in school?",
                "What's your biggest fear?",
                "What's the worst lie you've ever told?",
                "What's your most embarrassing childhood memory?",
                "What's the most trouble you've ever been in?",
                "What's your biggest regret?",
                "What's the most embarrassing thing in your search history?",
                "What's your biggest insecurity?",
                "What's the most embarrassing thing you've done while drunk?",
                "What's your biggest pet peeve?",
                "What's the most embarrassing thing you've ever said to someone?",
                "What's your most embarrassing nickname?",
                "What's the most embarrassing thing you've ever worn?",
                "What's your most embarrassing moment in public?",
                "What's the most embarrassing thing you've ever done for money?"
            ],
            'dare': [
                "Let someone in the group post something on your social media",
                "Call your mom and tell her you're getting married",
                "Let the group go through your phone for 2 minutes",
                "Do your best impression of someone in the group",
                "Let someone in the group text anyone in your contacts",
                "Dance for 30 seconds without music",
                "Let the group pick your profile picture for the next week",
                "Call a friend and sing them a song",
                "Let someone in the group look through your photos for 1 minute",
                "Do 10 push-ups right now",
                "Let the group choose your outfit for tomorrow",
                "Call a random number and try to sell them something",
                "Let someone in the group control your phone for 5 minutes",
                "Do your best animal impression",
                "Let the group pick your next status update"
            ],
            'would_you_rather': [
                "Would you rather be invisible or be able to fly?",
                "Would you rather be rich and ugly or poor and beautiful?",
                "Would you rather have unlimited money or unlimited knowledge?",
                "Would you rather live in the past or the future?",
                "Would you rather be famous or be a genius?",
                "Would you rather have no internet or no phone?",
                "Would you rather be too hot or too cold?",
                "Would you rather be a superhero or a villain?",
                "Would you rather be able to read minds or see the future?",
                "Would you rather be poor and happy or rich and miserable?",
                "Would you rather be able to speak all languages or play all instruments?",
                "Would you rather be able to teleport or time travel?",
                "Would you rather be a famous actor or a famous musician?",
                "Would you rather be able to control fire or water?",
                "Would you rather be able to talk to animals or speak all human languages?"
            ]
        }
    
    async def get_session(self):
        """Get or create an aiohttp session"""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def _is_valid_question(self, text):
        """Check if a scraped text is a valid question"""
        if not text or len(text) < 10 or len(text) > 500:
            return False
        
        # Check if it contains filter words
        text_lower = text.lower()
        if any(word in text_lower for word in FILTER_WORDS):
            return False
        
        # Check if it looks like a question (contains question words or ends with ?)
        question_indicators = ['what', 'when', 'where', 'who', 'why', 'how', 'would you', 'have you', 'do you', 'are you']
        has_question_indicator = any(indicator in text_lower for indicator in question_indicators)
        ends_with_question = text.strip().endswith('?')
        
        return has_question_indicator or ends_with_question
    
    async def scrape_questions(self, url):
        """Scrape questions from a given URL"""
        try:
            session = await self.get_session()
            headers = {'User-Agent': USER_AGENT}
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    questions = []
                    
                    # Try different selectors for finding questions
                    selectors = [
                        'li', 'p', 'h3', 'h4', 'h5', 'div.question', 
                        'div.truth-question', 'div.dare-question',
                        'span.question', 'article', 'section'
                    ]
                    
                    for selector in selectors:
                        elements = soup.select(selector)
                        for element in elements:
                            text = element.get_text().strip()
                            if self._is_valid_question(text):
                                questions.append(text)
                    
                    # Remove duplicates while preserving order
                    seen = set()
                    unique_questions = []
                    for question in questions:
                        if question not in seen:
                            seen.add(question)
                            unique_questions.append(question)
                    
                    return unique_questions[:MAX_QUESTIONS_PER_SOURCE]
                else:
                    print(f"Failed to scrape {url}: Status {response.status}")
                    return []
        except asyncio.TimeoutError:
            print(f"Timeout while scraping {url}")
            return []
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []
    
    async def get_all_questions(self, category):
        """Get all questions for a category from multiple sources"""
        # Check cache first
        if category in self.cache:
            cache_time, questions = self.cache[category]
            if datetime.now() - cache_time < self.cache_duration:
                return questions
        
        all_questions = []
        
        # Try primary sources
        urls = QUESTION_SOURCES.get(category, [])
        for url in urls:
            questions = await self.scrape_questions(url)
            all_questions.extend(questions)
        
        # If not enough questions, try alternative sources
        if len(all_questions) < 10:
            alt_urls = ALTERNATIVE_SOURCES.get(category, [])
            for url in alt_urls:
                questions = await self.scrape_questions(url)
                all_questions.extend(questions)
        
        # If still no questions, use fallback
        if not all_questions:
            all_questions = self.fallback_questions.get(category, [])
        
        # Cache the results
        self.cache[category] = (datetime.now(), all_questions)
        return all_questions
    
    async def get_random_question(self, category=None):
        """Get a random question from any category or a specific category"""
        if category is None:
            category = random.choice(list(QUESTION_SOURCES.keys()))
        
        questions = await self.get_all_questions(category)
        if questions:
            return random.choice(questions), category
        return None, None
    
    async def refresh_cache(self, category=None):
        """Refresh the cache for a specific category or all categories"""
        if category:
            if category in self.cache:
                del self.cache[category]
        else:
            self.cache.clear()
    
    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
    
    def get_cache_info(self):
        """Get information about the current cache"""
        info = {}
        for category, (cache_time, questions) in self.cache.items():
            age = datetime.now() - cache_time
            info[category] = {
                'question_count': len(questions),
                'cache_age_minutes': int(age.total_seconds() / 60),
                'is_fresh': age < self.cache_duration
            }
        return info 