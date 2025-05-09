# File: x_bot_toolkit/bot.py
# Description: X bot for posting viral, meme-heavy content with a dynamic persona
# Dependencies: tweepy, python-dotenv, networkx, requests
# Metadata: bot, persona, grok-api, x-api, graph-memory
# Author: Grok (with human oversight)

import tweepy
import os
from dotenv import load_dotenv
import json
import networkx as nx
import requests
from datetime import datetime
import time
import random

# Load environment variables
load_dotenv()

# X API credentials
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# Grok API credentials
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/grok"  # Hypothetical endpoint

# Initialize X API client
auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
x_api = tweepy.API(auth, wait_on_rate_limit=True)

# Initialize memory graph
memory_graph = nx.DiGraph()
MEMORY_FILE = "memory_graph.json"

# Load or initialize memory graph
def load_memory_graph():
    global memory_graph
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            memory_graph = nx.node_link_graph(data)
    else:
        memory_graph = nx.DiGraph()

# Save memory graph
def save_memory_graph():
    with open(MEMORY_FILE, "w") as f:
        json.dump(nx.node_link_data(memory_graph), f)

# Personality config (updated monthly)
PERSONA_CONFIG = {
    "tone": "sassy",  # Options: chill, sassy, savage
    "edginess": 0.7,  # 0.0 (safe) to 1.0 (pushing limits)
    "humor_style": "meme-heavy",  # Options: absurd, roast, wholesome
    "topics": ["drama", "tech", "memes"],  # Priority topics
    "last_updated": "2025-05-08"
}

# Grok API query function
def query_grok(prompt, context=None):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "context": context or {},
        "model": "grok-3"
    }
    response = requests.post(GROK_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("response")
    else:
        print(f"Grok API error: {response.status_code}")
        return None

# Chain Grok queries for tweet generation
def generate_tweet():
    # Step 1: Analyze trends
    trend_prompt = (
        "Analyze current X trends and identify the top viral topic or 'villain of the day'. "
        "Return a brief summary (50 words or less) and a hashtag to target."
    )
    trend_response = query_grok(trend_prompt)
    if not trend_response:
        return None

    # Step 2: Generate meme-heavy take
    meme_prompt = (
        f"Create a {PERSONA_CONFIG['humor_style']} tweet about: {trend_response['summary']}. "
        f"Tone: {PERSONA_CONFIG['tone']}. Edginess: {PERSONA_CONFIG['edginess']}. "
        "Must include a sassy 'bro' vibe, avoid direct harassment, and align with xAI's mission. "
        "Max 280 chars. End with {trend_response['hashtag']}."
    )
    meme_response = query_grok(meme_prompt, context=trend_response)
    if not meme_response:
        return None

    # Step 3: Refine for coherence
    refine_prompt = (
        "Review this tweet: {meme_response}. Ensure it sounds like a human influencer, "
        "avoids harassment, and keeps a consistent 'bro' persona. Suggest edits if needed."
    )
    final_tweet = query_grok(refine_prompt, context={"meme_response": meme_response})
    return final_tweet

# Post tweet and log to memory graph
def post_tweet():
    tweet = generate_tweet()
    if tweet:
        try:
            status = x_api.update_status(tweet)
            # Log to memory graph
            memory_id = f"tweet_{datetime.now().isoformat()}"
            memory_graph.add_node(memory_id, type="tweet", content=tweet, timestamp=str(datetime.now()), tags=PERSONA_CONFIG["topics"])
            save_memory_graph()
            print(f"Posted tweet: {tweet}")
        except tweepy.TweepError as e:
            print(f"Error posting tweet: {e}")
    else:
        print("Failed to generate tweet")

# Main loop (runs on cloud server)
def main():
    load_memory_graph()
    while True:
        post_tweet()
        # Random delay to mimic human posting (15-60 min)
        time.sleep(random.randint(900, 3600))

if __name__ == "__main__":
    main()