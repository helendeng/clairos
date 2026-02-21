# This will set the category to (domain, subcategory) pipeline and dataclass
from enum import Enum

# TODO: Fill out list with sensitive categories in mind
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
    "Business_Strategy.M&A_Discussions": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Business_Strategy.Market_Expansion_Plans": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Business_Strategy.Pricing_Models": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Business_Strategy.Customer_Acquisition_Strategy": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Business_Strategy.Competitive_Analysis": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},
    "Business_Strategy.Board_Level_Communication": {"domain": "Strategic Confidential", "subdomain": "Business_Strategy"},


    ########################## R&D ############################
    ### Technical
    "Technical_R&D.Experiments": {"domain": "R&D", "subdomain": "Technical"},
    "Technical_R&D.Algorithms": {"domain": "R&D", "subdomain": "Technical"},
    "Technical_R&D.Models": {"domain": "R&D", "subdomain": "Technical"},
    "Technical_R&D.Prototype": {"domain": "R&D", "subdomain": "Technical"},
    "Technical_R&D.Hardware_Specifications": {"domain": "R&D", "subdomain": "Technical"},

    ### Scientific and IP
    "Scientific_&_IP.Patentable_Ideas": {"domain": "R&D", "subdomain": "Scientific_&_IP"},
    "Scientific_&_IP.Proprietary_Formulas": {"domain": "R&D", "subdomain": "Scientific_&_IP"},
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
    "Accounting.Salary_Negotiations": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Firing_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Hiring_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Bonus_Info": {"domain": "Financial", "subdomain": "Accounting"}, 
    "Accounting.Raise_Info": {"domain": "Financial", "subdomain": "Accounting"}, 

    ### Financial Strategy
    "Financial_Strategy.Budget_Forecasting": {"domain": "Financial", "subdomain": "Financial_Strategy"}, 
    "Financial_Strategy.Revenue_Projections": {"domain": "Financial", "subdomain": "Financial_Strategy"}, 
    "Financial_Strategy.Financial_Risk_Models": {"domain": "Financial", "subdomain": "Financial_Strategy"}, 
    "Financial_Strategy.Investment_Strategies": {"domain": "Financial", "subdomain": "Financial_Strategy"}, 
    "Financial_Strategy.Pricing_Models": {"domain": "Financial", "subdomain": "Financial_Strategy"}, 


    ########################## Operational ############################
    ### Project Metadata
    "Project_Metadata.Project_Deadlines": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Deliverables": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Handoff_Notes": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Progress_Updates": {"domain": "Operational", "subdomain": "Project_Metadata"}, 
    "Project_Metadata.Technocal_Blockers": {"domain": "Operational", "subdomain": "Project_Metadata"}, 

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
    "Health_Disclosures.Health_Disclosures": {"domain": "Personal", "subdomain": "Health_Disclosures"}, 

    ### Crisis/Sensitive Content 
    "Crisis_&_Sensitive.Breakups": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"}, 
    "Crisis_&_Sensitive.Family_Emergency": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"}, 
    "Crisis_&_Sensitive.Personal_Crisis": {"domain": "Personal", "subdomain": "Crisis_&_Sensitive"}, 

    ########################## Other ############################
    "Other.Other": {"domain": "Other", "subdomain": "Other"}, 
}

###############################################################################
############################### Category Keys #################################
# canonical keys
class CategoryKey(Enum):
    CREDIT_CARD = "financial.credit_card"
    EIN = "taxpayer.ein"
    API_KEY = "security.api_key"




###############################################################################
############################ Labels for Zero-Shot #############################
# The labels and their descriptions that will be fed into the Zero-Shot model
"""
1. HR: Performance Reviews, Internal Disputes
2. Legal.Litigation: Legal disputes, Notice of Claims, Pre-litigation
3. Legal.Compliance: SOX, Safety, Reporting Obligations
4. Legal.Privileged: To/from counsel, Referencing legal advice
5. Strategic: M&A, Market expansion, Pricing models, Customer acquisition, Competitive Analysis, Board Communications
6. R&D.Technical: Experiments, Algorithms, Models, Prototypes
7. R&D.IP: Patentable ideas, Proprietary formulas
8. Financial.Accounting: Salary negotiations, Firing/hiring, Bonuses
9. Financial.Strategy: Budget forecasting, Revenue projections, Investment strategies
10. Operational.Project: Technical blockers, Progress updates
11. Personal Life: Health disclosures, Crisis content
"""

ZERO_SHOT_LABELS = {
    #### HR
    "HR.Performance_Reviews": "Employee performance review, evaluation, or feedback discussion",
    "HR.Internal_Disputes": "Internal workplace conflict, disagreement, or dispute between employee",

    #### Legal
    "Legal.Litigation.Legal_Disputes": "Legal dispute, lawsuit, litigation, or court proceeding",
    "Legal.Litigation.Notice_of_Claims": "Notice of claim, formal complaint, or legal demand letter",
    "Legal.Litigation.Pre_Litigation": "Pre-litigation discussion, potential lawsuit, or threatened legal action",
    "Legal.Compliance.SOX": "Sarbanes-Oxley compliance, financial controls, or audit requirements",
    "Legal.Compliance.Safety": "Safety compliance, OSHA requirements, or workplace safety violations",
    "Legal.Compliance.Reporting_Obligations": "Regulatory reporting obligation, compliance deadline, or mandatory disclosure",
    "Legal.Privileged.To_From_Counsel": "Communication with attorney, legal counsel, or lawyer providing legal advice",
    "Legal.Privileged.Referencing_Legal_Advice": "Discussion referencing attorney advice, legal counsel recommendation, or privileged communication",

    #### Strategic
    "Strategic.M&A": "Merger, acquisition, company purchase, or buyout discussion",
    "Strategic.Market_Expansion": "Market expansion plan, new geographic territory, or business growth strategy",
    "Strategic.Pricing_Models": "Pricing strategy, pricing model, or margin analysis",
    "Strategic.Customer_Acquisition": "Customer acquisition strategy, sales funnel, or user growth tactics",
    "Strategic.Competitive_Analysis": "Competitive analysis, competitor research, or market positioning study",
    "Strategic.Board_Communications": "Board of directors meeting, board-level decision, or executive leadership communication",

    #### Research and Development
    "R&D.Technical.Experiments": "Scientific experiment, technical test, or research trial",
    "R&D.Technical.Algorithms": "Algorithm design, computational method, or optimization technique",
    "R&D.Technical.Models": "Machine learning model, predictive model, or statistical modeling approach",
    "R&D.Technical.Prototypes": "Prototype development, proof of concept, or experimental design",
    "R&D.IP.Patentable_Ideas": "Patentable invention, patent application, or novel intellectual property",
    "R&D.IP.Proprietary_Formulas": "Proprietary formula, trade secret, or confidential technical method",

    #### Financial
    "Financial.Accounting.Salary_Negotiations": "Salary negotiation, compensation discussion, or pay raise conversation",
    "Financial.Accounting.Firing_Hiring": "Employee termination, hiring decision, or staffing change",
    "Financial.Accounting.Bonuses": "Bonus payment, incentive compensation, or performance-based reward",
    "Financial.Strategy.Budget_Forecasting": "Budget forecast, financial planning, or spending projection",
    "Financial.Strategy.Revenue_Projections": "Revenue projection, sales forecast, or income estimate",
    "Financial.Strategy.Investment_Strategies": "Investment strategy, capital allocation, or funding decision",

    #### Operational
    "Operational.Project.Technical_Blockers": "Technical blocker, project impediment, or development dependency",
    "Operational.Project.Progress_Updates": "Project progress update, status report, or milestone achievement",

    #### Personal Life
    "Personal_Life.Health_Disclosures": "Personal health issue, medical condition, or doctor appointment",
    "Personal_Life.Crisis_Content": "Personal crisis, family emergency, or sensitive life event"
}