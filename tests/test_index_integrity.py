"""
Pytest integration tests for soroban-error-index schema and tools.
"""

import os
import sys
import glob
import pytest

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from tools.validate_schema import validate_all
from tools.search import search_entries, load_all_entries

def test_all_entries_schema_valid():
    """Verify all markdown entries strictly pass the JSON schema."""
    is_valid, errors = validate_all(root_dir)
    assert is_valid is True
    assert len(errors) == 0

def test_entry_count_at_least_29():
    """Verify minimum 29 testnet-verified entries are present."""
    pattern = os.path.join(root_dir, "entries", "**", "*.md")
    files = glob.glob(pattern, recursive=True)
    assert len(files) >= 29

def test_ranked_search():
    """Verify ranked search correctly scores and retrieves error entries."""
    entries = load_all_entries(root_dir)
    results = search_entries(entries, query="arithmetic", rank=True)
    assert len(results) > 0
    assert results[0]["id"] == "arith-error"
    assert results[0]["_score"] > 20.0

def test_storage_and_unwrap_search():
    """Verify search returns storage and panic error entries."""
    entries = load_all_entries(root_dir)
    results = search_entries(entries, query="unwrap", rank=True)
    assert len(results) > 0
    found_ids = [r["id"] for r in results]
    assert "option-unwrap-none" in found_ids or "map-key-not-found" in found_ids
