import re
from functools import lru_cache

from langchain_core.tools import tool

from settings import settings

STOP_WORDS = frozenset(
    "the a an of to and in on for is are was were with at by from as what how "
    "when who where why do does did can could should would will i you he she it "
    "we they me him her them my your tell give show list explain about".split()
)

# Remove any syntax from the words
_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


@lru_cache(maxsize=4)
def load_kb(path: str = settings.kb_path) -> list[str]:
    """Read knowledge-base text file, split on blank lines, return non-empty paragraphs."""
    with open(path) as f:
        raw = f.read()
    paragraphs = [p.strip() for p in raw.split("\n\n")]
    return [p for p in paragraphs if p]


def _tokenize(text: str) -> set[str]:
    """Tokenize, lowercase, drop stop words."""
    return {tok for tok in _TOKEN_RE.findall(text.lower()) if tok not in STOP_WORDS}


def search_kb(query: str, top_k: int = 3) -> list[str]:
    """Return top_k most-relevant paragraphs from the knowledge base for *query*."""
    paragraphs = load_kb()
    if not paragraphs:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scored = []
    for para in paragraphs:
        para_tokens = _tokenize(para)
        # Check overlap wording
        overlap = len(query_tokens & para_tokens)
        if overlap:
            scored.append((overlap, para))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [para for _, para in scored[:top_k]]


@tool
def retrieve_from_kb(query: str) -> str:
    """Find relevant paragraphs in the US stock knowledge base.

    Always call this before answering questions about a company, ticker, or
    financial figure. For multi-company questions, call once per company.
    """
    results = search_kb(query)
    if not results:
        return "[retrieve_from_kb] No relevant information found in the knowledge base."
    return "\n\n---\n\n".join(results)
