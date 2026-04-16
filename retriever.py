"""Compatibility wrapper for older imports.

The actual implementation now lives in policy_data.py and rag_engine.py.
"""

from policy_data import build_policy_corpus, chunk_text, fetch_all_policies, fetch_policy_text
from config import POLICY_LINKS as policy_links
from rag_engine import generate_response, get_retrieval_state, get_text_embedding, retrieve_relevant_chunks
