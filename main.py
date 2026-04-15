import os
import argparse
import getpass
from coordinator import run_deep_research


def main():
    parser = argparse.ArgumentParser(description="Run deep research coordinator")
    parser.add_argument("query", nargs="?", default=None, help="Research query to run")
    args = parser.parse_args()

    if os.environ.get("HF_TOKEN") is None:
        os.environ["HF_TOKEN"] = getpass.getpass("Huggingface Token: ")
    if os.environ.get("FIRECRAWL_API_KEY") is None:
        os.environ["FIRECRAWL_API_KEY"] = getpass.getpass("Firecrawl API Key: ")

    user_query = args.query or input("Research query: ")

    result = run_deep_research(user_query)
    print("\nFinal synthesized report:\n")
    print(result)


if __name__ == "__main__":
    main()
