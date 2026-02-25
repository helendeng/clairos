from dataclasses import dataclass, field
from typing import List
from enum import Enum

from Ingestion.Schemas.taxonomy import CategoryKey

###############################################################################
############################## Output Schemas #################################
@dataclass
class SourceInfo:
    """The source variable in class OutputSchema"""
    email_id: str
    sender: List[str]
    subject: str
    cc: List[str]
    bcc: List[str]
    timestamp: str

@dataclass
class OutputSchema:
    """Normalized output format of all tagging components"""
    chunk_id: int
    domain: str
    sub_domain: str
    text: str
    source: SourceInfo


###############################################################################
############################### Input Schemas #################################
@dataclass 
class EmailRecord:
    """Normalized input that we will feed the components"""
    email_id: str
    sender: str
    subject: str
    cc: List[str]
    bcc: List[str]
    body: str
    timestamp: str



###############################################################################
########################## InterComponent Schemas #############################
@dataclass
class Chunk:
    """Normalized chunking format"""
    chunk_id: int
    text: str


@dataclass
class TagHit:
    """A single tagged piece of data and all it carries"""
    category_key: CategoryKey
    evidence_text: str
    start_pos: int
    end_pos: int
    confidence: float