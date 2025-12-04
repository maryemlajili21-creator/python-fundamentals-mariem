from __future__ import annotations

import pandas as pd
import requests  # type: ignore[import-untyped]
from lxml import etree


def fetch_arxiv_to_dataframe(query: str, max_results: int = 10) -> pd.DataFrame:
    url = "http://export.arxiv.org/api/query"
    params: dict[str, str] = {
        "search_query": query,
        "max_results": str(max_results),
    }

    response = requests.get(url, params=params, timeout=10)
    xml_data = response.content

    root = etree.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    articles = []

    for entry in root.findall("atom:entry", ns):
        arxiv_id = entry.findtext("atom:id", namespaces=ns).split("/")[-1]
        title = entry.findtext("atom:title", namespaces=ns)
        summary = entry.findtext("atom:summary", namespaces=ns)
        author_name = entry.findtext("atom:author/atom:name", namespaces=ns)

        articles.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "summary": summary,
                "author_full_name": author_name,
                "author_title": "Researcher",
                "file_path": "",
                "content": None,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
            }
        )

    return pd.DataFrame(articles, dtype="string")
