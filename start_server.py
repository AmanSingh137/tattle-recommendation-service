#!/usr/bin/env python3
"""
Startup script for the Dating App Person Matching Service

This script handles environment setup and starts the FastAPI server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sentence_transformers
        import chromadb
        import pydantic
        import numpy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables and directories"""
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_example = Path(".env.example")
        if env_example.exists():
            print("📝 Creating .env file from .env.example")
            env_file.write_text(env_example.read_text())
        else:
            print("📝 Creating default .env file")
            env_content = """# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=person_profiles

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
"""
            env_file.write_text(env_content)
    
    # Create chroma_db directory if it doesn't exist
    chroma_dir = Path("./chroma_db")
    chroma_dir.mkdir(exist_ok=True)
    print("📁 Database directory ready")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Dating App Person Matching Service...")
    print("=" * 50)
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    """Main function"""
    print("💕 Dating App Person Matching Service")
    print("=====================================\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
