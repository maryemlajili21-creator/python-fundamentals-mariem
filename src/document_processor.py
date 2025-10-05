from typing import List, Any
import json
from pydantic import BaseModel
from pathlib import Path


class Document(BaseModel):  # type: ignore[misc]
    id: int
    title: str
    pages: int
    tags: list[str]
    approved: bool
    metadata: dict[str, Any] | None = None  # optional field


def load_documents(file_path: str) -> List[Document]:
    """Load and validate documents from a JSON file."""
    path = Path(file_path)
    with path.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return [Document(**doc) for doc in raw_data]


def display_document_info(document: Document) -> None:
    """Display document information, handling missing fields gracefully."""
    print(f"\n📘 {document.title}")
    print(f"   ID: {document.id}")
    print(f"   Pages: {document.pages}")
    print(f"   Tags: {', '.join(document.tags)}")
    print(f"   Approved: {'Yes' if document.approved else 'No'}")

    if document.metadata:
        author = document.metadata.get("author", "Unknown")
        year = document.metadata.get("year", "Unknown")
        print(f"   Author: {author}, Year: {year}")
    else:
        print("   Author/Year: Not provided")
