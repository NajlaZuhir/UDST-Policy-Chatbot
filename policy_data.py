from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import requests
from bs4 import BeautifulSoup

from config import CHUNK_SIZE, POLICY_LINKS


def fetch_policy_text(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator=" ").replace("\n", " ").strip()

    return " ".join(text.split())


def fetch_all_policies(policy_links: Dict[str, str] = POLICY_LINKS) -> Dict[str, str]:
    return {url: fetch_policy_text(url) for url in policy_links.values()}


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE) -> List[str]:
    return [text[index: index + chunk_size] for index in range(0, len(text), chunk_size)]


def build_policy_corpus(
    policy_texts: Dict[str, str],
    chunk_size: int = CHUNK_SIZE,
) -> Tuple[List[str], List[str]]:
    policy_chunks: List[str] = []
    policy_sources: List[str] = []

    for url, text in policy_texts.items():
        chunks = chunk_text(text, chunk_size=chunk_size)
        policy_chunks.extend(chunks)
        policy_sources.extend([url] * len(chunks))

    return policy_chunks, policy_sources