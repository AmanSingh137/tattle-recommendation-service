# Tattle Person Matching Service

A service that matches people based on their personality descriptions using vector embeddings. Perfect to find compatible matches based on vibes, interests, and personality traits.

## Features

- **Vector Embeddings**: Uses sentence transformers to convert personality descriptions into high-dimensional vectors
- **Similarity Search**: Find people with similar personalities using cosine similarity
- **Flexible Matching**: Search for 5, 10, 20, or any number of matches
- **Persistent Storage**: Uses ChromaDB for efficient vector storage and retrieval
- **RESTful API**: Clean FastAPI endpoints for easy integration
- **Real-time Search**: Fast similarity search with configurable result counts

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env file with your preferred settings
   ```

## Quick Start

1. **Start the service**:
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

2. **View API documentation**:
   Visit `http://localhost:8000/docs` for interactive API documentation

## API Usage

### 1. Add a Person Profile

```bash
curl -X POST "http://localhost:8000/profiles" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alex",
       "description": "I love hiking in the mountains, reading sci-fi novels, cooking Italian food, and playing guitar. I enjoy quiet evenings with good wine and meaningful conversations. I dislike loud parties and superficial interactions. I'm an introvert who values deep connections and intellectual discussions about philosophy and technology.",
       "age": 28,
       "location": "San Francisco"
     }'
```

### 2. Search for Similar Profiles

```bash
curl -X POST "http://localhost:8000/profiles/search" \
     -H "Content-Type: application/json" \
     -d '{
       "query_description": "Looking for someone who enjoys outdoor adventures, loves reading, appreciates good food, and values meaningful conversations over small talk. Someone who is introverted but loves deep discussions about life and ideas.",
       "limit": 10
     }'
```

### 3. Get a Specific Profile

```bash
curl -X GET "http://localhost:8000/profiles/{profile_id}"
```

### 4. Get All Profiles

```bash
curl -X GET "http://localhost:8000/profiles?limit=50"
```

## Example Python Client

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Add a profile
profile_data = {
    "name": "Sarah",
    "description": "I'm passionate about photography, yoga, and traveling to new places. I love trying different cuisines and meeting people from different cultures. I enjoy reading memoirs and watching documentaries. I value honesty, kindness, and someone who can make me laugh. I'm looking for someone who shares my sense of adventure and curiosity about the world.",
    "age": 26,
    "location": "New York"
}

response = requests.post(f"{BASE_URL}/profiles", json=profile_data)
profile_id = response.json()["profile_id"]
print(f"Added profile with ID: {profile_id}")

# Search for similar profiles
search_query = {
    "query_description": "I want to find someone who loves photography, enjoys traveling, is curious about different cultures, and values deep conversations. Someone who appreciates art and has a sense of adventure.",
    "limit": 5
}

response = requests.post(f"{BASE_URL}/profiles/search", json=search_query)
matches = response.json()["results"]

print(f"Found {len(matches)} potential matches:")
for match in matches:
    print(f"- {match['name']} (Age: {match['age']}, Similarity: {match['similarity_score']:.3f})")
    print(f"  Description: {match['description'][:100]}...")
    print()
```

## Configuration

### Environment Variables

- `CHROMA_PERSIST_DIRECTORY`: Directory to store the vector database (default: `./chroma_db`)
- `COLLECTION_NAME`: Name of the ChromaDB collection (default: `person_profiles`)
- `API_HOST`: API host address (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)
- `EMBEDDING_MODEL`: Sentence transformer model to use (default: `all-MiniLM-L6-v2`)

### Available Embedding Models

- `all-MiniLM-L6-v2` (default): Fast and efficient, good for most use cases
- `all-mpnet-base-v2`: Higher quality but slower
- `all-distilroberta-v1`: Balanced performance
- `paraphrase-multilingual-MiniLM-L12-v2`: Supports multiple languages

## How It Works

1. **Text to Vector**: When you add a person's description, it's converted to a high-dimensional vector using sentence transformers
2. **Storage**: The vector is stored in ChromaDB with metadata (name, age, location, etc.)
3. **Similarity Search**: When searching, your query is also converted to a vector
4. **Matching**: The system finds the most similar vectors using cosine similarity
5. **Results**: Returns profiles ranked by similarity score (0-1, higher is more similar)

## Tips for Better Matching

### Writing Good Descriptions

**Good descriptions include**:
- Specific hobbies and interests
- Personality traits
- Values and preferences
- Lifestyle choices
- What you're looking for in a partner

**Example of a good description**:
> "I'm a software engineer who loves rock climbing on weekends and cooking elaborate meals for friends. I enjoy reading fantasy novels and playing board games. I value honesty, intellectual conversations, and someone who can make me laugh. I'm looking for someone who shares my love for outdoor adventures and appreciates both nerdy discussions and spontaneous road trips."

**Avoid**:
- Generic statements like "I like to have fun"
- Only physical descriptions
- Too short descriptions (less than 50 words)
- Negative descriptions focusing only on what you don't like

### Search Query Tips

- Be specific about what you're looking for
- Include personality traits, interests, and values
- Mention lifestyle preferences
- The more detailed your search, the better the matches

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service information and available endpoints |
| POST | `/profiles` | Add a new person profile |
| GET | `/profiles/{id}` | Get a specific profile |
| POST | `/profiles/search` | Search for similar profiles |
| GET | `/profiles` | Get all profiles (with limit) |
| DELETE | `/profiles/{id}` | Delete a profile |
| GET | `/stats` | Get database statistics |
| GET | `/health` | Health check |

## Performance

- **Embedding Generation**: ~100-500ms per description (depending on model)
- **Similarity Search**: ~50-200ms for 1000+ profiles
- **Storage**: ~1-2MB per 1000 profiles (depending on description length)

## Troubleshooting

### Common Issues

1. **Model loading errors**: The service will fallback to a default model if the specified one fails
2. **ChromaDB issues**: Make sure the persist directory is writable
3. **Memory issues**: For large datasets, consider using a lighter embedding model

### Logs

The service provides detailed logging for debugging. Check the console output for:
- Model loading status
- Database operations
- Error messages with stack traces

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
