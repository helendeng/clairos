# This will set the category to (domain, subcategory) pipeline and dataclass

TAXONOMY = {
    "financial.credit_card": {"domain": "PII", "subdomain": "Financial"},
    "taxpayer.ein": {"domain": "PII", "subdomain": "Tax IDs"},
    "security.api_key": {"domain": "Security", "subdomain": "Secrets"},

    ########################## PII ############################
    ### Direct Identifiers
    "direct_ID.SSN": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Passport_Number": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Visa_Number": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Medical_Device_Data": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Birthday": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Drivers_License": {"domain": "PII", "subdomain": "Direct Identifier"},
    "direct_ID.Geographical_ID": {"domain": "PII", "subdomain": "Direct Identifier"},

    ### Contact Identifiers
    "contact_ID.Personal_Address": {"domain": "PII", "subdomain": "Contact Identifier"},
    "contact_ID.Personal_Phone": {"domain": "PII", "subdomain": "Contact Identifier"},
    "contact_ID.Personal_Email": {"domain": "PII", "subdomain": "Contact Identifier"},
    "contact_ID.Employee_ID": {"domain": "PII", "subdomain": "Contact Identifier"},

    ### Financial Identifiers 
    "financial_ID.Personal_Credit_Card": {"domain": "PII", "subdomain": "Financial Identifier"},
    "financial_ID.Bank_Routing_Number": {"domain": "PII", "subdomain": "Financial Identifier"},
    "financial_ID.Taxpayer_ID": {"domain": "PII", "subdomain": "Financial Identifier"},


    ########################## HR ############################
    "HR.External_Credit_Card": {"domain": "HR", "subdomain": "HR"},
    "HR.External_Bank_Information": {"domain": "HR", "subdomain": "HR"},
    "HR.Performance_Reviews": {"domain": "HR", "subdomain": "HR"},
    "HR.Internal_Disputes": {"domain": "HR", "subdomain": "HR"},


    ########################## Legal ############################
    ### Litigation-Sensitive
    "litigation_sensitive.legal_disputes": {"domain": "Legal", "subdomain": "Litigation Sensitive"},
    "litigation_sensitive.Notice_of_Claims": {"domain": "Legal", "subdomain": "Litigation Sensitive"},
    "litigation_sensitive.Pre_Litigation_Discussions": {"domain": "Legal", "subdomain": "Litigation Sensitive"},

    ### Compliance and Regulatory
    "compliance&regulatory.SOX_Compliance": {"domain": "Legal", "subdomain": "Compliance&Regulatory"},
    "compliance&regulatory.Safety_Compliance": {"domain": "Legal", "subdomain": "Compliance&Regulatory"},
    "compliance&regulatory.Reporting_Obligations": {"domain": "Legal", "subdomain": "Compliance&Regulatory"},

    ### Contractual
    "contractual.NDA": {"domain": "Legal", "subdomain": "Contractual"},
    "contractual.Customer_Agreements": {"domain": "Legal", "subdomain": "Contractual"},
    "contractual.Vendor_Agreements": {"domain": "Legal", "subdomain": "Contractual"},

    ### Privileged Communications
    "privileged_communications.Messages_to&from_counsel": {"domain": "Legal", "subdomain": "Privileged_Communications"},
    "privileged_communications.Internal_Legal_Advice": {"domain": "Legal", "subdomain": "Privileged_Communications"},


    ########################## Security ############################
    ### Operational Security
    "operational_security.System_Diagrams": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Deployment_URLs": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Internal_IP_Address": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.VPN_Credentials": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Encryption_Keys": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.MFA_Recovery_Codes": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Admin_Credentials": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.API_Key": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Secret_Link": {"domain": "Security", "subdomain": "Operational_Security"},
    "operational_security.Tokens": {"domain": "Security", "subdomain": "Operational_Security"},

    ### Security Behavioral Data
    "behavioral.Audit_Log": {"domain": "Security", "subdomain": "Behavioral Data"},
    "behavioral.Failed_login_events": {"domain": "Security", "subdomain": "Behavioral Data"},
    "behavioral.Incident_Postmortems": {"domain": "Security", "subdomain": "Behavioral Data"},


    ########################## Strategic Confidential ############################
    ### Company Level Business Strategy
    "Strategic.M&A": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Strategic.Market_Expansion": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Strategic.Pricing_Models": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Strategic.Customer_Acquisition": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Strategic.Competitive_Analysis": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Strategic.Board_Communications": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},


    ########################## R&D ############################
    ### Technical
    "R&D.Technical.Experiments": {"domain": "R&D", "subdomain": "Technical"},
    "R&D.Technical.Algorithms": {"domain": "R&D", "subdomain": "Technical"},
    "R&D.Technical.Models": {"domain": "R&D", "subdomain": "Technical"},
    "R&D.Technical.Prototypes": {"domain": "R&D", "subdomain": "Technical"},
    "Technical_R&D.Hardware_Specifications": {"domain": "R&D", "subdomain": "Technical"},

    ### Scientific and IP
    "R&D.IP.Patentable_Ideas": {"domain": "R&D", "subdomain": "Scientific_&_IP"},
    "R&D.IP.Proprietary_Formulas": {"domain": "R&D", "subdomain": "Scientific_&_IP"},
    "Scientific_&_IP.Novel_Engineering_Concepts": {"domain": "R&D", "subdomain": "Scientific_&_IP"},


    ########################## Financial ############################
    ### Accounting
    "Accounting.Company_Credit_Card": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Company_Bank_Account_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Tax_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.W9_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.1099_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Payroll_Attachments": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Salary_Information": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Financial.Accounting.Salary_Negotiations": {"domain": "Financial", "subdomain": "Accounting"},
    "Financial.Accounting.Firing_Hiring": {"domain": "Financial", "subdomain": "Accounting"},
    "Accounting.Hiring_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Financial.Accounting.Bonuses": {"domain": "Financial", "subdomain": "Accounting"},
    "Accounting.Raise_Info": {"domain": "Financial", "subdomain": "Accounting"}, 

    ### Financial Strategy
    "Financial.Strategy.Budget_Forecasting": {"domain": "Financial", "subdomain": "Financial_Strategy"},
    "Financial.Strategy.Revenue_Projections": {"domain": "Financial", "subdomain": "Financial_Strategy"},
    "Financial_Strategy.Financial_Risk_Models": {"domain": "Financial", "subdomain": "Financial_Strategy"},
    "Financial.Strategy.Investment_Strategies": {"domain": "Financial", "subdomain": "Financial_Strategy"},
    "Financial_Strategy.Pricing_Models": {"domain": "Financial", "subdomain": "Financial_Strategy"},


    ########################## Operational ############################
    ### Project Metadata
    "Project_Metadata.Project_Deadlines": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Deliverables": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Handoff_Notes": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Operational.Project.Progress_Updates": {"domain": "Operational", "subdomain": "Project_Metadata"},
    "Operational.Project.Technical_Blockers": {"domain": "Operational", "subdomain": "Project_Metadata"},

    ### Organization Structure Metadata
    "Org_Structure_Metadata.Coworker_Name": {"domain": "Operational", "subdomain": "Org_Structure_Metadata"}, 
    "Org_Structure_Metadata.Coworker_Email": {"domain": "Operational", "subdomain": "Org_Structure_Metadata"}, 
    "Org_Structure_Metadata.Roles": {"domain": "Operational", "subdomain": "Org_Structure_Metadata"}, 
    "Org_Structure_Metadata.Team_Transition": {"domain": "Operational", "subdomain": "Org_Structure_Metadata"}, 
    "Org_Structure_Metadata.Onboarding_Notes": {"domain": "Operational", "subdomain": "Org_Structure_Metadata"}, 

    ### System Operations
    "System_Operations.Maintenance_Window": {"domain": "Operational", "subdomain": "System_Operations"}, 
    "System_Operations.Deployment_Schedule": {"domain": "Operational", "subdomain": "System_Operations"}, 
    "System_Operations.Production_Alerts": {"domain": "Operational", "subdomain": "System_Operations"}, 
    "System_Operations.Internal_System_ID": {"domain": "Operational", "subdomain": "System_Operations"}, 


    ########################## Vendor ############################
    ### Sensitive Vendor Documents
    "Sensitive_Vendor_Docs.Invoices": {"domain": "Vendor", "subdomain": "Sensitive_Vendor_Docs"}, 
    "Sensitive_Vendor_Docs.Contracts": {"domain": "Vendor", "subdomain": "Sensitive_Vendor_Docs"}, 
    "Sensitive_Vendor_Docs.Statements_of_Work": {"domain": "Vendor", "subdomain": "Sensitive_Vendor_Docs"}, 

    ### Support Tickets and Escalation
    "Support_&_Escalation.Customer_Success_Hotline": {"domain": "Vendor", "subdomain": "Support_&_Escalation"}, 
    "Support_&_Escalation.Support_Escalation_Contact": {"domain": "Vendor", "subdomain": "Support_&_Escalation"}, 

    ### Vendor Metadata
    "Vendor_Metadata.Vendor_Address": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 
    "Vendor_Metadata.Vendor_Email": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 
    "Vendor_Metadata.Vendor_Name": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 
    "Vendor_Metadata.Contractor_Address": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 
    "Vendor_Metadata.Contractor_Email": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 
    "Vendor_Metadata.Contractor_Name": {"domain": "Vendor", "subdomain": "Vendor_Metadata"}, 


    ########################## Scheduling ############################
    "Scheduling.Recurrences": {"domain": "Scheduling", "subdomain": "Scheduling"}, 
    "Scheduling.Travel_Itineraries": {"domain": "Scheduling", "subdomain": "Scheduling"}, 
    "Scheduling.Time_Zones": {"domain": "Scheduling", "subdomain": "Scheduling"}, 
    "Scheduling.Cross_Team_Coordination": {"domain": "Scheduling", "subdomain": "Scheduling"}, 
    "Scheduling.Meeting_Moved_Notices": {"domain": "Scheduling", "subdomain": "Scheduling"}, 

    ########################## Personal Life ############################
    ### Health Disclosures
    "Personal_Life.Health_Disclosures": {"domain": "Personal", "subdomain": "Health_Disclosures"},

    ### Crisis/Sensitive Content 
    "Crisis_&_Sensitive.Breakups": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"}, 
    "Crisis_&_Sensitive.Family_Emergency": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"}, 
    "Personal_Life.Crisis_Content": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"},

    ########################## Other ############################
    "Other.Other": {"domain": "Other", "subdomain": "Other"},
}


###############################################################################
########################## RAG Domain Routing Map #############################
# Maps every taxonomy key → list of FAISS index basenames (without extension).
# Names must exactly match filenames in rag_demo4/indexes/ (e.g. "all_hr" →
# "all_hr.faiss" / "all_hr.chunks.json").
# Use [] for subdomains that should NOT be served via RAG (sensitive PII, etc).
LABEL_TO_RAG_DOMAIN: dict[str, list[str]] = {

    # ── PII / Direct Identifiers — redacted, no RAG index ─────────────────
    "direct_ID.SSN":                                        [],
    "direct_ID.Passport_Number":                            [],
    "direct_ID.Visa_Number":                                [],
    "direct_ID.Medical_Device_Data":                        [],
    "direct_ID.Birthday":                                   [],
    "direct_ID.Drivers_License":                            [],
    "direct_ID.Geographical_ID":                            [],

    # ── PII / Contact Identifiers ──────────────────────────────────────────
    "contact_ID.Personal_Address":                          ["contact_identifiers"],
    "contact_ID.Personal_Phone":                            ["contact_identifiers"],
    "contact_ID.Personal_Email":                            ["contact_identifiers"],
    "contact_ID.Employee_ID":                               ["contact_identifiers"],

    # ── PII / Financial Identifiers — sensitive PII, no RAG index ─────────
    "financial_ID.Personal_Credit_Card":                    [],
    "financial_ID.Bank_Routing_Number":                     [],
    "financial_ID.Taxpayer_ID":                             [],
    "financial.credit_card":                                [],
    "taxpayer.ein":                                         [],
    "security.api_key":                                     ["operational_security"],

    # ── HR ─────────────────────────────────────────────────────────────────
    "HR.External_Credit_Card":                              ["all_hr"],
    "HR.External_Bank_Information":                         ["all_hr"],
    "HR.Performance_Reviews":                               ["all_hr"],
    "HR.Internal_Disputes":                                 ["all_hr"],

    # ── Legal / Litigation Sensitive ───────────────────────────────────────
    "litigation_sensitive.legal_disputes":                  ["litigation_sensitive"],
    "litigation_sensitive.Notice_of_Claims":                ["litigation_sensitive"],
    "litigation_sensitive.Pre_Litigation_Discussions":      ["litigation_sensitive"],

    # ── Legal / Compliance & Regulatory ───────────────────────────────────
    "compliance&regulatory.SOX_Compliance":                 ["compliance_and_regulatory"],
    "compliance&regulatory.Safety_Compliance":              ["compliance_and_regulatory"],
    "compliance&regulatory.Reporting_Obligations":          ["compliance_and_regulatory"],

    # ── Legal / Contractual ────────────────────────────────────────────────
    "contractual.NDA":                                      ["contractual"],
    "contractual.Customer_Agreements":                      ["contractual"],
    "contractual.Vendor_Agreements":                        ["contractual"],

    # ── Legal / Privileged Communications ─────────────────────────────────
    "privileged_communications.Messages_to&from_counsel":   ["litigation_sensitive"],
    "privileged_communications.Internal_Legal_Advice":      ["litigation_sensitive"],

    # ── Security / Operational Security ───────────────────────────────────
    "operational_security.System_Diagrams":                 ["operational_security"],
    "operational_security.Deployment_URLs":                 ["operational_security"],
    "operational_security.Internal_IP_Address":             ["operational_security"],
    "operational_security.VPN_Credentials":                 ["operational_security"],
    "operational_security.Encryption_Keys":                 ["operational_security"],
    "operational_security.MFA_Recovery_Codes":              ["operational_security"],
    "operational_security.Admin_Credentials":               ["operational_security"],
    "operational_security.API_Key":                         ["operational_security"],
    "operational_security.Secret_Link":                     ["operational_security"],
    "operational_security.Tokens":                          ["operational_security"],

    # ── Security / Behavioral Data ─────────────────────────────────────────
    "behavioral.Audit_Log":                                 ["operational_security"],
    "behavioral.Failed_login_events":                       ["operational_security"],
    "behavioral.Incident_Postmortems":                      ["operational_security"],

    # ── Strategic ──────────────────────────────────────────────────────────
    "Strategic.M&A":                                        ["business_strategy"],
    "Strategic.Market_Expansion":                           ["business_strategy"],
    "Strategic.Pricing_Models":                             ["business_strategy", "company_financial_strategy"],
    "Strategic.Customer_Acquisition":                       ["business_strategy"],
    "Strategic.Competitive_Analysis":                       ["business_strategy"],
    "Strategic.Board_Communications":                       ["business_strategy"],

    # ── R&D / Technical ────────────────────────────────────────────────────
    "R&D.Technical.Experiments":                            ["technical_randd"],
    "R&D.Technical.Algorithms":                             ["technical_randd"],
    "R&D.Technical.Models":                                 ["technical_randd"],
    "R&D.Technical.Prototypes":                             ["technical_randd"],
    "Technical_R&D.Hardware_Specifications":                ["technical_randd"],

    # ── R&D / IP ───────────────────────────────────────────────────────────
    "R&D.IP.Patentable_Ideas":                              ["technical_randd"],
    "R&D.IP.Proprietary_Formulas":                          ["technical_randd"],
    "Scientific_&_IP.Novel_Engineering_Concepts":           ["technical_randd"],

    # ── Financial / Accounting ─────────────────────────────────────────────
    "Accounting.Company_Credit_Card":                       ["accounting"],
    "Accounting.Company_Bank_Account_Info":                 ["accounting"],
    "Accounting.Tax_Info":                                  ["accounting"],
    "Accounting.W9_Info":                                   ["accounting"],
    "Accounting.1099_Info":                                 ["accounting"],
    "Accounting.Payroll_Attachments":                       ["accounting"],
    "Accounting.Salary_Information":                        ["accounting"],
    "Financial.Accounting.Salary_Negotiations":             ["accounting"],
    "Financial.Accounting.Firing_Hiring":                   ["accounting"],
    "Accounting.Hiring_Info":                               ["accounting"],
    "Financial.Accounting.Bonuses":                         ["accounting"],
    "Accounting.Raise_Info":                                ["accounting"],

    # ── Financial / Strategy ───────────────────────────────────────────────
    "Financial.Strategy.Budget_Forecasting":                ["company_financial_strategy"],
    "Financial.Strategy.Revenue_Projections":               ["company_financial_strategy"],
    "Financial_Strategy.Financial_Risk_Models":             ["company_financial_strategy"],
    "Financial.Strategy.Investment_Strategies":             ["company_financial_strategy"],
    "Financial_Strategy.Pricing_Models":                    ["company_financial_strategy", "business_strategy"],

    # ── Operational / Project Metadata ─────────────────────────────────────
    "Project_Metadata.Project_Deadlines":                   ["project_metadata"],
    "Project_Metadata.Deliverables":                        ["project_metadata"],
    "Project_Metadata.Handoff_Notes":                       ["project_metadata"],
    "Operational.Project.Progress_Updates":                 ["project_metadata"],
    "Operational.Project.Technical_Blockers":               ["project_metadata"],

    # ── Operational / Org Structure ────────────────────────────────────────
    "Org_Structure_Metadata.Coworker_Name":                 ["orgstructure_metadata"],
    "Org_Structure_Metadata.Coworker_Email":                ["orgstructure_metadata"],
    "Org_Structure_Metadata.Roles":                         ["orgstructure_metadata"],
    "Org_Structure_Metadata.Team_Transition":               ["orgstructure_metadata"],
    "Org_Structure_Metadata.Onboarding_Notes":              ["orgstructure_metadata"],

    # ── Operational / System Operations ───────────────────────────────────
    "System_Operations.Maintenance_Window":                 ["system_operations"],
    "System_Operations.Deployment_Schedule":                ["system_operations"],
    "System_Operations.Production_Alerts":                  ["system_operations"],
    "System_Operations.Internal_System_ID":                 ["system_operations"],

    # ── Vendor ─────────────────────────────────────────────────────────────
    "Sensitive_Vendor_Docs.Invoices":                       ["vendor_metadata"],
    "Sensitive_Vendor_Docs.Contracts":                      ["vendor_metadata"],
    "Sensitive_Vendor_Docs.Statements_of_Work":             ["vendor_metadata"],
    "Support_&_Escalation.Customer_Success_Hotline":        ["vendor_metadata"],
    "Support_&_Escalation.Support_Escalation_Contact":      ["vendor_metadata"],
    "Vendor_Metadata.Vendor_Address":                       ["vendor_metadata"],
    "Vendor_Metadata.Vendor_Email":                         ["vendor_metadata"],
    "Vendor_Metadata.Vendor_Name":                          ["vendor_metadata"],
    "Vendor_Metadata.Contractor_Address":                   ["vendor_metadata"],
    "Vendor_Metadata.Contractor_Email":                     ["vendor_metadata"],
    "Vendor_Metadata.Contractor_Name":                      ["vendor_metadata"],

    # ── Scheduling ─────────────────────────────────────────────────────────
    "Scheduling.Recurrences":                               ["all_schedule"],
    "Scheduling.Travel_Itineraries":                        ["all_schedule"],
    "Scheduling.Time_Zones":                                ["all_schedule"],
    "Scheduling.Cross_Team_Coordination":                   ["all_schedule"],
    "Scheduling.Meeting_Moved_Notices":                     ["all_schedule"],

    # ── Personal / Health ──────────────────────────────────────────────────
    "Personal_Life.Health_Disclosures":                     ["health_disclosures"],

    # ── Personal / Crisis & Sensitive ──────────────────────────────────────
    "Crisis_&_Sensitive.Breakups":                          ["crisis_sensitive_content"],
    "Crisis_&_Sensitive.Family_Emergency":                  ["crisis_sensitive_content"],
    "Personal_Life.Crisis_Content":                         ["crisis_sensitive_content"],

    # ── Other ──────────────────────────────────────────────────────────────
    "Other.Other":                                          [],
}


###############################################################################
############################ Labels for Zero-Shot #############################
# The labels and their descriptions that will be fed into the Zero-Shot model
"""
1. HR: Performance Reviews, Internal Disputes
2. Strategic: M&A, Market expansion, Pricing models, Customer acquisition, Competitive Analysis, Board Communications
3. R&D.Technical: Experiments, Algorithms, Models, Prototypes
4. R&D.IP: Patentable ideas, Proprietary formulas
5. Financial.Accounting: Salary negotiations, Firing/hiring, Bonuses
6. Financial.Strategy: Budget forecasting, Revenue projections, Investment strategies
7. Operational.Project: Technical blockers, Progress updates
8. Personal Life: Health disclosures, Crisis content
"""

## We are tagging in groups, thus we need to split up the labels into groups of 10 each
ZERO_SHOT_LABEL_GROUPS = {
    #### Strategic and HR
    "Strategic_&_HR": {
        "Strategic.M&A": "Merger, acquisition, company purchase, or buyout discussion",
        "Strategic.Market_Expansion": "Market expansion plan, new geographic territory, or business growth strategy",
        "Strategic.Pricing_Models": "Pricing strategy, pricing model, or margin analysis",
        "Strategic.Customer_Acquisition": "Customer acquisition strategy, sales funnel, or user growth tactics",
        "Strategic.Competitive_Analysis": "Competitive analysis, competitor research, or market positioning study",
        "Strategic.Board_Communications": "Board of directors meeting, board-level decision, or executive leadership communication",
        "HR.Performance_Reviews": "Employee performance review, evaluation, or feedback discussion",
        "HR.Internal_Disputes": "Internal workplace conflict, disagreement, or dispute between employee",
    },

    #### Research and Development
    "R&D": {
        "R&D.Technical.Experiments": "Scientific experiment, technical test, or research trial",
        "R&D.Technical.Algorithms": "Algorithm design, computational method, or optimization technique",
        "R&D.Technical.Models": "Machine learning model, predictive model, or statistical modeling approach",
        "R&D.Technical.Prototypes": "Prototype development, proof of concept, or experimental design",
        "R&D.IP.Patentable_Ideas": "Patentable invention, patent application, or novel intellectual property",
        "R&D.IP.Proprietary_Formulas": "Proprietary formula, trade secret, or confidential technical method",
    },

    #### Financial
    "Financial": {
        "Financial.Accounting.Salary_Negotiations": "Salary negotiation, compensation discussion, or pay raise conversation",
        "Financial.Accounting.Firing_Hiring": "Employee termination, hiring decision, or staffing change",
        "Financial.Accounting.Bonuses": "Bonus payment, incentive compensation, or performance-based reward",
        "Financial.Strategy.Budget_Forecasting": "Budget forecast, financial planning, or spending projection",
        "Financial.Strategy.Revenue_Projections": "Revenue projection, sales forecast, or income estimate",
        "Financial.Strategy.Investment_Strategies": "Investment strategy, capital allocation, or funding decision",
    },

    #### Operational
    "Operational_&_Personal": {
        "Operational.Project.Technical_Blockers": "Technical blocker, project impediment, or development dependency",
        "Operational.Project.Progress_Updates": "Project progress update, status report, or milestone achievement",
        "Personal_Life.Health_Disclosures": "Personal health issue, medical condition, or doctor appointment",
        "Personal_Life.Crisis_Content": "Personal crisis, family emergency, or sensitive life event"
    },
}


###############################################################################
######################## Threshold Values for Zero-Shot #######################
CATEGORY_THRESHOLDS = {
    # High precision, low recall → LOWER threshold
    'Strategic.Board_Communications': 0.35,
    'Operational.Project.Technical_Blockers': 0.35,
    'Financial.Accounting.Firing_Hiring': 0.25,
    'Strategic.Pricing_Models': 0.30,
    'Strategic.Customer_Acquisition': 0.35,
    'R&D.Technical.Models': 0.35,
    'Financial.Strategy.Budget_Forecasting': 0.35,
    'Operational.Project.Progress_Updates': 0.40,
    
    # Balanced → Keep at 0.5
    'Strategic.M&A': 0.5,
    'Strategic.Market_Expansion': 0.5,
    'HR.Performance_Reviews': 0.5,
    'Financial.Accounting.Salary_Negotiations': 0.5,
    'Financial.Accounting.Bonuses': 0.5,
    
    # High recall, lower precision → RAISE threshold (reduce false positives)
    'R&D.Technical.Experiments': 0.6,  # 20 false positives
    'R&D.IP.Patentable_Ideas': 0.6,    # 15 false positives
    'HR.Internal_Disputes': 0.55,      # 8 false positives
}