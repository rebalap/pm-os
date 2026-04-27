#!/usr/bin/env python3
"""
Tavily Search CLI — PM-OS Tool
Usage:
  python3 tools/tavily-search.py "your search query"
  python3 tools/tavily-search.py "your query" --depth advanced
  python3 tools/tavily-search.py "your query" --topic news
  python3 tools/tavily-search.py "your query" --max-results 10
  python3 tools/tavily-search.py "your query" --raw
  python3 tools/tavily-search.py "your query" --include-domains "nih.gov,pubmed.ncbi.nlm.nih.gov"

Loads TAVILY_API_KEY from:
  1. Environment variable TAVILY_API_KEY
  2. .env file in the pm-os directory
"""

import sys
import os
import json
import argparse
from pathlib import Path


def load_env():
    """Load .env from pm-os root directory."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())


def run_search(
    query,
    search_depth="basic",
    topic="general",
    max_results=5,
    include_domains=None,
    exclude_domains=None,
    include_answer=True,
    include_raw_content=False,
    output_raw=False,
):
    try:
        from tavily import TavilyClient
    except ImportError:
        print("ERROR: tavily-python not installed. Run: pip3 install tavily-python")
        sys.exit(1)

    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        print("ERROR: TAVILY_API_KEY not set. Add it to pm-os/.env or export it.")
        sys.exit(1)

    client = TavilyClient(api_key=api_key)

    kwargs = {
        "query": query,
        "search_depth": search_depth,
        "topic": topic,
        "max_results": max_results,
        "include_answer": include_answer,
        "include_raw_content": include_raw_content,
    }
    if include_domains:
        kwargs["include_domains"] = include_domains
    if exclude_domains:
        kwargs["exclude_domains"] = exclude_domains

    response = client.search(**kwargs)

    if output_raw:
        print(json.dumps(response, indent=2))
        return

    # Formatted output
    print(f"\n{'='*70}")
    print(f"TAVILY SEARCH: {query}")
    print(f"Depth: {search_depth} | Topic: {topic} | Results: {max_results}")
    print(f"{'='*70}\n")

    # AI answer summary
    if include_answer and response.get("answer"):
        print("SUMMARY ANSWER")
        print("-" * 40)
        print(response["answer"])
        print()

    # Results
    results = response.get("results", [])
    print(f"TOP RESULTS ({len(results)})")
    print("-" * 40)
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r.get('title', 'No title')}")
        print(f"    URL: {r.get('url', '')}")
        score = r.get("score", 0)
        print(f"    Relevance: {score:.2f}" if score else "")
        content = r.get("content", "")
        if content:
            # Truncate long content for CLI display
            display = content[:400] + "..." if len(content) > 400 else content
            print(f"    {display}")

    print(f"\n{'='*70}")
    print(f"Images: {len(response.get('images', []))} | "
          f"Response time: {response.get('response_time', 'N/A')}s")
    print(f"{'='*70}\n")


def main():
    load_env()

    parser = argparse.ArgumentParser(
        description="Tavily Search CLI for PM-OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--depth",
        choices=["basic", "advanced"],
        default="basic",
        help="Search depth (basic=fast, advanced=thorough). Default: basic",
    )
    parser.add_argument(
        "--topic",
        choices=["general", "news", "finance"],
        default="general",
        help="Topic domain. Default: general",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=5,
        help="Number of results to return (1–20). Default: 5",
    )
    parser.add_argument(
        "--include-domains",
        help="Comma-separated list of domains to include (e.g. 'nih.gov,pubmed.ncbi.nlm.nih.gov')",
    )
    parser.add_argument(
        "--exclude-domains",
        help="Comma-separated list of domains to exclude",
    )
    parser.add_argument(
        "--no-answer",
        action="store_true",
        help="Skip AI-generated answer summary",
    )
    parser.add_argument(
        "--raw-content",
        action="store_true",
        help="Include full raw page content in results",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw JSON response",
    )

    args = parser.parse_args()

    include_domains = (
        [d.strip() for d in args.include_domains.split(",")]
        if args.include_domains
        else None
    )
    exclude_domains = (
        [d.strip() for d in args.exclude_domains.split(",")]
        if args.exclude_domains
        else None
    )

    run_search(
        query=args.query,
        search_depth=args.depth,
        topic=args.topic,
        max_results=args.max_results,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
        include_answer=not args.no_answer,
        include_raw_content=args.raw_content,
        output_raw=args.raw,
    )


if __name__ == "__main__":
    main()
