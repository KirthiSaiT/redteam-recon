from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime

class ScanRequest(BaseModel):
    domain: str
    scan_types: List[str] = ["subdomains", "ports", "osint"]  # default to all

class SubdomainResult(BaseModel):
    subdomains: List[str]
    count: int

class PortResult(BaseModel):
    ip: str
    ports: List[int]
    banners: Optional[Dict[str, str]] = None

class ScanResult(BaseModel):
    id: str
    domain: str
    status: str = "pending"
    timestamp: datetime
    subdomains: Optional[SubdomainResult] = None
    ports: Optional[List[PortResult]] = None
    technologies: Optional[List[str]] = None
    directories: Optional[List[str]] = None
    screenshots: Optional[Dict[str, str]] = None # subdomain -> b64
    vulnerabilities: Optional[List[str]] = None

