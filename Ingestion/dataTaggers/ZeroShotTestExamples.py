zero_shot_test_examples = [
    # =========================
    # HR.Performance_Reviews (10)
    # =========================
    {
        'text': "Subject: Q1 Performance Check-In\nHi Maya—your Q1 delivery was strong: you hit the launch date, unblocked QA, and mentored two new hires. Keep tightening your estimates; overall rating: Exceeds Expectations.",
        'true_labels': ['HR.Performance_Reviews']
    },
    {
        'text': "Subject: Feedback after customer escalation\nYour handling of the escalation was calm and effective. One improvement: loop Support earlier so we don't duplicate comms. Let's set a goal for proactive updates in Q2.",
        'true_labels': ['HR.Performance_Reviews', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Mid-year review notes\nStrengths: technical depth, ownership. Opportunities: documentation and handoffs. Proposed development plan attached; we'll revisit in 6 weeks.",
        'true_labels': ['HR.Performance_Reviews']
    },
    {
        'text': "Subject: Performance Improvement Plan (PIP)\nThis is a formal PIP due to repeated missed deadlines and unresolved bugs. Milestones: 2-week deliverables, weekly check-ins, and measurable quality targets.",
        'true_labels': ['HR.Performance_Reviews', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Peer feedback summary\nMultiple teammates noted you raise issues early and keep meetings focused. A few mentioned tone in code reviews can read as dismissive—please soften phrasing.",
        'true_labels': ['HR.Performance_Reviews', 'HR.Internal_Disputes']
    },
    {
        'text': "Subject: Bonus justification\nProposing an out-of-cycle bonus based on sustained performance: led incident response, reduced latency 22%, and delivered the compliance audit artifacts on time.",
        'true_labels': ['HR.Performance_Reviews', 'Financial.Accounting.Bonuses', 'Legal.All']
    },
    {
        'text': "Subject: Review calibration\nFor calibration: impact was high, scope moderate, collaboration high. Suggested rating: Meets+; promotion readiness: not yet—needs leadership across org boundary.",
        'true_labels': ['HR.Performance_Reviews']
    },
    {
        'text': "Subject: Internship evaluation\nJordan demonstrated strong debugging skills and shipped the dashboard ahead of schedule. Recommend return offer; mentorship notes included.",
        'true_labels': ['HR.Performance_Reviews', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Coaching notes\nYour technical output is excellent, but you frequently override stakeholders in meetings. Goal: ask clarifying questions before proposing solutions; track progress weekly.",
        'true_labels': ['HR.Performance_Reviews']
    },
    {
        'text': "Subject: End-of-year summary\nYou exceeded KPIs, improved onboarding docs, and reduced pager load. Areas to grow: cross-team communication and prioritization under ambiguity.",
        'true_labels': ['HR.Performance_Reviews']
    },

    # =========================
    # HR.Internal_Disputes (10)
    # =========================
    {
        'text': "Subject: Re: Code review disagreement\nThis is the third time you've blocked my PR without proposing alternatives. We need a mediator—this is stalling the release.",
        'true_labels': ['HR.Internal_Disputes', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Workplace conflict report\nI'm documenting repeated interruptions and dismissive comments from Alex during standup. Requesting HR guidance on next steps.",
        'true_labels': ['HR.Internal_Disputes']
    },
    {
        'text': "Subject: Escalation—team dynamics\nTwo engineers refuse to pair on the migration and are splitting the design into incompatible approaches. Please schedule a conflict-resolution meeting.",
        'true_labels': ['HR.Internal_Disputes', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Complaint about manager behavior\nI feel I'm being singled out with unrealistic deadlines compared to peers. I'd like to discuss this confidentially.",
        'true_labels': ['HR.Internal_Disputes', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Re: Ownership of the feature\nI was told I own the billing integration, but Priya keeps reassigning tasks without telling me. This is creating confusion and resentment.",
        'true_labels': ['HR.Internal_Disputes', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Hostile Slack messages\nAttaching screenshots of messages where I'm called incompetent. I want this addressed before it escalates further.",
        'true_labels': ['HR.Internal_Disputes']
    },
    {
        'text': "Subject: Mediation request\nCan we involve People Ops? We can't agree on the experiment design and it's becoming personal.",
        'true_labels': ['HR.Internal_Disputes', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Dispute over performance rating\nI disagree with my rating and believe the feedback is inconsistent with my documented outcomes. Requesting a formal review.",
        'true_labels': ['HR.Internal_Disputes', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Retaliation concern\nAfter I raised the safety issue, my shifts changed and I'm excluded from meetings. I'm worried this is retaliation.",
        'true_labels': ['HR.Internal_Disputes', 'Legal.All']
    },
    {
        'text': "Subject: Team conflict impacting delivery\nThe constant arguments between design and engineering are delaying decisions. We need a clear decision-maker and process.",
        'true_labels': ['HR.Internal_Disputes', 'Operational.Project.Technical_Blockers']
    },

    # =========================
    # Legal.Litigation.Legal_Disputes (10)
    # =========================
    {
        'text': "Subject: Lawsuit filed—ABC v. OurCo\nWe've been served with a complaint alleging breach of contract and damages. Litigation counsel is preparing the response timeline.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Court hearing schedule\nReminder: preliminary injunction hearing set for March 12. We need declarations and evidence exhibits finalized by next week.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Discovery hold\nLitigation is active. Please preserve all emails, Slack messages, and documents related to Project Orion—do not delete anything.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Settlement conference prep\nOpposing counsel proposed mediation; we need a settlement range recommendation and risk analysis before the conference.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Subpoena received\nWe received a subpoena requesting customer contracts and audit logs for 2024–2025. Legal will coordinate collection.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Breach of contract dispute update\nThe counterparty refuses to cure and is demanding immediate payment. Counsel recommends we prepare for litigation if negotiations fail.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Motion to dismiss draft\nDraft motion is attached for review—please provide any factual corrections by EOD Friday.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: PR + legal alignment\nBecause the lawsuit is public, marketing wants a statement. Legal says we must avoid admissions; please route all language through counsel.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Expert witness search\nWe need an expert in database performance to support our damages theory. Please share candidate lists and budgets.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },
    {
        'text': "Subject: Litigation risk—product claims\nCustomer alleges our product caused losses due to downtime; they've already retained counsel and are seeking damages.",
        'true_labels': ['Legal.All']
    },

    # =========================
    # Legal.Litigation.Notice_of_Claims (10)
    # =========================
    {
        'text': "Subject: Notice of Claim received\nWe received a formal Notice of Claim alleging negligence related to last month's incident. Forwarding to legal for intake.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Demand letter—IP infringement\nAttached is a demand letter claiming we infringe their patent and requesting immediate licensing talks.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'Legal.All']
    },
    {
        'text': "Subject: Formal complaint from vendor\nVendor counsel sent a written complaint alleging non-payment and breach. They request payment within 10 business days.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },
    {
        'text': "Subject: Claim notice—employment matter\nWe got a formal complaint alleging wrongful termination and discrimination. Preserve relevant documents.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Legal.All']
    },
    {
        'text': "Subject: Incoming claim—product liability\nWe received a written claim asserting the device was unsafe and caused injury; requesting insurance carrier notification.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Tort claim form\nCity claims property damage tied to our contractor's work; claim form attached with requested reimbursement.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Notice of intent to sue\nA letter from counsel states they intend to sue if we don't resolve within 30 days.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Claim acknowledgment\nPlease confirm receipt of the attached claim and provide next steps for our response under the contract.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Customer notice—data exposure\nCustomer sent a formal demand letter alleging damages from the breach and requesting remediation costs.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Claim regarding missed SLA\nFormal notice under the MSA: they claim we violated SLA uptime terms and are invoking service credits + damages.",
        'true_labels': ['Strategic.Pricing_Models', 'Legal.All']
    },

    # =========================
    # Legal.Litigation.Pre_Litigation (10)
    # =========================
    {
        'text': "Subject: Potential lawsuit risk\nCustomer is threatening to sue over termination fees. They haven't filed yet, but the tone is escalating.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Pre-litigation negotiation\nBefore anyone files, can we propose mediation? We need a settlement posture and a timeline to respond.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Escalation—legal exposure\nSales says the client will 'take this to court' if we don't refund. Please advise on response language.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Risk memo request\nCan Legal assess our exposure if VendorCo claims breach? No formal complaint yet; just emails from their CEO.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Preservation suggestion\nNot a lawsuit yet, but given the threats we should preserve Slack and email threads related to the contract negotiation.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Contract dispute—next steps\nThey're alleging we misrepresented features and want rescission. Counsel recommends we avoid admissions and gather facts.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Internal review before demand letter\nWe expect a demand letter soon. Please summarize timelines, commitments made, and who approved the statements.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Negotiation with counsel on cc\nLooping in our outside counsel—can you review the draft response before we send it?",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Threatened employment claim\nFormer employee says they'll sue unless we change the termination letter. Please handle via counsel.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Legal.All']
    },
    {
        'text': "Subject: Pre-suit strategy\nWe should evaluate settlement options vs. preparing for litigation. Provide cost ranges and best/worst-case outcomes.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },

    # =========================
    # Legal.Compliance.SOX (10)
    # =========================
    {
        'text': "Subject: SOX controls testing—Q2\nReminder: we must complete controls testing for revenue recognition workflows. Please provide evidence screenshots and approval logs.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Audit request—access reviews\nInternal audit requests quarterly user access review for finance systems. Confirm least-privilege and provide sign-off artifacts.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Financial controls gap\nWe found a segregation-of-duties issue: the same person can create vendors and approve payments. Need remediation plan by Friday.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: Change management controls\nFor SOX: document approvals for production changes affecting billing. Please ensure every deploy has ticket linkage and reviewer sign-off.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Evidence collection\nAuditors need evidence of monthly close procedures, reconciliations, and review timestamps. Upload to the audit portal.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Legal.All']
    },
    {
        'text': "Subject: SOX scoping\nWe're adding the new subscription module into SOX scope. Identify key reports, controls, and control owners.",
        'true_labels': ['Strategic.Pricing_Models', 'Legal.All']
    },
    {
        'text': "Subject: Audit findings\nFinding: incomplete documentation for journal entry approvals. Action: enforce approval workflow and retain logs for 7 years.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: CFO note—SOX readiness\nWe need to be audit-ready by quarter close. Any missing controls or unaddressed gaps must be escalated immediately.",
        'true_labels': ['Strategic.Board_Communications', 'Legal.All']
    },
    {
        'text': "Subject: SOX + incident\nBecause the incident impacted billing, audit wants root-cause plus evidence controls still operated effectively during the outage.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Legal.All']
    },
    {
        'text': "Subject: Controls attestation\nPlease sign the quarterly SOX sub-certification confirming controls were followed and exceptions were reported.",
        'true_labels': ['Legal.All']
    },

    # =========================
    # Legal.Compliance.Safety (10)
    # =========================
    {
        'text': "Subject: OSHA log update\nWe need to record the warehouse injury on the OSHA 300 log and review corrective actions for the forklift aisle policy.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Safety violation report\nMultiple employees reported missing PPE in the lab. Please replenish supplies and enforce mandatory goggles immediately.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Workplace hazard assessment\nFacilities flagged exposed wiring near the test bench. This is a safety risk—request urgent remediation.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: Incident investigation\nFollowing the near-miss, we must complete a safety incident report and implement training before resuming operations.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Safety compliance training\nAll staff must complete annual safety training by end of month; managers track completion rates.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Chemical storage audit\nThe inspection found unlabeled containers and incompatible storage. Corrective actions required within 48 hours.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Contractor safety rules\nBefore the construction work starts, confirm contractors follow site safety plan and provide proof of training.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Ergonomics complaint\nSeveral employees report wrist strain due to workstation setup. Please evaluate and document corrective measures.",
        'true_labels': ['Personal_Life.Health_Disclosures', 'Legal.All']
    },
    {
        'text': "Subject: Safety non-compliance escalation\nIf we don't fix the guardrail issue, we risk regulatory penalties. Please prioritize this over non-critical work.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Emergency drill\nReminder: building evacuation drill is required this quarter; ensure floor wardens are assigned and outcomes documented.",
        'true_labels': ['Legal.All']
    },

    # =========================
    # Legal.Compliance.Reporting_Obligations (10)
    # =========================
    {
        'text': "Subject: Regulatory filing deadline\nReminder: the quarterly compliance report must be submitted by April 15. Please send finalized metrics and attestations.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Data breach notification timeline\nWe may have a 72-hour notification obligation depending on scope. Legal needs incident details and impacted regions ASAP.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Audit response due date\nExternal auditors require responses to PBC items by Friday. Missing this is a compliance risk.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Government request\nWe must respond to the agency inquiry within 10 days. Please gather requested documentation and timeline events.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Mandatory disclosure\nPer contract, we must disclose the outage incident to EnterpriseCustomer within 5 business days. Draft is in review.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Legal.All']
    },
    {
        'text': "Subject: Safety reporting\nOSHA reporting may be required for the hospitalization event. Confirm details and prepare submission.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: SEC-style controls certification\nLeadership needs quarterly certification statements and evidence packets; please complete by EOD Wednesday.",
        'true_labels': ['Strategic.Board_Communications', 'Legal.All']
    },
    {
        'text': "Subject: Contractual notice\nWe must provide written notice to VendorCo within 30 days to preserve our rights. Please send draft notice to legal.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Export compliance recordkeeping\nReminder: keep records of shipments and screening results for the required retention period; upload logs monthly.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Reporting obligation—incident postmortem\nCustomer contract requires an incident report within 7 days including root cause and prevention plan. Engineering, please provide details.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Legal.All']
    },

    # =========================
    # Legal.Privileged.To_From_Counsel (10)
    # =========================
    {
        'text': "Subject: Attorney review requested\nHi Counsel—please review the attached contract redlines and advise on risk items before we sign.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Legal advice on termination\nCounsel, can you advise on whether we can terminate this employee for cause given the documentation timeline?",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Legal.All']
    },
    {
        'text': "Subject: Privileged—strategy memo\nOutside counsel drafted a litigation risk memo. Please keep distribution limited and do not forward externally.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Counsel on cc—response draft\nSharing the draft response to the customer complaint; counsel is cc'd for legal review and suggested edits.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Request for legal interpretation\nCan you interpret the indemnification clause and tell us if this triggers a duty to defend?",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Counsel guidance on compliance\nCounsel—do we have any reporting obligations due to this incident? Please advise on deadlines and wording.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Privileged comms re: IP\nCounsel, do we have freedom-to-operate concerns for this feature? Attaching the technical description and prior art notes.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'Legal.All']
    },
    {
        'text': "Subject: Employment policy question\nCounsel, please confirm whether our new policy language creates any legal exposure in CA/NY.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Demand letter response—legal review\nBefore we send anything, counsel needs to approve the final wording. Please route all replies through legal.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Privileged—board materials\nCounsel reviewed the board deck section on the dispute; please use the counsel-approved version only.",
        'true_labels': ['Strategic.Board_Communications', 'Legal.All']
    },

    # =========================
    # Legal.Privileged.Referencing_Legal_Advice (10)
    # =========================
    {
        'text': "Subject: Re: Contract response\nPer legal's guidance, we should avoid acknowledging breach and instead propose a 'without prejudice' meeting.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Messaging constraints\nLegal advised we cannot promise refunds in writing. Please remove that sentence from the customer email draft.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Policy update\nBased on counsel's recommendation, we're revising retention settings and restricting access to sensitive logs.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Incident disclosure\nLegal said we may need to notify regulators depending on scope; engineering must confirm affected users and timelines.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Litigation posture\nCounsel recommends we don't engage further without a formal response plan. Please pause negotiations for now.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Employment risk\nPer counsel's advice, do not discuss performance concerns in Slack—use documented channels and HR templates.",
        'true_labels': ['HR.Performance_Reviews', 'Legal.All']
    },
    {
        'text': "Subject: Product claims wording\nLegal told us to describe the issue as 'service disruption' not 'failure' to avoid admissions. Update the postmortem wording.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Legal.All']
    },
    {
        'text': "Subject: Negotiation plan\nFollowing counsel's recommendation, propose mediation before suit and set a response deadline to the demand letter.",
        'true_labels': ['Legal.All']
    },
    {
        'text': "Subject: Board update\nLegal advised that board minutes should avoid detailed legal theories; keep discussion high-level and action-focused.",
        'true_labels': ['Strategic.Board_Communications', 'Legal.All']
    },
    {
        'text': "Subject: IP precautions\nCounsel suggested we document the invention timeline and limit distribution of the proprietary method until filing decisions are made.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'Legal.All']
    },

    # =========================
    # Strategic.M&A (10)
    # =========================
    {
        'text': "Subject: Acquisition target shortlist\nWe're evaluating acquiring DataForge this quarter. Initial valuation range: $40-$60M; due diligence kick-off next week.",
        'true_labels': ['Strategic.M&A', 'Financial.Strategy.Investment_Strategies']
    },
    {
        'text': "Subject: LOI draft\nAttached is the draft LOI for the TechCo acquisition, including exclusivity period and proposed purchase price structure.",
        'true_labels': ['Strategic.M&A', 'Legal.All']
    },
    {
        'text': "Subject: Integration plan\nIf we acquire them, we need a 90-day integration plan: org design, product roadmap consolidation, and pricing alignment.",
        'true_labels': ['Strategic.M&A', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Potential carve-out\nExploring buying only the AI division (asset purchase) rather than the full company; need tax + legal input.",
        'true_labels': ['Strategic.M&A', 'Legal.All']
    },
    {
        'text': "Subject: Due diligence—security\nRequesting diligence docs: SOC2 reports, incident history, access controls. This is gating the acquisition timeline.",
        'true_labels': ['Strategic.M&A', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Competing bid rumor\nHearing there's another bidder. If true, we may need to move faster or revise our offer terms.",
        'true_labels': ['Strategic.M&A']
    },
    {
        'text': "Subject: Board update—M&A pipeline\nFor the board: two active targets, one paused. Seeking guidance on capital allocation and risk appetite.",
        'true_labels': ['Strategic.M&A', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Talent acquisition via acquisition\nMain goal is the team + their proprietary algorithm; product can be sunset. Please estimate retention packages.",
        'true_labels': ['Strategic.M&A', 'Financial.Accounting.Bonuses', 'R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Acquisition synergy model\nFinance is modeling synergies: reduced infra spend, cross-sell uplift, and headcount consolidation assumptions.",
        'true_labels': ['Strategic.M&A', 'Financial.Strategy.Budget_Forecasting', 'Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Post-close pricing migration\nIf we buy them, we must migrate customers to our pricing tiers over 6 months—risk of churn is non-trivial.",
        'true_labels': ['Strategic.M&A', 'Strategic.Pricing_Models', 'Strategic.Customer_Acquisition']
    },

    # =========================
    # Strategic.Market_Expansion (10)
    # =========================
    {
        'text': "Subject: LATAM expansion plan\nProposal: launch in Brazil + Mexico in Q3, localize billing, and hire regional sales leads. Market sizing attached.",
        'true_labels': ['Strategic.Market_Expansion', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: New territory decision\nWe need to decide: enter healthcare vertical or expand into EMEA first. Please provide go-to-market risks and timelines.",
        'true_labels': ['Strategic.Market_Expansion', 'Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Regulatory constraints\nMarket expansion to EU requires data residency and reporting considerations; legal should review requirements before commit.",
        'true_labels': ['Strategic.Market_Expansion', 'Legal.All']
    },
    {
        'text': "Subject: Partner strategy\nTo expand into APAC, we should partner with a reseller rather than direct sales. Draft partner criteria attached.",
        'true_labels': ['Strategic.Market_Expansion', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Expansion KPI targets\nGoals: 200 net-new customers in the new region, CAC payback < 9 months, and churn < 2% monthly.",
        'true_labels': ['Strategic.Market_Expansion', 'Strategic.Customer_Acquisition', 'Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Localization blockers\nExpansion is blocked on localization for invoices and tax rules. Engineering needs a plan for the compliance layer.",
        'true_labels': ['Strategic.Market_Expansion', 'Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: New office footprint\nMarket expansion requires a small office in Dublin. Facilities cost estimate + hiring plan requested.",
        'true_labels': ['Strategic.Market_Expansion', 'Financial.Strategy.Budget_Forecasting', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Competitive landscape—new region\nCompetitors in-region undercut pricing by 20%. We need differentiated positioning and potentially different tiers.",
        'true_labels': ['Strategic.Market_Expansion', 'Strategic.Competitive_Analysis', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Expansion narrative for board\nBoard deck: rationale, market size, execution plan, risks, and expected revenue contribution by quarter.",
        'true_labels': ['Strategic.Market_Expansion', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Pilot launch\nLet's run a 6-week pilot in Canada before broader expansion. Need success criteria, experiment design, and budget.",
        'true_labels': ['Strategic.Market_Expansion', 'R&D.Technical.Experiments', 'Financial.Strategy.Budget_Forecasting']
    },

    # =========================
    # Strategic.Pricing_Models (10)
    # =========================
    {
        'text': "Subject: Pricing tier redesign\nProposal: move from seat-based to usage-based pricing with minimum commit. Margin impact model attached.",
        'true_labels': ['Strategic.Pricing_Models', 'Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Discount policy\nSales is requesting a new discount band for enterprise deals. We need guardrails so discounts don't destroy margin.",
        'true_labels': ['Strategic.Pricing_Models', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Pricing A/B test\nPlan to run an experiment on new onboarding flow + price page. Need experiment design and tracking metrics.",
        'true_labels': ['Strategic.Pricing_Models', 'R&D.Technical.Experiments', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Price increase notification\nWe're raising prices 12% at renewal. Draft customer email and contract language need review.",
        'true_labels': ['Strategic.Pricing_Models', 'Legal.All']
    },
    {
        'text': "Subject: Competitor price match\nCompetitor offers 30% lower. Should we match or reposition? Need competitive analysis and churn risk estimate.",
        'true_labels': ['Strategic.Pricing_Models', 'Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Revenue leakage\nCurrent pricing doesn't charge for premium support; we're losing revenue. Suggest add-on SKU + internal process updates.",
        'true_labels': ['Strategic.Pricing_Models', 'Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Contract renewal terms\nCustomer insists on old pricing tier; legal says we must ensure most-favored-nation clause doesn't trigger.",
        'true_labels': ['Strategic.Pricing_Models', 'Legal.All']
    },
    {
        'text': "Subject: Pricing model for new product\nNeed to price the new feature bundle. Inputs: infra costs, support load, target gross margin, market willingness-to-pay.",
        'true_labels': ['Strategic.Pricing_Models', 'Financial.Strategy.Budget_Forecasting', 'Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Usage metering accuracy\nPricing change depends on accurate metering. Engineering reports current logs are incomplete—this blocks launch.",
        'true_labels': ['Strategic.Pricing_Models', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Board question on pricing\nBoard wants rationale for pricing shift and expected revenue lift. Provide sensitivity analysis for churn vs ARPU changes.",
        'true_labels': ['Strategic.Pricing_Models', 'Strategic.Board_Communications', 'Financial.Strategy.Revenue_Projections']
    },

    # =========================
    # Strategic.Customer_Acquisition (10)
    # =========================
    {
        'text': "Subject: Q2 acquisition plan\nWe're shifting spend to high-intent channels and refining the funnel: landing page, trial, activation, then upsell.",
        'true_labels': ['Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Growth experiment backlog\nIdeas: referral program, onboarding nudges, reactivation emails. Prioritize by expected lift and engineering cost.",
        'true_labels': ['Strategic.Customer_Acquisition', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: CAC analysis\nPaid search CAC doubled; we need creative refresh and maybe new pricing entry tier to improve conversion.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Sales enablement\nTo acquire more enterprise accounts, we need a case study deck, ROI calculator, and new outbound sequences.",
        'true_labels': ['Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Product-led growth\nProposal: add an in-app shareable report to drive virality; track invites sent and activation rates.",
        'true_labels': ['Strategic.Customer_Acquisition', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Partner channel acquisition\nReseller pipeline looks promising; define partner incentives and lead handoff process.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Financial.Strategy.Investment_Strategies']
    },
    {
        'text': "Subject: Competitive wedge\nCompetitor is weak on compliance—position our product as safer and use that in outbound messaging.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Strategic.Competitive_Analysis', 'Legal.All']
    },
    {
        'text': "Subject: Trial conversion blockers\nEngineering says signup errors are spiking due to auth changes. This is killing acquisition—fix ASAP.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Revenue target linkage\nTo hit revenue projections, we need +30% new customers. Provide weekly acquisition dashboard and forecast.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Financial.Strategy.Revenue_Projections', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Board asks about growth\nBoard wants a clear customer acquisition narrative: channels, costs, risks, and expected payback timeline.",
        'true_labels': ['Strategic.Customer_Acquisition', 'Strategic.Board_Communications', 'Financial.Strategy.Budget_Forecasting']
    },

    # =========================
    # Strategic.Competitive_Analysis (10)
    # =========================
    {
        'text': "Subject: Competitor teardown\nAttached: breakdown of RivalCo features, pricing, and positioning. Key gap: they lack audit logs; we should emphasize ours.",
        'true_labels': ['Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Win/loss analysis\nIn last 12 enterprise deals, we lost 7 to CompetitorX. Reasons: price + integration. Recommendations included.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Market positioning memo\nWe should position as the 'compliance-first' option. Competitors optimize for speed; our differentiation is trust.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Legal.All']
    },
    {
        'text': "Subject: Competitive intelligence request\nPlease gather RivalCo's latest release notes, customer testimonials, and rumored roadmap; summarize by Friday.",
        'true_labels': ['Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Feature parity debate\nSales claims we must match their workflow feature to stay competitive; product thinks we should double down on our strengths.",
        'true_labels': ['Strategic.Competitive_Analysis', 'HR.Internal_Disputes']
    },
    {
        'text': "Subject: Competitor pricing pressure\nCompetitors are offering aggressive discounts. We need a response strategy and an updated pricing model.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: TAM/SAM/SOM notes\nSizing: our best segment is mid-market regulated industries. Competitors focus SMB—opportunity for us.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Strategic.Market_Expansion']
    },
    {
        'text': "Subject: Competitive landscape for board\nBoard deck section: who the competitors are, how we win, and what could disrupt us this year.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Head-to-head benchmark\nWe ran a performance benchmark vs RivalCo; results show lower latency for us but weaker admin UX.",
        'true_labels': ['Strategic.Competitive_Analysis', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Competitive threat—new entrant\nA new open-source tool is gaining traction. Need analysis of adoption curve and whether acquisition or partnership makes sense.",
        'true_labels': ['Strategic.Competitive_Analysis', 'Strategic.M&A', 'Financial.Strategy.Investment_Strategies']
    },

    # =========================
    # Strategic.Board_Communications (10)
    # =========================
    {
        'text': "Subject: Board meeting agenda\nAgenda: Q4 results, security posture, budget approval, and CEO succession planning. Pre-read deck attached.",
        'true_labels': ['Strategic.Board_Communications']
    },
    {
        'text': "Subject: Board minutes draft\nDraft minutes from last meeting for review—please confirm decisions on pricing change and expansion plan.",
        'true_labels': ['Strategic.Board_Communications', 'Strategic.Pricing_Models', 'Strategic.Market_Expansion']
    },
    {
        'text': "Subject: Board update—incident\nWe need to brief the board on the outage: impact, remediation, and any reporting obligations.",
        'true_labels': ['Strategic.Board_Communications', 'Operational.Project.Progress_Updates', 'Legal.All']
    },
    {
        'text': "Subject: Compensation committee\nComp committee requests bonus recommendations and performance summaries for VP-level roles.",
        'true_labels': ['Strategic.Board_Communications', 'Financial.Accounting.Bonuses', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Board approval required\nCapital allocation decision: approve acquisition budget ceiling and authorize diligence spend.",
        'true_labels': ['Strategic.Board_Communications', 'Strategic.M&A', 'Financial.Strategy.Investment_Strategies']
    },
    {
        'text': "Subject: Investor/board Q&A prep\nAnticipated questions: churn, CAC, margins, audit readiness. Provide crisp answers + backup slides.",
        'true_labels': ['Strategic.Board_Communications', 'Financial.Strategy.Revenue_Projections', 'Legal.All']
    },
    {
        'text': "Subject: Governance update\nBoard wants an updated risk register and compliance overview—especially around reporting deadlines and safety incidents.",
        'true_labels': ['Strategic.Board_Communications', 'Legal.All']
    },
    {
        'text': "Subject: Board decision memo\nDecision needed: proceed with EMEA expansion vs. delay for product hardening. Include financial forecast scenarios.",
        'true_labels': ['Strategic.Board_Communications', 'Strategic.Market_Expansion', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Executive session\nBoard requests an executive session without management to discuss leadership and org health issues.",
        'true_labels': ['Strategic.Board_Communications', 'HR.Internal_Disputes']
    },
    {
        'text': "Subject: Board materials confidentiality\nReminder: board materials are confidential. Use the secure portal only; do not forward via email.",
        'true_labels': ['Strategic.Board_Communications']
    },

    # =========================
    # R&D.Technical.Experiments (10)
    # =========================
    {
        'text': "Subject: Experiment plan—new embedding model\nWe'll run an A/B test comparing retrieval quality across two embedding models. Metrics: MRR, nDCG, latency, and cost.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Lab test results\nPrototype sensor rig was tested across 30 trials; failure rate 12%. Need revised setup and rerun next week.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Hyperparameter sweep\nRunning a sweep over learning rate and batch size; logging validation curves and overfitting signals.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Benchmark methodology\nTo compare algorithms fairly, fix random seeds, use same dataset split, and report confidence intervals across 5 runs.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Experiment anomaly\nOne run shows a 3x accuracy jump; suspect data leakage. Re-running with stricter train/test isolation.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: User study design\nWe're testing whether the new UI reduces time-to-answer. Need consent language and success criteria.",
        'true_labels': ['R&D.Technical.Experiments', 'Legal.All']
    },
    {
        'text': "Subject: Experiment backlog grooming\nPrioritize experiments by expected learning value, not just potential wins. Kill low-signal tests quickly.",
        'true_labels': ['R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Load test as experiment\nWe'll simulate 10k requests/min to test scaling behavior. Compare caching strategy A vs B.",
        'true_labels': ['R&D.Technical.Experiments', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Experimental feature flag\nShip the new ranking model behind a flag; collect metrics before full rollout.",
        'true_labels': ['R&D.Technical.Experiments', 'R&D.Technical.Models', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Replication attempt\nTrying to replicate a published result; our numbers don't match. Need to verify dataset preprocessing steps.",
        'true_labels': ['R&D.Technical.Experiments']
    },

    # =========================
    # R&D.Technical.Algorithms (10)
    # =========================
    {
        'text': "Subject: New routing algorithm proposal\nDesigning an algorithm to minimize cost under latency constraints; considering A* variant with heuristics.",
        'true_labels': ['R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Optimization method\nWe should replace brute force with dynamic programming; complexity drops from O(n^3) to O(n^2).",
        'true_labels': ['R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Ranking algorithm bug\nThe sorting step breaks stability; need a deterministic tie-breaker to avoid jitter in results.",
        'true_labels': ['R&D.Technical.Algorithms', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Algorithm design review\nPlease review the pseudocode for the new deduplication method; prove it handles edge cases and is linear-time.",
        'true_labels': ['R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Streaming algorithm\nNeed an online algorithm to update metrics without storing all events. Proposing reservoir sampling + sketches.",
        'true_labels': ['R&D.Technical.Algorithms', 'R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Algorithm + model boundary\nThe model outputs candidates, but the algorithm chooses final allocations under constraints. Document this pipeline clearly.",
        'true_labels': ['R&D.Technical.Algorithms', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Algorithm performance benchmark\nOur new algorithm reduces latency by 18% but increases memory. Need tradeoff analysis and tuning suggestions.",
        'true_labels': ['R&D.Technical.Algorithms', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Approximation approach\nExact solution is NP-hard; propose greedy approximation with provable bound and empirical validation.",
        'true_labels': ['R&D.Technical.Algorithms', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Edge-case correctness\nAlgorithm fails when input list is empty or contains duplicates. Add invariants and unit tests.",
        'true_labels': ['R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Patent angle\nThis algorithmic improvement might be patentable if we can articulate novelty vs prior art—capture details now.",
        'true_labels': ['R&D.Technical.Algorithms', 'R&D.IP.Patentable_Ideas']
    },

    # =========================
    # R&D.Technical.Models (10)
    # =========================
    {
        'text': "Subject: Model evaluation summary\nThe classifier improves F1 from 0.71 to 0.78. Error analysis shows confusion between legal and HR labels.",
        'true_labels': ['R&D.Technical.Models']
    },
    {
        'text': "Subject: Model training run\nTraining the transformer with new data augmentation; monitoring loss, calibration, and drift metrics.",
        'true_labels': ['R&D.Technical.Models']
    },
    {
        'text': "Subject: Deployment readiness\nBefore shipping the model, we need guardrails, monitoring, and rollback strategy if hallucinations spike.",
        'true_labels': ['R&D.Technical.Models', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Model card draft\nDocument intended use, limitations, bias risks, and evaluation datasets. Include privacy and compliance notes.",
        'true_labels': ['R&D.Technical.Models', 'Legal.All']
    },
    {
        'text': "Subject: Drift alert\nProduction distribution shifted—more legal content than usual. Re-train or adjust thresholds to maintain precision.",
        'true_labels': ['R&D.Technical.Models', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Fine-tuning vs zero-shot\nZero-shot is fast but inconsistent on rare labels. Consider light fine-tuning with curated examples.",
        'true_labels': ['R&D.Technical.Models']
    },
    {
        'text': "Subject: Model interpretability\nAdd attention/feature attribution snapshots for top predictions so auditors can understand decisions.",
        'true_labels': ['R&D.Technical.Models', 'Legal.All']
    },
    {
        'text': "Subject: Model failure case\nModel flags a lot of benign emails as litigation. We need thresholding + better negative examples.",
        'true_labels': ['R&D.Technical.Models', 'Legal.All']
    },
    {
        'text': "Subject: Cost/perf tradeoff\nSmaller model is 2x faster but loses recall on privileged comms. Decide based on risk tolerance.",
        'true_labels': ['R&D.Technical.Models', 'Legal.All']
    },
    {
        'text': "Subject: Model + algorithm integration\nPipeline: NER extracts entities, model classifies doc type, algorithm selects snippets for the brief. Document interfaces.",
        'true_labels': ['R&D.Technical.Models', 'R&D.Technical.Algorithms']
    },

    # =========================
    # R&D.Technical.Prototypes (10)
    # =========================
    {
        'text': "Subject: Prototype build\nWe assembled a proof-of-concept pipeline that ingests emails and outputs a structured brief in under 10 seconds.",
        'true_labels': ['R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Prototype demo feedback\nDemo worked, but the UI froze during large uploads. Need performance profiling before next demo.",
        'true_labels': ['R&D.Technical.Prototypes', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Hardware prototype\nThe sensor prototype captures motion, but calibration drifts over time. Plan: redesign mounting + rerun tests.",
        'true_labels': ['R&D.Technical.Prototypes', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: MVP scope\nPrototype should support 3 labels only for first test, then expand taxonomy gradually. Avoid overbuilding.",
        'true_labels': ['R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Prototype security review\nBefore sharing the prototype externally, confirm redaction works and privileged content can't leak.",
        'true_labels': ['R&D.Technical.Prototypes', 'Legal.All']
    },
    {
        'text': "Subject: Prototype metrics\nInitial throughput: 25 docs/min; latency p95: 6s. Next: optimize chunking and caching.",
        'true_labels': ['R&D.Technical.Prototypes', 'R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Prototype funding request\nNeed $15k for prototype infra and test devices. Please approve budget allocation.",
        'true_labels': ['R&D.Technical.Prototypes', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Prototype integration plan\nIntegrate the prototype with auth and role-based access. Blocker: unclear API contract with identity provider.",
        'true_labels': ['R&D.Technical.Prototypes', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Prototype usability test\nRunning a small user test with 5 engineers. Collect time-to-task and qualitative feedback.",
        'true_labels': ['R&D.Technical.Prototypes', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Prototype packaging\nWe need a deployable container image for the prototype so others can reproduce results consistently.",
        'true_labels': ['R&D.Technical.Prototypes']
    },

    # =========================
    # R&D.IP.Patentable_Ideas (10)
    # =========================
    {
        'text': "Subject: Potential invention disclosure\nWe may have a novel method for role-aware redaction that preserves utility while minimizing leakage. Documenting for possible filing.",
        'true_labels': ['R&D.IP.Patentable_Ideas']
    },
    {
        'text': "Subject: Patentability check\nThis new ranking approach seems different from prior art. Please capture diagrams, novelty claims, and implementation details.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Invention timeline\nRecord the invention date, contributors, and early prototypes. Keep this confidential until counsel review.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'Legal.All']
    },
    {
        'text': "Subject: Novel hardware mechanism\nThe gripper design uses a new compliant linkage for fragile objects—this may be patentable. CAD screenshots attached.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Prior art notes\nI searched papers and patents and didn't find this exact technique. Still, we should do a formal prior art search.",
        'true_labels': ['R&D.IP.Patentable_Ideas']
    },
    {
        'text': "Subject: Disclosure draft\nDrafting an invention disclosure: problem, solution, differentiators, and alternate embodiments. Need contributor list confirmed.",
        'true_labels': ['R&D.IP.Patentable_Ideas']
    },
    {
        'text': "Subject: Keep it quiet\nPlease don't share the new method outside the team until we decide whether to file. Limit Slack discussion.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Patent vs trade secret decision\nWe need to decide: file a patent or keep as trade secret. Consider reverse-engineering risk and product exposure.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Counsel feedback\nLegal suggested tightening claims language and removing public references from the draft write-up.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'Legal.All']
    },
    {
        'text': "Subject: Collaboration note\nTwo teams independently built similar features; we need to clarify inventorship and consolidate documentation.",
        'true_labels': ['R&D.IP.Patentable_Ideas', 'HR.Internal_Disputes']
    },

    # =========================
    # R&D.IP.Proprietary_Formulas (10)
    # =========================
    {
        'text': "Subject: Confidential scoring formula\nDo not share externally: our internal risk-scoring formula weights access level, entity density, and context signals.",
        'true_labels': ['R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Trade secret handling\nThe new extraction heuristic is a trade secret. Store only in the secure repo; no screenshots in tickets.",
        'true_labels': ['R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Proprietary pipeline details\nOur chunking + reranking approach is core IP. Please keep implementation notes private until leadership approves disclosure.",
        'true_labels': ['R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Secret sauce tuning\nWe found a thresholding trick that reduces false positives by 30%. Keep the parameterization confidential.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: NDA reminder\nBefore we discuss the proprietary method with the partner, confirm NDA is signed and counsel approved scope.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'Legal.All']
    },
    {
        'text': "Subject: Access restriction\nOnly the core team should have access to the formula spreadsheet and calibration code. Remove broad org permissions.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'Legal.All']
    },
    {
        'text': "Subject: Documentation request\nWrite internal-only documentation for the trade-secret method: inputs, outputs, failure modes, and guardrails.",
        'true_labels': ['R&D.IP.Proprietary_Formulas']
    },
    {
        'text': "Subject: Vendor question\nVendor asked how our system computes risk. Provide a high-level explanation only—do not reveal the formula.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'Strategic.Competitive_Analysis']
    },
    {
        'text': "Subject: Potential leak concern\nI saw the proprietary formula pasted into a public channel. Please remove immediately and remind team about confidentiality.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'HR.Internal_Disputes']
    },
    {
        'text': "Subject: Trade secret vs patent\nThis method might be patentable, but disclosure would expose implementation. Leaning trade secret—need decision memo.",
        'true_labels': ['R&D.IP.Proprietary_Formulas', 'R&D.IP.Patentable_Ideas']
    },

    # =========================
    # Financial.Accounting.Salary_Negotiations (10)
    # =========================
    {
        'text': "Subject: Compensation discussion\nI'd like to revisit my base salary given expanded scope and market rates. Can we schedule a comp review this week?",
        'true_labels': ['Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Offer negotiation\nThanks for the offer. I'm excited, but I'm looking for a higher base and a signing bonus to make the move work.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations', 'Financial.Accounting.Bonuses']
    },
    {
        'text': "Subject: Raise request\nGiven my performance and new responsibilities, I'm requesting a salary adjustment effective next pay period.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Equity vs cash mix\nCan we discuss shifting comp mix toward equity instead of base? I'd like clarity on vesting and refresh schedule.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Market data\nAttached are salary benchmarks for my role in NYC/SF. Requesting alignment to the 75th percentile band.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Counteroffer\nMy current employer countered with a raise. If you can match the base, I can commit by Friday.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Promotion comp adjustment\nIf the promotion is approved, I want to confirm the new salary band, bonus target, and title mapping.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Cost of living\nGiven the relocation, I'm requesting a comp adjustment or stipend to offset cost-of-living differences.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Timeline for comp decision\nWhen will the compensation committee finalize the raise pool? I need to plan finances accordingly.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Comp dispute\nI believe my salary is mis-leveled compared to peers with similar scope. Requesting a formal review and adjustment.",
        'true_labels': ['Financial.Accounting.Salary_Negotiations', 'HR.Internal_Disputes']
    },

    # =========================
    # Financial.Accounting.Firing_Hiring (10)
    # =========================
    {
        'text': "Subject: Hiring approval\nRequesting approval to open two roles for the infra team due to increased on-call load and roadmap commitments.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Candidate decision\nWe should extend an offer to Sam. Strong systems background and culture fit; comp range included below.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Financial.Accounting.Salary_Negotiations']
    },
    {
        'text': "Subject: Termination paperwork\nConfirming we are proceeding with termination effective Friday. HR will coordinate access removal and final paycheck.",
        'true_labels': ['Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Layoff planning\nDue to budget cuts, we need a reduction-in-force plan. Please provide team impact and severance estimates.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Hiring freeze\nEffective immediately, hiring is paused for non-critical roles. Exceptions require CFO approval.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Backfill request\nWe need to backfill the security engineer role after resignation; risk is too high to leave open.",
        'true_labels': ['Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Offer rescinded\nDue to changing financial conditions, we must rescind the pending offer. Legal wants the wording reviewed.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Legal.All']
    },
    {
        'text': "Subject: Contractor conversion\nProposal to convert two contractors to FTE to reduce long-term cost and improve retention.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Financial.Strategy.Investment_Strategies']
    },
    {
        'text': "Subject: Hiring plan vs roadmap\nIf we don't hire two more engineers, we can't deliver the compliance features this year—please decide priority.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: Termination risk\nFormer employee is threatening legal action after termination. Route all communication through counsel.",
        'true_labels': ['Financial.Accounting.Firing_Hiring', 'Legal.All']
    },

    # =========================
    # Financial.Accounting.Bonuses (10)
    # =========================
    {
        'text': "Subject: Bonus payout schedule\nReminder: annual bonuses will be paid on March 1. Confirm your banking details in the HR portal.",
        'true_labels': ['Financial.Accounting.Bonuses']
    },
    {
        'text': "Subject: Spot bonus nomination\nNominating Taylor for a spot bonus for resolving the production incident and preventing recurrence.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Sales commission true-up\nWe need to reconcile commission payouts for Q4 due to retroactive contract changes.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Bonus pool constraints\nFinance is reducing bonus pool by 10% due to revenue shortfall. Managers: recalibrate allocations.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Retention bonus proposal\nTo retain key engineers through the acquisition integration, propose retention bonuses with 12-month cliff.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Strategic.M&A']
    },
    {
        'text': "Subject: Bonus dispute\nI believe my bonus calculation is wrong relative to my performance rating and target percentage.",
        'true_labels': ['Financial.Accounting.Bonuses', 'HR.Internal_Disputes', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Performance bonus criteria\nCriteria: reliability improvements, shipping milestones, and quality targets. Please align goals to the rubric.",
        'true_labels': ['Financial.Accounting.Bonuses', 'HR.Performance_Reviews']
    },
    {
        'text': "Subject: Bonus approval workflow\nAll bonus exceptions require VP approval and documentation for audit purposes.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Legal.All']
    },
    {
        'text': "Subject: Sign-on bonus repayment\nReminder: sign-on bonus repayment clause triggers if you leave before 12 months. Please acknowledge receipt.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Bonus timing\nGiven the delayed audit, can we shift bonus payouts? Need legal + finance confirmation of constraints.",
        'true_labels': ['Financial.Accounting.Bonuses', 'Legal.All']
    },

    # =========================
    # Financial.Strategy.Budget_Forecasting (10)
    # =========================
    {
        'text': "Subject: FY budget forecast\nPlease submit Q3-Q4 spend forecasts by category: headcount, infra, vendors, and travel.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Cloud cost forecast\nInfra costs are trending +18% vs plan. Forecast the next 2 quarters and propose cost containment options.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Scenario planning\nBuild three budget scenarios: base, aggressive growth, and downturn. Include hiring plan assumptions.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Budget reallocation request\nWe need to shift $50k from marketing to security remediation. Provide justification and impact on acquisition targets.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Budget approval cycle\nBudget freeze ends next week; submit revised forecasts before finance finalizes.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Procurement planning\nForecast vendor spend for audit tools and compliance support; include contract renewal dates and expected increases.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },
    {
        'text': "Subject: M&A diligence spend\nWe need a forecast for diligence spend (legal, accounting, consultants) for the potential acquisition.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Strategic.M&A']
    },
    {
        'text': "Subject: Budget variance explanation\nExplain why travel spend exceeded forecast and propose controls to prevent recurrence.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },
    {
        'text': "Subject: Forecasting cadence\nProvide weekly rolling forecast for the next 8 weeks; leadership wants earlier warning signals.",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Budget vs roadmap tension\nIf we cut infra spend, latency SLOs will suffer. Need decision: cost savings or reliability investment?",
        'true_labels': ['Financial.Strategy.Budget_Forecasting', 'Operational.Project.Technical_Blockers']
    },

    # =========================
    # Financial.Strategy.Revenue_Projections (10)
    # =========================
    {
        'text': "Subject: Revenue forecast update\nUpdating revenue projections: pipeline conversion down 5%, but expansion revenue up 8%. Revised model attached.",
        'true_labels': ['Financial.Strategy.Revenue_Projections']
    },
    {
        'text': "Subject: Quarterly sales forecast\nPlease submit your regional forecast: new ARR, renewals, churn risk, and upside deals.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Strategic.Customer_Acquisition']
    },
    {
        'text': "Subject: Pricing impact on revenue\nIf we shift to usage-based pricing, estimate revenue lift under conservative/base/aggressive adoption curves.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Board asks about guidance\nNeed guidance numbers for the board: expected ARR range, risk factors, and sensitivity to churn.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Revenue miss analysis\nWe missed forecast due to delayed enterprise renewal and lower conversion. Provide root cause and mitigation plan.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Expansion revenue model\nForecast revenue contribution from EMEA expansion: ramp schedule, hiring costs, and churn assumptions.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Strategic.Market_Expansion']
    },
    {
        'text': "Subject: Pipeline integrity\nRevenue forecast depends on CRM hygiene. Audit shows inflated probabilities—fix forecasting process.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Legal.All']
    },
    {
        'text': "Subject: Renewal risk\nTop 3 customers might churn if incident repeats. Update revenue projections and include downside scenario.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Legal.All']
    },
    {
        'text': "Subject: Investor model parity\nEnsure internal revenue projections match investor materials; discrepancies create credibility risk.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Revenue forecast dispute\nSales disagrees with finance's conservative churn estimate. Need alignment meeting and revised assumptions.",
        'true_labels': ['Financial.Strategy.Revenue_Projections', 'HR.Internal_Disputes']
    },

    # =========================
    # Financial.Strategy.Investment_Strategies (10)
    # =========================
    {
        'text': "Subject: Capital allocation\nProposal: invest in infra modernization to reduce long-term costs and improve reliability; ROI analysis attached.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Financial.Strategy.Budget_Forecasting']
    },
    {
        'text': "Subject: Funding decision\nWe should prioritize funding the compliance roadmap over new features this quarter due to risk and enterprise demand.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Legal.All']
    },
    {
        'text': "Subject: Investment memo—new product line\nRequesting approval to invest $200k in building the new product line prototype; success criteria included.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Acquire vs build\nDecision: acquire VendorCo's tech or build internally. Provide cost, timeline, and strategic risks for both options.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Strategic.M&A', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: R&D budget allocation\nAllocate more budget to model experimentation to improve accuracy; current mislabels harm trust and retention.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Portfolio priorities\nGiven limited funds, choose: customer acquisition spend, pricing overhaul, or security hardening. Need ranked options.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Strategic.Customer_Acquisition', 'Strategic.Pricing_Models']
    },
    {
        'text': "Subject: Investment risk assessment\nIf we invest in expansion, what's the downside if regulations slow entry? Include sensitivity and break-even analysis.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Strategic.Market_Expansion', 'Legal.All']
    },
    {
        'text': "Subject: Board approval for spend\nBoard needs to approve the capex line item for the new data center footprint. Provide justification and timeline.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Strategic.Board_Communications']
    },
    {
        'text': "Subject: Investment in retention\nRetention bonuses may be cheaper than replacing senior engineers. Provide cost comparison and attrition risk.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Financial.Accounting.Bonuses', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Legal cost planning\nIf litigation proceeds, we may need to increase legal spend. Propose an investment strategy to manage exposure.",
        'true_labels': ['Financial.Strategy.Investment_Strategies', 'Financial.Strategy.Budget_Forecasting', 'Legal.All']
    },

    # =========================
    # Operational.Project.Technical_Blockers (10)
    # =========================
    {
        'text': "Subject: Blocker—API dependency\nWe can't ship until IdentityService exposes the new endpoint. Current API returns inconsistent auth scopes.",
        'true_labels': ['Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Release blocked\nBuild pipeline is failing due to dependency conflicts. Need someone to own the upgrade path today.",
        'true_labels': ['Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Security review blocker\nWe're blocked on the security team signing off on the redaction logic. Without approval, launch is paused.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: Data quality issue\nModel training is blocked because labels are inconsistent and missing negatives. Need relabeling sprint.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Infra constraint\nWe hit GPU quota limits; experiments are queued for days. Need budget approval or better scheduling.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'Financial.Strategy.Budget_Forecasting', 'R&D.Technical.Experiments']
    },
    {
        'text': "Subject: Vendor outage\nThird-party email ingestion API is down. Until it's restored, ingestion tests cannot proceed.",
        'true_labels': ['Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Compliance gating\nWe can't deploy until we implement audit logging and retention controls required for SOX readiness.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'Legal.All']
    },
    {
        'text': "Subject: Conflicting requirements\nProduct wants speed, Legal wants stricter access constraints. This disagreement is blocking final architecture decision.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'HR.Internal_Disputes', 'Legal.All']
    },
    {
        'text': "Subject: Bug in prod\nCritical bug causes misclassification of privileged emails. Must fix before next customer pilot.",
        'true_labels': ['Operational.Project.Technical_Blockers', 'R&D.Technical.Models', 'Legal.All']
    },
    {
        'text': "Subject: Timeline risk\nWe're blocked on data ingestion parsing edge cases; without it, downstream tagging accuracy is unreliable.",
        'true_labels': ['Operational.Project.Technical_Blockers']
    },

    # =========================
    # Operational.Project.Progress_Updates (10)
    # =========================
    {
        'text': "Subject: Weekly status\nThis week: finished pattern matchers, improved NER precision, and deployed the new ingestion controller to staging.",
        'true_labels': ['Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Milestone achieved\nWe completed the first end-to-end run on 500 emails and generated a draft brief. Next: expand label coverage.",
        'true_labels': ['Operational.Project.Progress_Updates', 'R&D.Technical.Prototypes']
    },
    {
        'text': "Subject: Sprint update\nOn track: 6/8 stories done. Blocked: auth integration. Risks: audit logging not implemented yet.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Incident postmortem summary\nRoot cause identified, mitigation deployed, and monitoring added. Customer impact: 23 minutes downtime.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Legal.All']
    },
    {
        'text': "Subject: Release notes\nv1.2 shipped: improved redaction, added role-based access checks, and new dashboard charts.",
        'true_labels': ['Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Pilot progress\nPilot customer onboarded; first feedback is positive but they want more transparency on model decisions.",
        'true_labels': ['Operational.Project.Progress_Updates', 'R&D.Technical.Models']
    },
    {
        'text': "Subject: Roadmap update\nWe moved M&A label work to next sprint and pulled forward compliance artifacts due to audit schedule.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Strategic.M&A', 'Legal.All']
    },
    {
        'text': "Subject: Staffing update\nWe hired one contractor to accelerate ingestion work. Expected to improve throughput by next sprint.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Financial.Accounting.Firing_Hiring']
    },
    {
        'text': "Subject: Metrics update\nLatency p95 improved from 6.4s to 5.9s. Next optimization: caching + better chunk boundaries.",
        'true_labels': ['Operational.Project.Progress_Updates', 'R&D.Technical.Algorithms']
    },
    {
        'text': "Subject: Executive summary\nOverall: green. Key risk: reporting deadline next month; mitigation plan in progress.",
        'true_labels': ['Operational.Project.Progress_Updates', 'Strategic.Board_Communications', 'Legal.All']
    },

    # =========================
    # Personal_Life.Health_Disclosures (10)
    # =========================
    {
        'text': "Subject: Time off for appointment\nI have a doctor's appointment Wednesday morning and will be offline 9-11am.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: Medical leave\nI'm having surgery next month and will need two weeks of medical leave. I'll hand off my projects before then.",
        'true_labels': ['Personal_Life.Health_Disclosures', 'Operational.Project.Progress_Updates']
    },
    {
        'text': "Subject: Health update\nI've been dealing with migraines and may need flexibility for a bit. I'll keep you posted on availability.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: PT schedule\nPhysical therapy twice a week means I'll block 4-5pm Tuesdays/Thursdays for the next month.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: Ergonomic accommodation\nMy wrist pain is flaring up; requesting an ergonomic keyboard and setup to prevent further injury.",
        'true_labels': ['Personal_Life.Health_Disclosures', 'Legal.All']
    },
    {
        'text': "Subject: Medication side effects\nNew medication is making me drowsy in mornings—best time for meetings is afternoons this week.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: Confidential health matter\nI'm managing a health condition and may need intermittent time off. Please keep this private.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: Mental health day\nI'm taking a mental health day tomorrow and will respond Friday.",
        'true_labels': ['Personal_Life.Health_Disclosures']
    },
    {
        'text': "Subject: COVID exposure\nI was exposed and am getting tested. I'll work remote until results come back.",
        'true_labels': ['Personal_Life.Health_Disclosures', 'Legal.All']
    },
    {
        'text': "Subject: Recovery update\nI'm back part-time after treatment; I can handle light tasks but not on-call this week.",
        'true_labels': ['Personal_Life.Health_Disclosures', 'Operational.Project.Technical_Blockers']
    },

    # =========================
    # Personal_Life.Crisis_Content (10)
    # =========================
    {
        'text': "Subject: Family emergency\nI have a family emergency and need to step away immediately. I'll be offline for the rest of the day.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Urgent—hospital\nMy parent was taken to the hospital. I'm leaving now and will update you when I can.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Housing crisis\nMy apartment flooded overnight and I'm dealing with emergency repairs. I may miss meetings today.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Bereavement\nI had a death in the family and will be taking bereavement leave starting tomorrow.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Domestic emergency\nI'm handling an urgent personal situation at home and won't be reachable for a few hours.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Travel disruption\nMy flight was cancelled and I'm stuck overnight. I can't present at the meeting—please cover for me.",
        'true_labels': ['Personal_Life.Crisis_Content', 'Operational.Project.Technical_Blockers']
    },
    {
        'text': "Subject: Safety concern\nThere was an incident near my home and I'm coordinating with authorities. I'll be offline.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Childcare emergency\nDaycare closed unexpectedly and I have no backup today. I'll be intermittent and may miss standup.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Financial emergency\nI'm dealing with an unexpected urgent personal financial issue today and need to step away briefly.",
        'true_labels': ['Personal_Life.Crisis_Content']
    },
    {
        'text': "Subject: Crisis + handoff\nI can't work this week due to a personal crisis. Please reassign my open tickets and handle customer follow-ups.",
        'true_labels': ['Personal_Life.Crisis_Content', 'Operational.Project.Progress_Updates']
    },
]