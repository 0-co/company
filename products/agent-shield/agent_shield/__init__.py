"""
agent-shield — security scanner for AI agent skills and plugins.

Quick start:
  from agent_shield import Scanner
  results = Scanner().scan_directory("./skills")
  for r in results:
      print(r.skill_name, r.risk_level, len(r.findings))
"""

from .scanner import Finding, ScanResult, Scanner, create_manifest, verify_manifest

__version__ = "0.1.0"

__all__ = [
    "Scanner",
    "ScanResult",
    "Finding",
    "create_manifest",
    "verify_manifest",
]
