"""Neo4j database connection management."""
from neo4j import GraphDatabase, Driver
from typing import Optional
import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


class Neo4jClient:
    """Singleton Neo4j driver manager."""

    _driver: Optional[Driver] = None

    @classmethod
    def get_driver(cls) -> Driver:
        """
        Get or create Neo4j driver instance.

        Returns:
            Neo4j driver instance
        """
        if cls._driver is None:
            cls._driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password)
            )
        return cls._driver

    @classmethod
    def close_driver(cls):
        """Close the Neo4j driver connection."""
        if cls._driver is not None:
            cls._driver.close()
            cls._driver = None

    @classmethod
    def test_connection(cls) -> bool:
        """
        Test Neo4j connection.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            driver = cls.get_driver()
            with driver.session() as session:
                result = session.run("RETURN 1 as test")
                return result.single()["test"] == 1
        except Exception as e:
            print(f"Neo4j connection test failed: {e}")
            return False


# Convenience functions for common operations
def get_driver() -> Driver:
    """Get Neo4j driver instance."""
    return Neo4jClient.get_driver()


def test_connection() -> bool:
    """Test Neo4j connection."""
    return Neo4jClient.test_connection()
