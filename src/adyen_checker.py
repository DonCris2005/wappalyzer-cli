#!/usr/bin/env python3
"""Bulk Adyen detection tool.

Processes a text file with one domain per line, checks if each domain
uses Adyen using the Wappalyzer library and writes results to
``goods.txt`` and ``bads.txt``.

The script reads the input file in a streaming fashion and supports
multi-threaded execution.
"""

from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

from Wappalyzer import Wappalyzer, WebPage


# Global Wappalyzer instance reused across threads
_wappalyzer = None

def _prepare_url(domain: str) -> str:
    domain = domain.strip()
    if not domain:
        return ""
    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = "http://" + domain
    return domain


def _init_wappalyzer() -> None:
    global _wappalyzer
    if _wappalyzer is None:
        _wappalyzer = Wappalyzer.latest()


def check_domain(domain: str) -> tuple[str, bool]:
    """Return tuple of domain and whether it uses Adyen."""
    _init_wappalyzer()
    url = _prepare_url(domain)
    if not url:
        return domain, False
    try:
        webpage = WebPage.new_from_url(url)
        technologies = _wappalyzer.analyze(webpage)
        return domain, "Adyen" in technologies
    except Exception:
        return domain, False


def process_file(path: str, goods_path: str, bads_path: str, workers: int) -> None:
    total = good = bad = 0
    with open(path, "r") as infile, \
            open(goods_path, "w") as goodfile, \
            open(bads_path, "w") as badfile, \
            ThreadPoolExecutor(max_workers=workers) as executor:
        domain_iter = (line.strip() for line in infile if line.strip())
        for domain, uses in executor.map(check_domain, domain_iter, chunksize=1):
            total += 1
            if uses:
                good += 1
                goodfile.write(domain + "\n")
            else:
                bad += 1
                badfile.write(domain + "\n")
            if total % 1000 == 0:
                print(f"Processed: {total}, adyen: {good}", file=sys.stderr)
    print(
        f"Finished. Total: {total}, adyen: {good}, others: {bad}",
        file=sys.stderr,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect Adyen usage for domains")
    parser.add_argument(
        "-i", "--input", required=True, help="Input file containing domains"
    )
    parser.add_argument(
        "--workers", type=int, default=4, help="Number of concurrent threads"
    )
    parser.add_argument(
        "--goods", default="goods.txt", help="File for domains using Adyen"
    )
    parser.add_argument(
        "--bads", default="bads.txt", help="File for domains not using Adyen"
    )
    args = parser.parse_args(argv)

    process_file(args.input, args.goods, args.bads, args.workers)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
