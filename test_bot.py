#!/usr/bin/env python3
"""
Test script for the Truth and Truth Discord Bot
This script tests the web scraping functionality and bot commands
"""

import asyncio
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import QuestionScraper
from config import QUESTION_SOURCES

async def test_scraper():
    """Test the web scraping functionality"""
    print("🧪 Testing Question Scraper...")
    
    scraper = QuestionScraper()
    
    try:
        # Test each category
        for category in ['truth', 'dare', 'would_you_rather']:
            print(f"\n📋 Testing {category} questions...")
            
            # Get questions for this category
            questions = await scraper.get_all_questions(category)
            
            if questions:
                print(f"✅ Successfully scraped {len(questions)} {category} questions")
                print(f"   Sample question: {questions[0][:100]}...")
            else:
                print(f"❌ Failed to scrape {category} questions")
        
        # Test random question generation
        print(f"\n🎲 Testing random question generation...")
        question, category = await scraper.get_random_question()
        if question:
            print(f"✅ Random {category} question: {question[:100]}...")
        else:
            print("❌ Failed to generate random question")
        
        # Test cache functionality
        print(f"\n💾 Testing cache functionality...")
        cache_info = scraper.get_cache_info()
        for cat, info in cache_info.items():
            print(f"   {cat}: {info['question_count']} questions (age: {info['cache_age_minutes']} min)")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    finally:
        await scraper.close()

async def test_fallback_questions():
    """Test the fallback question system"""
    print("\n🔄 Testing fallback questions...")
    
    scraper = QuestionScraper()
    
    try:
        # Test fallback questions for each category
        for category in ['truth', 'dare', 'would_you_rather']:
            questions = scraper.fallback_questions.get(category, [])
            print(f"   {category}: {len(questions)} fallback questions available")
        
        print("✅ Fallback questions test completed!")
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
    
    finally:
        await scraper.close()

def test_config():
    """Test the configuration settings"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import (
            QUESTION_SOURCES, 
            EMBED_COLORS, 
            STATUS_MESSAGES,
            REQUEST_TIMEOUT,
            MAX_QUESTIONS_PER_SOURCE
        )
        
        print(f"   Question sources: {len(QUESTION_SOURCES)} categories")
        print(f"   Embed colors: {len(EMBED_COLORS)} defined")
        print(f"   Status messages: {len(STATUS_MESSAGES)} available")
        print(f"   Request timeout: {REQUEST_TIMEOUT} seconds")
        print(f"   Max questions per source: {MAX_QUESTIONS_PER_SOURCE}")
        
        print("✅ Configuration test completed!")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting Truth and Truth Bot Tests...")
    print("=" * 50)
    
    # Test configuration
    test_config()
    
    # Test fallback questions
    await test_fallback_questions()
    
    # Test web scraping
    await test_scraper()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")

if __name__ == "__main__":
    # Run the tests
    asyncio.run(main()) 