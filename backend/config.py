"""Configuration management for Knowledge Graph backend."""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Anthropic API
    anthropic_api_key: str

    # Neo4j Database
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str

    # FastAPI
    app_name: str = "Knowledge Graph API"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False
        # Map environment variable names to field names
        fields = {
            'anthropic_api_key': {'env': 'ANTHROPIC_API_KEY'},
            'neo4j_uri': {'env': 'NEO4J_URI'},
            'neo4j_user': {'env': 'NEO4J_USER'},
            'neo4j_password': {'env': 'NEO4J_PASSWORD'},
        }


# Load environment variables from .env file
load_dotenv()

# Create global settings instance
settings = Settings()
