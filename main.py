from dotenv import load_dotenv
from coordinator import run_deep_research


def main():
    load_dotenv()
    user_query = input("Enter your research query: ")
    result = run_deep_research(user_query)
    with open("research_result.md", "w") as f:
        f.write(result)

    print("\nResearch result saved to research_result.md")


if __name__ == "__main__":
    main()
