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


# SUBDOMAIN as Primary Classification (27 separate blocks)
# Domain is metadata only, SUBDOMAIN is the main searchable tag
SUBDOMAINS = [
    # PII
    "Direct Identifiers",
    "Contact Identifiers", 
    "Financial Identifiers",
    
    # HR
    "All_HR",  # HR subdomain
    
    # Legal
    "Litigation Sensitive",
    "Compliance & Regulatory",
    "Contractual",
    "Privileged Communications",
    
    # Security
    "Operational Security",
    "Security Behavioral Data",
    
    # Strategic Confidential
    "Business Strategy",
    
    # Research & Development
    "Technical R&D",
    "Scientific and IP R&D",
    
    # Financial
    "Accounting",
    "Company Financial Strategy",
    
    # Operational
    "Project Metadata",
    "Org-Structure Metadata",
    "System Operations",
    
    # Vendor
    "Sensitive Vendor Documents",
    "Support & Escalation",
    "Vendor Metadata",
    
    # Scheduling
    "All_Schedule",  # Scheduling subdomain (note: duplicate name with HR, but different domain)
    
    # Personal Life
    "Health Disclosures",
    "Crisis/Sensitive Content"
]

# Domain mapping (kept as metadata for context only)
SUBDOMAIN_TO_DOMAIN = {
    "Direct Identifiers": "PII",
    "Contact Identifiers": "PII",
    "Financial Identifiers": "PII",
    "All_HR": "HR",  # Note: This will be overwritten by Scheduling's "All"
    "Litigation Sensitive": "Legal",
    "Compliance & Regulatory": "Legal",
    "Contractual": "Legal",
    "Privileged Communications": "Legal",
    "Operational Security": "Security",
    "Security Behavioral Data": "Security",
    "Business Strategy": "Strategic Confidential",
    "Technical R&D": "Research & Development",
    "Scientific and IP R&D": "Research & Development",
    "Accounting": "Financial",
    "Company Financial Strategy": "Financial",
    "Project Metadata": "Operational",
    "Org-Structure Metadata": "Operational",
    "System Operations": "Operational",
    "Sensitive Vendor Documents": "Vendor",
    "Support & Escalation": "Vendor",
    "Vendor Metadata": "Vendor",
    "All_Schedule": "Scheduling",  # Commented: conflicts with HR
    "Health Disclosures": "Personal Life",
    "Crisis/Sensitive Content": "Personal Life"
}