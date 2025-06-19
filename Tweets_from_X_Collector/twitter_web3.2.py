import asyncio
import httpx
from twikit import Client, TooManyRequests
import time
from datetime import datetime
from random import randint
import gradio as gr
import pandas as pd
import os

# Web3 Style Configuration
WEB3_THEME = gr.themes.Default(
    primary_hue="purple",
    secondary_hue="pink",
    neutral_hue="slate",
    radius_size="lg",
    font=[gr.themes.GoogleFont("Poppins"), "ui-sans-serif", "system-ui"]
).set(
    button_primary_background_fill="linear-gradient(90deg, #8a2be2 0%, #ff6bff 100%)",
    button_primary_text_color="white",
    button_primary_background_fill_hover="linear-gradient(90deg, #7b1fa2 0%, #e91e63 100%)",
    button_secondary_background_fill="linear-gradient(90deg, #4b0082 0%, #9400d3 100%)",
    slider_color="#8a2be2",
    checkbox_label_background_fill_selected="#8a2be2",
    block_background_fill="#1e1e2e",
    block_label_text_color="#ffffff",
    block_title_text_color="#ffffff",
    input_background_fill="#2d2d3d"
)

class TwitterDataCollector:
    def __init__(self):
        self.client = None
        self.running = False
        self.tweet_count = 0
        self.tweets = None
        self.df = pd.DataFrame(columns=[
            "tweet_count", "username", "text", "created_at", 
            "retweets", "likes", "replies"
        ])
    
    async def login(self, email, password):
        self.client = Client('en-US')
        try:
            await self.client.login(
                auth_info_1=email,
              #  auth_info_2=username,
                password=password
            )
            self.client.save_cookies("cookies.json")
            return "✅ Login successful!"
        except Exception as e:
            return f"❌ Login failed: {str(e)}"
    
    def should_ignore_tweet(self, text, ignore_list):
        text_lower = text.lower()
        return any(ignore.lower() in text_lower for ignore in ignore_list)
    
    async def get_tweets(self, query, style, max_tweets, ignore_list):
        if not self.client:
            return "⚠️ Please login first", None, None
        
        self.running = True
        self.tweet_count = 0
        self.tweets = None
        self.df = self.df.iloc[0:0]  # Clear dataframe
        
        while self.tweet_count < max_tweets and self.running:
            try:
                if self.tweets is None:
                    print(f"🔍 Initial search for {query}")
                    time.sleep(randint(2, 6))
                    self.tweets = await self.client.search_tweet(query, product=style, count=100)
                else:
                    print("⏭ Getting next page")
                    time.sleep(randint(5, 13))
                    self.tweets = await self.tweets.next()
                
                if not self.tweets:
                    break
                    
                for tweet in self.tweets:
                    if self.should_ignore_tweet(tweet.text, ignore_list):
                        continue
                        
                    self.tweet_count += 1
                    
                    new_row = {
                        "tweet_count": self.tweet_count,
                        #"username": tweet.user.name,
                        "text": tweet.text,
                        "created_at": tweet.created_at,
                        "retweets": tweet.retweet_count,
                        "likes": tweet.favorite_count,
                        "replies": tweet.reply_count
                    }
                    
                    self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
                    
                    if self.tweet_count >= max_tweets:
                        break
                        
            except TooManyRequests as e:
                wait_time = e.rate_limit_reset - time.time()
                print(f"⏳ Rate limited. Waiting {wait_time:.1f} seconds...")
                time.sleep(max(wait_time, 0))
                continue
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(60)
                continue
        
        # Save to CSV
        csv_path = 'tweets.csv'
        self.df.to_csv(csv_path, index=False)
        status = f"✅ Collected {self.tweet_count} tweets"
        return status, self.df if not self.df.empty else None, csv_path
    
    def stop_collection(self):
        self.running = False
        return "⏹ Collection stopped"

def create_web3_interface():
    agent = TwitterDataCollector()
    
    with gr.Blocks(theme=WEB3_THEME, title="Web3 Twitter Collector") as demo:
        gr.Markdown("""
        #  Minh's X Twitter Collector
        *Collect and analyze tweets with Web3 style*
        """)
        
        with gr.Tab("🔐 Authentication"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Twitter Credentials")
                   # username = gr.Textbox(label="Username", placeholder="Your Twitter username")
                    email = gr.Textbox(label="Email", placeholder="Your Twitter email")
                    password = gr.Textbox(label="Password", type="password")
                    login_btn = gr.Button("Login", variant="primary")
                    login_status = gr.Textbox(label="Status", interactive=False)
                    
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### 📝 Instructions
                    1. Enter your Twitter credentials
                    2. Login to authenticate
                    3. Go to 'Collect Tweets' tab
                    4. Set your search parameters
                    5. Start collection!
                    """)
            
            login_btn.click(
                agent.login,
                inputs=[ email, password],
                outputs=login_status
            )
        
        with gr.Tab("🐦 Collect Tweets"):
            with gr.Row():
                with gr.Column(scale=2):
                    query = gr.Textbox(
                        label="Search Query",
                        placeholder="Enter hashtag, keyword or phrase",
                        value="solana"
                    )
                    ignore_list = gr.Textbox(
                        label="Words to Ignore (comma separated)",
                        value="t.co,discord,join,telegram,retweet,follow,like"
                    )
                    
                    with gr.Row():
                        search_style = gr.Radio(
                            label="Search Style",
                            choices=["LATEST", "TOP", "PEOPLE", "PHOTOS", "VIDEOS"],
                            value="LATEST"
                        )
                        max_tweets = gr.Slider(
                            label="Max Tweets to Collect",
                            minimum=100,
                            maximum=5000,
                            step=100,
                            value=1000
                        )
                    
                    with gr.Row():
                        collect_btn = gr.Button("🚀 Start Collection", variant="primary")
                        stop_btn = gr.Button("🛑 Stop Collection")
                
                with gr.Column(scale=3):
                    status = gr.Textbox(label="Collection Status", interactive=False)
                    results = gr.Dataframe(
                        headers=["Count", "Username", "Text", "Date", "Retweets", "Likes", "Replies"],
                        datatype=["number", "str", "str", "str", "number", "number", "number"],
                        interactive=False
                    )
            
            collect_btn.click(
                agent.get_tweets,
                inputs=[query, search_style, max_tweets, ignore_list],
                outputs=[status, results, gr.File(label="Download CSV")]
            )
            stop_btn.click(agent.stop_collection, outputs=status)
        
        # New section for displaying tweets
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Collected Tweets Preview")
                tweet_display = gr.Dataframe(
                    headers=["Count", "Username", "Text", "Date", "Retweets", "Likes", "Replies"],
                    datatype=["number", "str", "str", "str", "number", "number", "number"],
                    interactive=False,
                    elem_id="tweet-display"
                )
        
        # Update the display when collection completes
        collect_btn.click(
            lambda df: df,
            inputs=[results],
            outputs=[tweet_display]
        )
    
    return demo

if __name__ == "__main__":
    # Run the Web3 interface
    web3_app = create_web3_interface()
    web3_app.launch(share=True)