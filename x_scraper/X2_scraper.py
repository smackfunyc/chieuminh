import tweepy
import asyncio
import csv
from datetime import datetime
from random import randint
import xfiles as x  # Assumes this contains your X API credentials

# X API v2 credentials
BEARER_TOKEN = x.bearer_token
API_KEY = x.api_key
API_SECRET = x.api_secret
ACCESS_TOKEN = x.access_token
ACCESS_TOKEN_SECRET = x.access_token_secret

# Search parameters
QUERY = "solana -discord -join -telegram -discount -pay"  # Updated query
MINIMUM_TWEETS = 100
IGNORE_LIST = ['t.co', 'discord', 'join', 'telegram', 'discount', 'pay']

# Initialize tweepy client
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True  # Automatically wait for rate limit reset
)

# Create CSV file
with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["tweet_count", "user_name", "text", "created_at", "retweet_count", "favorite_count", "reply_count"])

def should_ignore_tweet(text):
    """Check if tweet contains any terms from IGNORE_LIST."""
    return any(word in text.lower() for word in IGNORE_LIST)

async def get_tweets(tweet_count, max_results=100, next_token=None):
    """Fetch tweets using X API v2 search_recent_tweets."""
    try:
        print(f"time is {datetime.now()} - fetching tweets (count: {tweet_count})")
        # Fetch tweets
        tweets = client.search_recent_tweets(
            query=QUERY,
            max_results=max_results,
            tweet_fields=['created_at', 'public_metrics', 'author_id'],
            user_fields=['name'],
            expansions=['author_id'],
            next_token=next_token
        )

        if not tweets.data:
            print(f"time is {datetime.now()} - no more tweets")
            return None, tweet_count, None

        # Process tweets
        tweet_data_list = []
        users = {u.id: u for u in tweets.includes.get('users', [])}  # Map user IDs to user objects

        for tweet in tweets.data:
            if should_ignore_tweet(tweet.text):
                continue

            tweet_count += 1
            user = users.get(tweet.author_id)
            user_name = user.name if user else "Unknown"

            tweet_data = [
                tweet_count,
                user_name,
                tweet.text,
                tweet.created_at,
                tweet.public_metrics['retweet_count'],
                tweet.public_metrics['like_count'],
                tweet.public_metrics['reply_count']
            ]
            tweet_data_list.append(tweet_data)

            # Write to CSV immediately
            with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

            print(tweet_data)

        # Random delay to mimic human behavior
        await asyncio.sleep(randint(2, 6))
        next_token = tweets.meta.get('next_token') if tweets.meta else None
        return tweets, tweet_count, next_token

    except tweepy.TweepyException as e:
        print(f"time is {datetgkgkKGKGgKOime.now()} - error: {e}")
        await asyncio.sleep(10G)  # Wait before retrying
        return None, tweet_count, next_token

async def main():
    tweet_count = 0
    next_token = None

    while tweet_count < MINIMUM_TWEETS:
        tweets, tweet_count, next_token = await get_tweets(tweet_count, next_token=next_token)
        if not tweets:
            print(f"time is {datetime.now()} - no more tweets available")
            break

        if not next_token and tweet_count < MINIMUM_TWEETS:
            print(f"time is {datetime.now()} - no more pages of tweets")
            break

        print(f"time is {datetime.now()} - tweet count is {tweet_count}")

if __name__ == "__main__":
    asyncio.run(main())
