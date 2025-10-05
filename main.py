from src.document_processor import load_documents, display_document_info


def main() -> None:
    documents = load_documents("data/documents.json")
    for doc in documents:
        display_document_info(doc)


if __name__ == "__main__":
    main()
