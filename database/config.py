"""
Configuration for ClairOS Qdrant Database
"""

# Qdrant Connection
QDRANT_URL = "https://5d7c76fd-3740-4b18-bb00-195dfbc57e7a.us-east4-0.gcp.cloud.qdrant.io:6333"  # From your dashboard
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwiZXhwIjoxNzc3MTQxNzI3fQ.clxY8AxlgV5Dj9qagRh4RbtkZF4MyJuNclzkaf6lxxw"
COLLECTION_NAME = "clairos_email_chunks"

# Embedding Model (replace with Qwen3-Embedding-0.6B later [1])
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Temporary for testing
EMBEDDING_DIM = 384  # Update when you switch to Qwen3