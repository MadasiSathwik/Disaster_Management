import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration loaded from environment variables."""

    # Database configuration (Neon/PostgreSQL)
    # e.g. DATABASE_URL=postgresql://user:pass@host:port/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

    # Pagination defaults - TODO: make configurable
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))

    # TODO: Add caching configuration (Redis/Memcached)
    # TODO: Add mail server configuration
    # TODO: Add other third party service credentials
