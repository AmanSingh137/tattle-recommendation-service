import os
import uuid
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from models import PersonProfile, PersonProfileCreate, PersonProfileResponse
from embedding_service import EmbeddingService

load_dotenv()


class VectorDatabase:
    """Vector database service using ChromaDB for storing and retrieving person profiles"""
    
    def __init__(self, persist_directory: str = None, collection_name: str = None):
        """
        Initialize the vector database
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection to use
        """
        self.persist_directory = persist_directory or os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "person_profiles")
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding service
        self.embedding_service = EmbeddingService()
        
        # Get or create collection
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create a new one"""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(name=self.collection_name)
            print(f"Using existing collection: {self.collection_name}")
            return collection
        except (ValueError, Exception):
            # Collection doesn't exist, create it
            # Catch both ValueError (old ChromaDB) and NotFoundError (new ChromaDB)
            print(f"Creating new collection: {self.collection_name}")
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Person profiles for dating app matching"}
            )
            return collection
    
    def add_person_profile(self, profile: PersonProfileCreate) -> str:
        """
        Add a new person profile to the database
        
        Args:
            profile: Person profile to add
            
        Returns:
            Unique ID of the added profile
        """
        try:
            # Generate unique ID
            profile_id = str(uuid.uuid4())
            
            # Generate embedding for the description
            embedding = self.embedding_service.generate_embedding(profile.description)
            
            # Prepare metadata
            metadata = {
                "name": profile.name,
                "age": profile.age,
                "location": profile.location,
                "created_at": datetime.now().isoformat()
            }
            
            # Add to collection
            self.collection.add(
                ids=[profile_id],
                embeddings=[embedding],
                documents=[profile.description],
                metadatas=[metadata]
            )
            
            print(f"Added person profile with ID: {profile_id}")
            return profile_id
        
        except Exception as e:
            print(f"Error adding person profile: {e}")
            raise
    
    def get_person_profile(self, profile_id: str) -> Optional[PersonProfile]:
        """
        Retrieve a person profile by ID
        
        Args:
            profile_id: ID of the profile to retrieve
            
        Returns:
            PersonProfile object or None if not found
        """
        try:
            result = self.collection.get(ids=[profile_id])
            
            if not result['ids']:
                return None
            
            metadata = result['metadatas'][0]
            document = result['documents'][0]
            
            return PersonProfile(
                id=profile_id,
                name=metadata['name'],
                description=document,
                age=metadata.get('age'),
                location=metadata.get('location'),
                created_at=datetime.fromisoformat(metadata['created_at'])
            )
        
        except Exception as e:
            print(f"Error retrieving person profile: {e}")
            return None
    
    def search_similar_profiles(self, query_description: str, limit: int = 5, exclude_id: str = None) -> List[PersonProfileResponse]:
        """
        Search for similar profiles based on description similarity
        
        Args:
            query_description: Description to search for
            limit: Maximum number of results to return
            exclude_id: ID to exclude from results
            
        Returns:
            List of PersonProfileResponse objects with similarity scores
        """
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_service.generate_embedding(query_description)
            
            # Prepare where clause for exclusion
            where_clause = None
            if exclude_id:
                where_clause = {"id": {"$ne": exclude_id}}
            
            # Search for similar profiles
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=limit + (1 if exclude_id else 0),  # Get extra in case we need to exclude one
                where=where_clause,
                include=['documents', 'metadatas', 'distances']
            )
            
            # Process results
            similar_profiles = []
            
            for i, (distance, document, metadata, profile_id) in enumerate(zip(
                results['distances'][0],
                results['documents'][0],
                results['metadatas'][0],
                results['ids'][0]
            )):
                # Skip excluded ID if it appears in results
                if exclude_id and profile_id == exclude_id:
                    continue
                
                # Convert distance to similarity score (ChromaDB returns distances, we want similarities)
                similarity_score = 1.0 - distance
                
                profile_response = PersonProfileResponse(
                    id=profile_id,
                    name=metadata['name'],
                    description=document,
                    age=metadata.get('age'),
                    location=metadata.get('location'),
                    created_at=datetime.fromisoformat(metadata['created_at']),
                    similarity_score=similarity_score
                )
                
                similar_profiles.append(profile_response)
                
                # Stop if we have enough results
                if len(similar_profiles) >= limit:
                    break
            
            return similar_profiles
        
        except Exception as e:
            print(f"Error searching similar profiles: {e}")
            raise
    
    def get_all_profiles(self, limit: int = 100) -> List[PersonProfile]:
        """
        Get all profiles from the database
        
        Args:
            limit: Maximum number of profiles to return
            
        Returns:
            List of PersonProfile objects
        """
        try:
            results = self.collection.get(limit=limit, include=['documents', 'metadatas'])
            
            profiles = []
            for i, (document, metadata, profile_id) in enumerate(zip(
                results['documents'],
                results['metadatas'],
                results['ids']
            )):
                profile = PersonProfile(
                    id=profile_id,
                    name=metadata['name'],
                    description=document,
                    age=metadata.get('age'),
                    location=metadata.get('location'),
                    created_at=datetime.fromisoformat(metadata['created_at'])
                )
                profiles.append(profile)
            
            return profiles
        
        except Exception as e:
            print(f"Error getting all profiles: {e}")
            raise
    
    def delete_person_profile(self, profile_id: str) -> bool:
        """
        Delete a person profile by ID
        
        Args:
            profile_id: ID of the profile to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            self.collection.delete(ids=[profile_id])
            print(f"Deleted person profile with ID: {profile_id}")
            return True
        
        except Exception as e:
            print(f"Error deleting person profile: {e}")
            return False
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            count = self.collection.count()
            return {
                "total_profiles": count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            print(f"Error getting collection stats: {e}")
            return {"error": str(e)}
