#!/usr/bin/env python3
"""
Hacker News Top Stories Fetcher
Simple script to fetch and display HN top stories
"""

import json
import urllib.request

def fetch_hn_top_stories(count=10):
    """Fetch top stories from Hacker News"""
    url = f"https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            
            # Fetch details for each story
            stories = []
            for i, story_id in enumerate(data[:count]):
                detail_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                with urllib.request.urlopen(detail_url) as detail_response:
                    story = json.loads(detail_response.read())
                    stories.append(story)
            
            return stories
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    print("📰 Hacker News - Top Stories\n")
    
    stories = fetch_hn_top_stories(10)
    
    if not stories:
        print("Could not fetch stories.")
        return
    
    for i, story in enumerate(stories):
        title = story.get('title', 'No title')
        url = story.get('url', f"https://news.ycombinator.com/item?id={story['id']}")
        score = story.get('score', 0)
        
        print(f"{i+1}. {title}")
        print(f"   Score: {score}")
        print(f"   URL: {url}")
        print()

if __name__ == "__main__":
    main()
