#!/usr/bin/env python3
"""
Example usage of the Dating App Person Matching Service

This script demonstrates how to use the API to add profiles and find matches.
"""

import requests
import json
import time
from typing import List, Dict

# Configuration
BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30


class DatingAppClient:
    """Client for interacting with the dating app matching service"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def add_profile(self, name: str, description: str, age: int = None, location: str = None) -> str:
        """Add a new person profile"""
        profile_data = {
            "name": name,
            "description": description,
            "age": age,
            "location": location
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/profiles",
                json=profile_data,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result["profile_id"]
        except requests.exceptions.RequestException as e:
            print(f"Error adding profile: {e}")
            raise
    
    def search_matches(self, query_description: str, limit: int = 5, exclude_id: str = None) -> List[Dict]:
        """Search for matching profiles"""
        search_data = {
            "query_description": query_description,
            "limit": limit,
            "exclude_id": exclude_id
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/profiles/search",
                json=search_data,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            result = response.json()
            return result["results"]
        except requests.exceptions.RequestException as e:
            print(f"Error searching matches: {e}")
            raise
    
    def get_profile(self, profile_id: str) -> Dict:
        """Get a specific profile"""
        try:
            response = requests.get(
                f"{self.base_url}/profiles/{profile_id}",
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting profile: {e}")
            raise
    
    def get_all_profiles(self, limit: int = 100) -> List[Dict]:
        """Get all profiles"""
        try:
            response = requests.get(
                f"{self.base_url}/profiles?limit={limit}",
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting all profiles: {e}")
            raise
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/stats",
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting stats: {e}")
            raise


def main():
    """Main example function"""
    print("🚀 Dating App Person Matching Service - Example Usage")
    print("=" * 60)
    
    # Initialize client
    client = DatingAppClient()
    
    # Check if service is running
    try:
        stats = client.get_stats()
        print(f"✅ Service is running. Current profiles: {stats.get('total_profiles', 0)}")
    except Exception as e:
        print(f"❌ Service is not running or not accessible: {e}")
        print("Please start the service with: python main.py")
        return
    
    print("\n📝 Adding sample profiles...")
    
    # Sample profiles with diverse personalities
    sample_profiles = [
        {
            "name": "Alex",
            "description": "I love hiking in the mountains, reading sci-fi novels, cooking Italian food, and playing guitar. I enjoy quiet evenings with good wine and meaningful conversations. I dislike loud parties and superficial interactions. I'm an introvert who values deep connections and intellectual discussions about philosophy and technology.",
            "age": 28,
            "location": "San Francisco"
        },
        {
            "name": "Sarah",
            "description": "I'm passionate about photography, yoga, and traveling to new places. I love trying different cuisines and meeting people from different cultures. I enjoy reading memoirs and watching documentaries. I value honesty, kindness, and someone who can make me laugh. I'm looking for someone who shares my sense of adventure and curiosity about the world.",
            "age": 26,
            "location": "New York"
        },
        {
            "name": "Jordan",
            "description": "I'm a fitness enthusiast who loves rock climbing, CrossFit, and outdoor adventures. I enjoy cooking healthy meals and experimenting with new recipes. I'm into self-improvement books and podcasts. I value discipline, authenticity, and someone who challenges me to be better. I'm looking for a partner who shares my active lifestyle and growth mindset.",
            "age": 30,
            "location": "Denver"
        },
        {
            "name": "Casey",
            "description": "I'm an artist who loves painting, visiting museums, and attending art shows. I enjoy jazz music, vintage vinyl records, and cozy coffee shops. I'm introverted but love deep conversations about creativity and meaning. I value emotional intelligence, empathy, and someone who appreciates beauty in everyday life. I'm looking for someone who understands the artist's soul.",
            "age": 24,
            "location": "Portland"
        },
        {
            "name": "Riley",
            "description": "I'm a software engineer who loves coding, playing video games, and attending tech meetups. I enjoy anime, board games, and building side projects. I'm into science fiction and fantasy novels. I value intelligence, creativity, and someone who shares my nerdy interests. I'm looking for someone who can appreciate both my logical side and my playful imagination.",
            "age": 27,
            "location": "Seattle"
        }
    ]
    
    # Add profiles
    profile_ids = []
    for profile_data in sample_profiles:
        try:
            profile_id = client.add_profile(**profile_data)
            profile_ids.append(profile_id)
            print(f"✅ Added {profile_data['name']} (ID: {profile_id[:8]}...)")
        except Exception as e:
            print(f"❌ Failed to add {profile_data['name']}: {e}")
    
    print(f"\n📊 Database now has {len(profile_ids)} profiles")
    
    # Wait a moment for embeddings to be processed
    print("\n⏳ Waiting for embeddings to be processed...")
    time.sleep(2)
    
    # Example searches
    search_examples = [
        {
            "title": "Looking for outdoor enthusiasts",
            "query": "I want to find someone who loves hiking, rock climbing, and outdoor adventures. Someone who enjoys being active and exploring nature. I value someone who shares my passion for fitness and adventure.",
            "limit": 3
        },
        {
            "title": "Seeking artistic and creative types",
            "query": "Looking for someone who appreciates art, creativity, and beauty. I love visiting museums, attending art shows, and having deep conversations about meaning and expression. Someone who values emotional intelligence and artistic expression.",
            "limit": 3
        },
        {
            "title": "Tech-savvy and nerdy matches",
            "query": "I want to find someone who loves technology, coding, video games, and nerdy hobbies. Someone who enjoys science fiction, board games, and intellectual discussions. I value intelligence, creativity, and shared interests in tech and gaming.",
            "limit": 3
        },
        {
            "title": "Adventure and travel lovers",
            "query": "Seeking someone who loves traveling, trying new cuisines, meeting people from different cultures, and exploring the world. I value curiosity, openness to new experiences, and someone who shares my sense of adventure and wonder.",
            "limit": 3
        }
    ]
    
    print("\n🔍 Running example searches...")
    
    for i, search_example in enumerate(search_examples, 1):
        print(f"\n--- Search {i}: {search_example['title']} ---")
        print(f"Query: {search_example['query']}")
        
        try:
            matches = client.search_matches(
                query_description=search_example['query'],
                limit=search_example['limit']
            )
            
            print(f"\nFound {len(matches)} matches:")
            for j, match in enumerate(matches, 1):
                print(f"{j}. {match['name']} (Age: {match['age']}, Location: {match['location']})")
                print(f"   Similarity: {match['similarity_score']:.3f}")
                print(f"   Description: {match['description'][:150]}...")
                print()
        
        except Exception as e:
            print(f"❌ Search failed: {e}")
    
    # Show final stats
    print("\n📈 Final Statistics:")
    try:
        final_stats = client.get_stats()
        print(json.dumps(final_stats, indent=2))
    except Exception as e:
        print(f"❌ Failed to get final stats: {e}")
    
    print("\n✨ Example completed! You can now:")
    print("- Add more profiles using the API")
    print("- Search for matches with different queries")
    print("- View the interactive API docs at http://localhost:8000/docs")
    print("- Modify the service to fit your dating app needs")


if __name__ == "__main__":
    main()
