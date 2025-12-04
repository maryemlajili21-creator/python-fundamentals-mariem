from assignement8.pipeline import run_pipeline

print(">>> main.py loaded")


def main() -> None:
    print("Running full ArXiv pipeline...")
    df = run_pipeline("machine learning", max_results=10)
    print(df[["title", "article_id"]])


if __name__ == "__main__":
    print(">>> __main__ triggered")
    main()
