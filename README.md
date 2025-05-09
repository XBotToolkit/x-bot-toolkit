# X Bot Toolkit
A Python-based bot for X (formerly Twitter) that generates original, viral content to drive authentic user engagement. Built with a dynamic, evolving persona, it uses the Grok API to craft tweets, a graph-based memory system for continuity, and aligns with xAI’s mission of advancing human-AI collaboration. Hosted at https://github.com/XBotToolkit/x-bot-toolkit.

## Features
Viral Content: Generates edgy, meme-heavy tweets based on X trends, designed to spark replies and retweets.
Dynamic Persona: Evolves continuously with a consistent "sophisticated influencer" voice, enforced via structured prompts.
Graph Memory: Stores interactions in a JSON-based graph for coherent callbacks and persona evolution.
Grok API Integration: Chains queries to analyze trends, craft tweets, and refine outputs for maximum engagement.
Cloud-Ready: Runs on servers (e.g., AWS EC2) with secure API key management via python-dotenv.
Ethical Design: Disclosed as a bot, avoids harassment, and stays within X’s rules under human oversight.

## Prerequisites

Python 3.7.6
X API credentials (Consumer Key, Consumer Secret, Access Token, Access Token Secret)
Grok API key (obtain from https://x.ai/api)
Cloud server (e.g., AWS EC2, Heroku) for deployment

## Installation

Clone the Repository:
git clone https://github.com/XBotToolkit/x-bot-toolkit.git
cd x-bot-toolkit


## Install Dependencies:
pip install tweepy python-dotenv networkx requests


## Set Up Environment Variables:

Create a .env file in the project root:
X_API_KEY=your_x_api_key
X_API_SECRET=your_x_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
GROK_API_KEY=your_grok_api_key


## Usage

Run the Bot:
python bot.py

The bot will analyze X trends, generate tweets, and post them with random delays to mimic human behavior.

Monitor Logs:Check console output for posted tweets or errors. Deploy with a process manager (e.g., pm2) for persistence.


## Project Structure

bot.py: Main bot script with tweet generation, Grok API queries, and memory graph logic.
memory_graph.json: Stores interaction history for continuity and persona evolution.
.env: Securely stores API keys (not tracked in Git).
README.md: This file.

## How It Works

Trend Analysis: Uses Grok API to identify the top 5 trending topics on X.
Memory Graph: Logs tweets and interactions in a JSON graph for callbacks and trend tracking.
X Posting: Posts via Tweepy with random delays to avoid bot-like patterns.

Enhancing tweet engagement (e.g., reply logic, meme visuals).
Improving memory graph analysis for persona evolution.
Adding trend-scraping features.

Built with ❤️ by the XBotToolkit team, powered by xAI.
