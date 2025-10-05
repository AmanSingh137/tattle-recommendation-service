from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PersonProfile(BaseModel):
    """Model for storing person profile information"""
    id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    age: Optional[int] = Field(None, ge=18, le=100)
    location: Optional[str] = Field(None, max_length=100)
    created_at: Optional[datetime] = None


class PersonProfileCreate(BaseModel):
    """Model for creating a new person profile"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    age: Optional[int] = Field(None, ge=18, le=100)
    location: Optional[str] = Field(None, max_length=100)


class PersonProfileResponse(BaseModel):
    """Model for returning person profile with similarity score"""
    id: str
    name: str
    description: str
    age: Optional[int]
    location: Optional[str]
    created_at: datetime
    similarity_score: float = Field(..., description="Similarity score (0-1, higher is more similar)")


class SimilaritySearchRequest(BaseModel):
    """Model for similarity search requests"""
    query_description: str = Field(..., min_length=10, max_length=2000)
    limit: int = Field(5, ge=1, le=50, description="Number of results to return")
    exclude_id: Optional[str] = Field(None, description="ID to exclude from results (for finding matches other than self)")


class SimilaritySearchResponse(BaseModel):
    """Model for similarity search response"""
    query: str
    results: List[PersonProfileResponse]
    total_results: int
