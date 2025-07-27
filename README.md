# Truth and Truth Discord Bot

**Truth and Truth** is a fun and interactive Discord bot that engages users by randomly generating truth or dare questions. It scrapes popular websites for fresh questions and offers a comprehensive caching system for optimal performance. Whether you're looking for lighthearted conversation or trying to spice up a game night, this bot is the perfect companion for your Discord server.

## 🚀 Features

- **🌐 Web Scraping**: Automatically scrapes questions from multiple popular websites
- **🎯 Multiple Categories**: Truth questions, dare challenges, and "Would You Rather" questions
- **⚡ Intelligent Caching**: Caches questions for faster responses and reduced server load
- **🔄 Fallback System**: Uses curated fallback questions if web scraping fails
- **🎨 Beautiful Embeds**: Rich Discord embeds with colors and formatting
- **📊 Statistics**: Track bot performance and cache status
- **🛡️ Error Handling**: Robust error handling and user-friendly messages

## 📋 Commands

| Command | Description |
|---------|-------------|
| `!truth` | Get a random truth question |
| `!dare` | Get a random dare challenge |
| `!would_you_rather` | Get a random "Would You Rather" question |
| `!random` | Get a random question of any type |
| `!stats` | Show bot statistics and cache status |
| `!refresh` | Refresh the question cache |
| `!info` | Show help information |

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Discord bot token

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Truth-Truth
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the bot token

### 4. Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

### 5. Invite Bot to Server
1. Go to the "OAuth2" section in your Discord application
2. Select "bot" under scopes
3. Select the following permissions:
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open it in your browser to invite the bot

### 6. Run the Bot
```bash
python bot.py
```

## 🔧 Configuration

The bot can be customized by editing `config.py`:

- **Question Sources**: Add or modify websites to scrape from
- **Cache Duration**: Change how long questions are cached
- **Embed Colors**: Customize the appearance of Discord embeds
- **Filter Words**: Modify words to filter out during scraping

## 🏗️ Project Structure

```
Truth-Truth/
├── bot.py              # Main bot file
├── scraper.py          # Web scraping functionality
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your environment variables (create this)
└── README.md          # This file
```

## 🔍 How It Works

1. **Web Scraping**: The bot uses BeautifulSoup to scrape questions from multiple websites
2. **Question Validation**: Scraped text is validated to ensure it's actually a question
3. **Caching**: Questions are cached for 1 hour to improve performance
4. **Fallback System**: If scraping fails, the bot uses curated fallback questions
5. **Random Selection**: Questions are randomly selected from the available pool

## 🛡️ Error Handling

The bot includes comprehensive error handling:
- Network timeouts and connection errors
- Invalid HTML responses
- Missing or malformed data
- Rate limiting protection
- Graceful fallback to cached or default questions

## 📈 Performance Features

- **Async/Await**: Non-blocking operations for better performance
- **Connection Pooling**: Reuses HTTP connections
- **Intelligent Caching**: Reduces server load and improves response times
- **Timeout Protection**: Prevents hanging on slow websites

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the console output for error messages
2. Ensure your bot token is correct
3. Verify the bot has the necessary permissions
4. Check your internet connection for web scraping

## 🎉 Have Fun!

The Truth and Truth bot is designed to bring fun and entertainment to your Discord server. Use it responsibly and enjoy your conversations!
