"""
Database configuration and setup.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os


class DatabaseConfig:
    """Database configuration class."""

    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite+aiosqlite:///./tickets.db"
        )

    @property
    def engine_kwargs(self):
        """Get engine configuration based on database type."""
        if "sqlite" in self.database_url:
            return {
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            }
        return {}

    def create_engine(self):
        """Create async database engine."""
        return create_async_engine(
            self.database_url,
            echo=False,  # Set to True for debugging
            **self.engine_kwargs
        )

    def create_session_factory(self, engine):
        """Create session factory."""
        return sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
