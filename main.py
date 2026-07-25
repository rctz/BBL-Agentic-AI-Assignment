import argparse

from langchain_core.messages import HumanMessage

from src.agents.generator import build_generator

BANNER = "RAG Agent - type 'exit'/'quit' or Ctrl-D to leave"


def run_query(app, query: str) -> str:
    result = app.invoke({"messages": [HumanMessage(content=query)]})
    return result["messages"][-1].content


def cli_mode(app, query: str) -> None:
    print(run_query(app, query))


def repl_mode(app) -> None:
    print(BANNER)
    try:
        while True:
            line = input("> ").strip()
            if not line or line.lower() in ("exit", "quit"):
                break
            print("Report:")
            try:
                print(run_query(app, line))
            except Exception as e:
                print(f"Error: {e}")
            print()
    except (EOFError, KeyboardInterrupt):
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="BBL RAG Agent")
    parser.add_argument("query", nargs="?", default=None, help="Single query string")
    args = parser.parse_args()

    app = build_generator()

    if args.query is not None:
        cli_mode(app, args.query)
    else:
        repl_mode(app)


if __name__ == "__main__":
    main()
