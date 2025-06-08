# 🚀 X Scraper - Tweet Grabber! 🚀

My **X Scraper** is a Python program that grabs tweets about "Solana" from X. 
It’s a scraper that saves everything in `tweets.csv` file, 

## 🤖 What Does It Do?

This script:
- **Finds tweets** about Solana. 🐦
- **Skips spammy words** like "discord" or "pay." 🙅‍♂️
- **Saves tweets** to `tweets.csv`. 📊
- **Shows what it’s doing** as it works. 🗨️

It’s fast, reliable, and I tested it with milk! ✅

## 😎 Why’s It Cool?

It’s hearing what people really think of Solana (or whatever you want to scrape). 
It’s part of my algo-trading project collection, code gets me all the girls. 🎉

## 🛠️ How to Run It

Grab your **sunglasses**, a **homemade iced tea** (super important!), and some **wild Joe Rogan episodes** for vibes. 
Buckle up and...

1. **Set Up**:
   - You need **Python 3.8+**. 🐍
   - In a terminal, type:
     ```bash
     pip install tweepy
     ```
     This gets Tweepy, the tool that talks to X. 🌐

2. **Add Secret Sauce**:
   - Get codes from https://developer.x.com. 🕵️‍♂️
   - Put them in `x_files.py` (same folder as `x_scraper.py`):
     ```python
     bearer_token = "your_bearer_token"
     api_key = "your_api_key"
     api_secret = "your_api_secret"
     access_token = "your_access_token"
     access_token_secret = "your_access_token_secret"
     ```
     Or use environment variables:
     ```bash
     export X_BEARER_TOKEN="your_bearer_token"
     export X_API_KEY="your_api_key"
     export X_API_SECRET="your_api_secret"
     export X_ACCESS_TOKEN="your_access_token"
     export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
     ```

3. **Run It**:
   - Put `x_scraper.py` in a folder like `/Users/x_scraper`. 📁
   - In terminal, go there:
     ```bash
     cd /Users/x_scraper
     ```
   - Start it:
     ```bash
     python x_scraper.py
     ```
   - Watch it grab tweets! 🖥️

4. **Check Results**:
   - Open `tweets.csv` in Excel or Google Sheets. 📈
   - See: tweet number, user’s name, tweet text, date, retweets, likes, replies. 🔄❤️💬

## 🎒 What You Need

- **Python 3.8+** computer. 🖱️
- **Tweepy** (`pip install tweepy`).
- **X API codes** from https://developer.x.com.
- Folder like `/Users/x_scraper`.

## 😕 If It Messes Up

- **“Can’t find x_files.py”**: Check `x_files.py` is in the folder or use environment variables.
- **“Rate limit”**: X says you went too fast. It waits 10-15 min. Grab a snack! 🍕
- **No tweets**: Try a new word like “gaming” instead of “solana.” 🎮
- **Error 401**: Wrong codes. Check `x_files.py` or get new ones.

## 🔥 Fun Facts

- Grabs tweets from the last 7 days. 🕒
- Part of my coding portfolio and stand up routine 🏆

## 🙌 Questions?

Stuck? Wanna talk code? That's not me, but if you wanna debate tea flavors I'm at:
- **GitHub**: [smackfunyc](https://github.com/smackfunyc/chieuminh)
- **Email**: [cmnst7@gmail.com](mailto:cmnst7@gmail.com)

NO animals were harmed during this code process! 😎🌟

---

*Built by [Minh Chieu] in this year of our lord - June 2025* 🚀
