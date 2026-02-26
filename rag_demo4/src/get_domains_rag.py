"""Local domain router used by rag_demo4.

This keeps routing logic inside rag_demo4 while reusing ingestion taxonomy
and zero-shot classifier from the monorepo Ingestion package.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_repo_root_on_path() -> None:
    # .../clairos/rag_demo4/src/get_domains_rag.py -> repo root is .../clairos
    repo_root = Path(__file__).resolve().parents[2]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


_ensure_repo_root_on_path()

from Ingestion.dataTaggers.ZeroShot import zero_shot_classify  # noqa: E402
from Ingestion.Schemas.taxonomy import CATEGORY_THRESHOLDS, ZERO_SHOT_LABEL_GROUPS  # noqa: E402

_DEFAULT_THRESHOLD = 0.5

LABEL_TO_RAG_DOMAIN: dict[str, list[str]] = {
    "Strategic.M&A": ["business_strategy"],
    "Strategic.Market_Expansion": ["business_strategy"],
    "Strategic.Pricing_Models": ["business_strategy", "company_financial_strategy"],
    "Strategic.Customer_Acquisition": ["business_strategy"],
    "Strategic.Competitive_Analysis": ["business_strategy"],
    "Strategic.Board_Communications": ["business_strategy"],
    "HR.Performance_Reviews": ["all_hr"],
    "HR.Internal_Disputes": ["all_hr"],
    "R&D.Technical.Experiments": ["technical_randd"],
    "R&D.Technical.Algorithms": ["technical_randd"],
    "R&D.Technical.Models": ["technical_randd"],
    "R&D.Technical.Prototypes": ["technical_randd"],
    "R&D.IP.Patentable_Ideas": ["scientific_and_ip_randd"],
    "R&D.IP.Proprietary_Formulas": ["scientific_and_ip_randd"],
    "Financial.Accounting.Salary_Negotiations": ["accounting"],
    "Financial.Accounting.Firing_Hiring": ["accounting"],
    "Financial.Accounting.Bonuses": ["accounting"],
    "Financial.Strategy.Budget_Forecasting": ["company_financial_strategy"],
    "Financial.Strategy.Revenue_Projections": ["company_financial_strategy"],
    "Financial.Strategy.Investment_Strategies": ["company_financial_strategy"],
    "Operational.Project.Technical_Blockers": ["project_metadata"],
    "Operational.Project.Progress_Updates": ["project_metadata"],
    "Personal_Life.Health_Disclosures": [],
    "Personal_Life.Crisis_Content": [],
}


def get_domains_for_rag(query: str) -> list[str]:
    domains: set[str] = set()

    for labels_dict in ZERO_SHOT_LABEL_GROUPS.values():
        desc_to_key = {desc: key for key, desc in labels_dict.items()}
        candidate_labels = list(labels_dict.values())
        result = zero_shot_classify(query, candidate_labels, multi_label=True)

        for label_desc, score in zip(result["labels"], result["scores"]):
            category_key = desc_to_key.get(label_desc)
            if category_key is None:
                continue
            threshold = CATEGORY_THRESHOLDS.get(category_key, _DEFAULT_THRESHOLD)
            if score < threshold:
                continue
            domains.update(LABEL_TO_RAG_DOMAIN.get(category_key, []))

    return sorted(domains)
