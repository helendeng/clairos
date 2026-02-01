"""
Comprehensive test cases for ClairOS database
Covers all 11 domains and 27 subdomains per project requirements [1]
"""

# Test cases organized by domain and subdomain
# Format matches your updated chunk structure with integer chunk_id

TEST_CHUNKS = {
    "PII": {
        "Direct Identifiers": [
            {
                "chunk_id": 1,
                "domain": "PII",
                "subdomain": "Direct Identifiers",
                "text": "Employee SSN: [REDACTED]. Date of birth: [REDACTED]. Passport number [REDACTED].",
                "source": {
                    "email_id": "pii_direct_001",
                    "cc": "hr@company.com",
                    "bcc": "",
                    "from": "admin@company.com",
                    "subject": "Employee Verification",
                    "timestamp": "2026-01-10"
                }
            },
            {
                "chunk_id": 2,
                "domain": "PII",
                "subdomain": "Direct Identifiers",
                "text": "Driver's license number for David Smith: [REDACTED]. Home address: [REDACTED].",
                "source": {
                    "email_id": "pii_direct_002",
                    "cc": "",
                    "bcc": "",
                    "from": "facilities@company.com",
                    "subject": "Parking Pass Application",
                    "timestamp": "2026-01-11"
                }
            }
        ],
        "Contact Identifiers": [
            {
                "chunk_id": 1,
                "domain": "PII",
                "subdomain": "Contact Identifiers",
                "text": "Personal phone: [REDACTED]. Personal email: [REDACTED].",
                "source": {
                    "email_id": "pii_contact_001",
                    "cc": "",
                    "bcc": "",
                    "from": "employee@company.com",
                    "subject": "Emergency Contact Update",
                    "timestamp": "2026-01-12"
                }
            }
        ],
        "Financial Identifiers": [
            {
                "chunk_id": 1,
                "domain": "PII",
                "subdomain": "Financial Identifiers",
                "text": "Bank account for direct deposit: [REDACTED]. Routing number: [REDACTED].",
                "source": {
                    "email_id": "pii_financial_001",
                    "cc": "payroll@company.com",
                    "bcc": "",
                    "from": "employee@company.com",
                    "subject": "Payroll Setup",
                    "timestamp": "2026-01-13"
                }
            }
        ]
    },
    
    "HR": {
        "All_HR": [
            {
                "chunk_id": 1,
                "domain": "HR",
                "subdomain": "All_HR",
                "text": "Performance review scheduled for Q1. Discussion of salary adjustment pending.",
                "source": {
                    "email_id": "hr_001",
                    "cc": "",
                    "bcc": "",
                    "from": "hr@company.com",
                    "subject": "Annual Review Notice",
                    "timestamp": "2026-01-14"
                }
            },
            {
                "chunk_id": 2,
                "domain": "HR",
                "subdomain": "All_HR",
                "text": "Disciplinary action recorded. Employee counseling session notes attached.",
                "source": {
                    "email_id": "hr_002",
                    "cc": "manager@company.com",
                    "bcc": "",
                    "from": "hr@company.com",
                    "subject": "Employee Relations Matter",
                    "timestamp": "2026-01-15"
                }
            }
        ]
    },
    
    "Legal": {
        "Litigation Sensitive": [
            {
                "chunk_id": 1,
                "domain": "Legal",
                "subdomain": "Litigation Sensitive",
                "text": "Pending lawsuit regarding Atlas project delays. Attorney-client privileged.",
                "source": {
                    "email_id": "legal_litigation_001",
                    "cc": "counsel@company.com",
                    "bcc": "",
                    "from": "legal@company.com",
                    "subject": "PRIVILEGED: Atlas Litigation",
                    "timestamp": "2026-01-16"
                }
            }
        ],
        "Compliance & Regulatory": [
            {
                "chunk_id": 1,
                "domain": "Legal",
                "subdomain": "Compliance & Regulatory",
                "text": "Environmental permit compliance review due by March 1st per EPA regulations.",
                "source": {
                    "email_id": "legal_compliance_001",
                    "cc": "project@company.com",
                    "bcc": "",
                    "from": "compliance@company.com",
                    "subject": "EPA Compliance Deadline",
                    "timestamp": "2026-01-17"
                }
            }
        ],
        "Contractual": [
            {
                "chunk_id": 1,
                "domain": "Legal",
                "subdomain": "Contractual",
                "text": "Vendor contract renewal terms under negotiation. NDA restrictions apply.",
                "source": {
                    "email_id": "legal_contract_001",
                    "cc": "procurement@company.com",
                    "bcc": "",
                    "from": "legal@company.com",
                    "subject": "Contract Renewal - Confidential",
                    "timestamp": "2026-01-18"
                }
            }
        ],
        "Privileged Communications": [
            {
                "chunk_id": 1,
                "domain": "Legal",
                "subdomain": "Privileged Communications",
                "text": "Attorney work product regarding regulatory strategy. Do not forward.",
                "source": {
                    "email_id": "legal_privileged_001",
                    "cc": "",
                    "bcc": "",
                    "from": "attorney@lawfirm.com",
                    "subject": "PRIVILEGED: Legal Strategy",
                    "timestamp": "2026-01-19"
                }
            }
        ]
    },
    
    "Security": {
        "Operational Security": [
            {
                "chunk_id": 1,
                "domain": "Security",
                "subdomain": "Operational Security",
                "text": "New access codes for data center. Effective immediately: [REDACTED].",
                "source": {
                    "email_id": "security_ops_001",
                    "cc": "it@company.com",
                    "bcc": "",
                    "from": "security@company.com",
                    "subject": "Updated Security Codes",
                    "timestamp": "2026-01-20"
                }
            }
        ],
        "Security Behavioral Data": [
            {
                "chunk_id": 1,
                "domain": "Security",
                "subdomain": "Security Behavioral Data",
                "text": "Unusual login pattern detected from employee account. Investigation ongoing.",
                "source": {
                    "email_id": "security_behavior_001",
                    "cc": "soc@company.com",
                    "bcc": "",
                    "from": "security@company.com",
                    "subject": "Security Alert",
                    "timestamp": "2026-01-21"
                }
            }
        ]
    },
    
    "Strategic Confidential": {
        "Business Strategy": [
            {
                "chunk_id": 1,
                "domain": "Strategic Confidential",
                "subdomain": "Business Strategy",
                "text": "Q2 acquisition target identified. Board approval pending. HIGHLY CONFIDENTIAL.",
                "source": {
                    "email_id": "strategy_001",
                    "cc": "ceo@company.com",
                    "bcc": "",
                    "from": "strategy@company.com",
                    "subject": "CONFIDENTIAL: M&A Opportunity",
                    "timestamp": "2026-01-22"
                }
            }
        ]
    },
    
    "Research & Development": {
        "Technical R&D": [
            {
                "chunk_id": 1,
                "domain": "Research & Development",
                "subdomain": "Technical R&D",
                "text": "New turbine blade design shows 15% efficiency improvement in testing. Patent pending.",
                "source": {
                    "email_id": "rd_tech_001",
                    "cc": "engineering@company.com",
                    "bcc": "",
                    "from": "rnd@company.com",
                    "subject": "Turbine Innovation - Confidential",
                    "timestamp": "2026-01-23"
                }
            }
        ],
        "Scientific and IP R&D": [
            {
                "chunk_id": 1,
                "domain": "Research & Development",
                "subdomain": "Scientific and IP R&D",
                "text": "Patent application drafted for solar panel coating technology. Prior art search complete.",
                "source": {
                    "email_id": "rd_ip_001",
                    "cc": "legal@company.com",
                    "bcc": "",
                    "from": "rnd@company.com",
                    "subject": "Patent Filing - Solar Tech",
                    "timestamp": "2026-01-24"
                }
            }
        ]
    },
    
    "Financial": {
        "Accounting": [
            {
                "chunk_id": 1,
                "domain": "Financial",
                "subdomain": "Accounting",
                "text": "Q4 revenue projections revised downward by 8%. Earnings call scheduled.",
                "source": {
                    "email_id": "finance_accounting_001",
                    "cc": "cfo@company.com",
                    "bcc": "",
                    "from": "accounting@company.com",
                    "subject": "Q4 Forecast Update",
                    "timestamp": "2026-01-25"
                }
            }
        ],
        "Company Financial Strategy": [
            {
                "chunk_id": 1,
                "domain": "Financial",
                "subdomain": "Company Financial Strategy",
                "text": "Board approved $50M capital raise. Term sheet negotiations with investors ongoing.",
                "source": {
                    "email_id": "finance_strategy_001",
                    "cc": "board@company.com",
                    "bcc": "",
                    "from": "cfo@company.com",
                    "subject": "CONFIDENTIAL: Funding Round",
                    "timestamp": "2026-01-26"
                }
            }
        ]
    },
    
    "Operational": {
        "Project Metadata": [
            {
                "chunk_id": 1,
                "domain": "Operational",
                "subdomain": "Project Metadata",
                "text": "Atlas project timeline extended to Q3 2027. Stakeholder notification required.",
                "source": {
                    "email_id": "ops_project_001",
                    "cc": "team@company.com",
                    "bcc": "",
                    "from": "pm@company.com",
                    "subject": "Atlas Timeline Update",
                    "timestamp": "2026-01-27"
                }
            },
            {
                "chunk_id": 2,
                "domain": "Operational",
                "subdomain": "Project Metadata",
                "text": "Environmental assessment for wind farm approved by state regulators.",
                "source": {
                    "email_id": "ops_project_002",
                    "cc": "permits@company.com",
                    "bcc": "",
                    "from": "regulatory@company.com",
                    "subject": "Permit Approval - Wind Project",
                    "timestamp": "2026-01-28"
                }
            }
        ],
        "Org-Structure Metadata": [
            {
                "chunk_id": 1,
                "domain": "Operational",
                "subdomain": "Org-Structure Metadata",
                "text": "Organizational restructure announced. Three departments merging into Energy Division.",
                "source": {
                    "email_id": "ops_org_001",
                    "cc": "all@company.com",
                    "bcc": "",
                    "from": "ceo@company.com",
                    "subject": "Org Structure Changes",
                    "timestamp": "2026-01-29"
                }
            }
        ],
        "System Operations": [
            {
                "chunk_id": 1,
                "domain": "Operational",
                "subdomain": "System Operations",
                "text": "Planned system maintenance window: February 10, 2am-6am EST. All services offline.",
                "source": {
                    "email_id": "ops_systems_001",
                    "cc": "it@company.com",
                    "bcc": "",
                    "from": "ops@company.com",
                    "subject": "Maintenance Notice",
                    "timestamp": "2026-01-30"
                }
            }
        ]
    },
    
    "Vendor": {
        "Sensitive Vendor Documents": [
            {
                "chunk_id": 1,
                "domain": "Vendor",
                "subdomain": "Sensitive Vendor Documents",
                "text": "Vendor pricing proposal for turbine components. NDA-protected terms included.",
                "source": {
                    "email_id": "vendor_sensitive_001",
                    "cc": "procurement@company.com",
                    "bcc": "",
                    "from": "vendor@supplier.com",
                    "subject": "CONFIDENTIAL: Pricing Proposal",
                    "timestamp": "2026-01-31"
                }
            }
        ],
        "Support & Escalation": [
            {
                "chunk_id": 1,
                "domain": "Vendor",
                "subdomain": "Support & Escalation",
                "text": "Critical support ticket escalated to vendor engineering team. Resolution ETA 48 hours.",
                "source": {
                    "email_id": "vendor_support_001",
                    "cc": "it@company.com",
                    "bcc": "",
                    "from": "support@vendor.com",
                    "subject": "Escalation: Ticket #12345",
                    "timestamp": "2026-02-01"
                }
            }
        ],
        "Vendor Metadata": [
            {
                "chunk_id": 1,
                "domain": "Vendor",
                "subdomain": "Vendor Metadata",
                "text": "Vendor contact updated: New account manager assigned to our account.",
                "source": {
                    "email_id": "vendor_meta_001",
                    "cc": "procurement@company.com",
                    "bcc": "",
                    "from": "vendor@supplier.com",
                    "subject": "Account Manager Change",
                    "timestamp": "2026-02-02"
                }
            }
        ]
    },
    
    "Scheduling": {
        "All_Schedule": [
            {
                "chunk_id": 1,
                "domain": "Scheduling",
                "subdomain": "All_Schedule",
                "text": "Meeting set for 3pm PST / 6pm EST tomorrow to review onboarding.",
                "source": {
                    "email_id": "sch_email_001",
                    "cc": "team@company.com",
                    "bcc": "",
                    "from": "manager@company.com",
                    "subject": "Onboarding meeting",
                    "timestamp": "2026-01-18"
                }
            },
        ]
    }
}