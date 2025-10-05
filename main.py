from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from dotenv import load_dotenv

from models import (
    PersonProfile, 
    PersonProfileCreate, 
    PersonProfileResponse, 
    SimilaritySearchRequest, 
    SimilaritySearchResponse
)
from vector_db import VectorDatabase

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Dating App Person Matching Service",
    description="A service that matches people based on their personality descriptions using vector embeddings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector database
vector_db = VectorDatabase()


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "message": "Dating App Person Matching Service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "add_profile": "POST /profiles",
            "get_profile": "GET /profiles/{profile_id}",
            "search_similar": "POST /profiles/search",
            "get_all_profiles": "GET /profiles",
            "delete_profile": "DELETE /profiles/{profile_id}",
            "stats": "GET /stats"
        }
    }


@app.post("/profiles", response_model=dict)
async def add_person_profile(profile: PersonProfileCreate):
    """
    Add a new person profile to the database
    
    The description should include the person's habits, hobbies, likes, dislikes, 
    personality traits, interests, and other characteristics that would help 
    find compatible matches.
    """
    try:
        profile_id = vector_db.add_person_profile(profile)
        return {
            "message": "Profile added successfully",
            "profile_id": profile_id,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add profile: {str(e)}"
        )


@app.get("/profiles/{profile_id}", response_model=PersonProfile)
async def get_person_profile(profile_id: str):
    """Get a person profile by ID"""
    try:
        profile = vector_db.get_person_profile(profile_id)
        if profile is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with ID {profile_id} not found"
            )
        return profile
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve profile: {str(e)}"
        )


@app.post("/profiles/search", response_model=SimilaritySearchResponse)
async def search_similar_profiles(request: SimilaritySearchRequest):
    """
    Search for similar profiles based on personality description
    
    This endpoint finds people who have similar vibes, interests, and personality traits
    based on the provided description. Perfect for finding compatible matches!
    """
    try:
        # Validate limit
        if request.limit > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 50"
            )
        
        # Search for similar profiles
        similar_profiles = vector_db.search_similar_profiles(
            query_description=request.query_description,
            limit=request.limit,
            exclude_id=request.exclude_id
        )
        
        return SimilaritySearchResponse(
            query=request.query_description,
            results=similar_profiles,
            total_results=len(similar_profiles)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search profiles: {str(e)}"
        )


@app.get("/profiles", response_model=List[PersonProfile])
async def get_all_profiles(limit: int = 100):
    """Get all person profiles (with optional limit)"""
    try:
        if limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 1000"
            )
        
        profiles = vector_db.get_all_profiles(limit=limit)
        return profiles
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve profiles: {str(e)}"
        )


@app.delete("/profiles/{profile_id}")
async def delete_person_profile(profile_id: str):
    """Delete a person profile by ID"""
    try:
        success = vector_db.delete_person_profile(profile_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile with ID {profile_id} not found"
            )
        
        return {
            "message": "Profile deleted successfully",
            "profile_id": profile_id,
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}"
        )


@app.get("/stats")
async def get_stats():
    """Get database statistics"""
    try:
        stats = vector_db.get_collection_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get stats: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        stats = vector_db.get_collection_stats()
        return {
            "status": "healthy",
            "database": "connected",
            "stats": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
