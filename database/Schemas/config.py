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
    #Raw emails
    "Raw Email",
    # PII
    "Direct Identifier",
    "Contact Identifier",
    "Financial Identifier",

    # HR
    "HR",

    # Legal
    "Litigation Sensitive",
    "Compliance&Regulatory",
    "Contractual",
    "Privileged_Communications",

    # Security
    "Operational_Security",
    "Behavioral Data",

    # Strategic Confidential
    "Business_Strategy",

    # Research & Development
    "Technical",
    "Scientific_&_IP",

    # Financial
    "Accounting",
    "Financial_Strategy",

    # Operational
    "Project_Metadata",
    "Org_Structure_Metadata",
    "System_Operations",

    # Vendor
    "Sensitive_Vendor_Docs",
    "Support_&_Escalation",
    "Vendor_Metadata",

    # Scheduling
    "Scheduling",

    # Personal
    "Health_Disclosures",
    "Crisis_&_Sensitive",

    # Other
    "Other",
]

SUBDOMAIN_TO_DOMAIN = {
    "Raw Email": "Raw Email",
    "Direct Identifier": "PII",
    "Contact Identifier": "PII",
    "Financial Identifier": "PII",
    "HR": "HR",
    "Litigation Sensitive": "Legal",
    "Compliance&Regulatory": "Legal",
    "Contractual": "Legal",
    "Privileged_Communications": "Legal",
    "Operational_Security": "Security",
    "Behavioral Data": "Security",
    "Business_Strategy": "Strategic Confidential",
    "Technical": "R&D",
    "Scientific_&_IP": "R&D",
    "Accounting": "Financial",
    "Financial_Strategy": "Financial",
    "Project_Metadata": "Operational",
    "Org_Structure_Metadata": "Operational",
    "System_Operations": "Operational",
    "Sensitive_Vendor_Docs": "Vendor",
    "Support_&_Escalation": "Vendor",
    "Vendor_Metadata": "Vendor",
    "Scheduling": "Scheduling",
    "Health_Disclosures": "Personal",
    "Crisis_&_Sensitive": "Personal",
    "Other": "Other",
}