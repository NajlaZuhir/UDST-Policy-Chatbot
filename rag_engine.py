from __future__ import annotations

import os
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Sequence

import faiss
import numpy as np
from mistralai.client.models.usermessage import UserMessage
from mistralai.client.sdk import Mistral

from config import (
    CHAT_MODEL,
    EMBEDDING_BATCH_SIZE,
    EMBEDDING_MODEL,
    EMBEDDING_RATE_LIMIT_DELAY_SECONDS,
    EMBEDDING_RETRY_DELAY_SECONDS,
    EMBEDDING_RETRY_LIMIT,
    MIN_CHUNK_LENGTH,
    POLICY_LINKS,
    RETRIEVAL_K,
)
from policy_data import build_policy_corpus, fetch_all_policies


@dataclass(frozen=True)
class RetrievalState:
    policy_chunks: Sequence[str]
    index: faiss.IndexFlatL2


def _load_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key and key not in os.environ:
            os.environ[key] = value


def _get_api_key() -> str:
    _load_env_file()
    api_key = os.getenv("MISTRAL_API_KEY")
    if api_key:
        return api_key

    try:
        import streamlit as st

        return st.secrets["MISTRAL_API_KEY"]
    except Exception as exc:
        raise RuntimeError(
            "MISTRAL_API_KEY is missing. Set it in your environment or Streamlit secrets."
        ) from exc


def _create_client() -> Mistral:
    return Mistral(api_key=_get_api_key())


def _extract_answer_text(response) -> str:
    try:
        message = response.choices[0].message
        content = message.content if message is not None else ""
    except Exception:
        return ""

    if isinstance(content, str):
        return content.strip()

    return str(content).strip()


def get_text_embedding(list_txt_chunks: Sequence[str], batch_size: int = EMBEDDING_BATCH_SIZE) -> List[List[float]]:
    client = _create_client()
    embeddings: List[List[float]] = []

    for start in range(0, len(list_txt_chunks), batch_size):
        batch = list_txt_chunks[start: start + batch_size]

        retries = EMBEDDING_RETRY_LIMIT
        while retries > 0:
            try:
                embeddings_batch_response = client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    inputs=list(batch),
                )
                embeddings.extend([item.embedding for item in embeddings_batch_response.data])
                time.sleep(EMBEDDING_RETRY_DELAY_SECONDS)
                break
            except Exception as exc:
                retries -= 1
                if retries == 0:
                    raise
                if "429" in str(exc):
                    time.sleep(EMBEDDING_RATE_LIMIT_DELAY_SECONDS)

    return embeddings


@lru_cache(maxsize=1)
def get_retrieval_state() -> RetrievalState:
    policy_texts = fetch_all_policies()
    policy_chunks, _policy_sources = build_policy_corpus(policy_texts)

    text_embeddings = get_text_embedding(policy_chunks)
    if not text_embeddings:
        raise RuntimeError("No embeddings were retrieved for the policy corpus.")

    embeddings = np.asarray(text_embeddings, dtype=np.float32)
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return RetrievalState(policy_chunks=tuple(policy_chunks), index=index)


def retrieve_relevant_chunks(query: str) -> List[str]:
    retrieval_state = get_retrieval_state()
    query_embedding = np.asarray(get_text_embedding([query]), dtype=np.float32)
    distances, indices = retrieval_state.index.search(query_embedding, k=RETRIEVAL_K)

    confidence_scores = 1 / (1 + distances[0])

    if confidence_scores[0] > 0.9:
        top_k = 2
    elif confidence_scores[0] > 0.7:
        top_k = 4
    else:
        top_k = 6

    retrieved_chunks = [
        retrieval_state.policy_chunks[index]
        for index in indices[0][:top_k]
        if index < len(retrieval_state.policy_chunks)
    ]
    return [chunk for chunk in retrieved_chunks if len(chunk) > MIN_CHUNK_LENGTH]


def _match_policies(user_query: str) -> List[str]:
    query_keywords = user_query.lower().split()
    matches: List[str] = []

    for policy_name in POLICY_LINKS:
        policy_keywords = policy_name.lower().split()
        if any(keyword in query_keywords for keyword in policy_keywords):
            matches.append(policy_name)

    return matches


def generate_response(user_query: str) -> str:
    retrieved_chunks = retrieve_relevant_chunks(user_query)
    relevant_policies = _match_policies(user_query)

    prompt = f"""
    You are an AI assistant providing official university policy information.
    Provide concise, to-the-point answers. Only include the most relevant details.

    Context:
    ---------------------
    {' '.join(retrieved_chunks)}
    ---------------------

    - Answer the user query in 2-3 sentences max.
    - If there are specific steps, summarize them in bullet points.
    - Do NOT include unnecessary background details.
    - If certain details are missing, mention where users can find them.

    User Query: {user_query}
    Answer:
    """

    client = _create_client()
    messages = [UserMessage(content=prompt)]

    response = client.chat.complete(
        model=CHAT_MODEL,
        messages=messages,
    )
    answer = _extract_answer_text(response)

    if relevant_policies:
        best_match = max(
            relevant_policies,
            key=lambda policy_name: sum(word in user_query.lower() for word in policy_name.lower().split()),
        )
        policy_links_html = f"🔗 **More Information:** [Read the full {best_match} here]({POLICY_LINKS[best_match]})"
        answer = f"{answer}\n\n{policy_links_html}"

    return answer