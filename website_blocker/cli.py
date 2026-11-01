"""Command-line interface."""
import argparse
import sys

from . import hosts
from .classifier import CATEGORIES, classify
from .scraper import scrape


def cmd_block(args):
    sites = args.sites or input("Websites to block (space separated): ").split()
    print("Blocked:", ", ".join(hosts.block(sites)))


def cmd_unblock(args):
    remaining = hosts.unblock(args.sites)
    print("Still blocked:", ", ".join(remaining) or "(none)")


def cmd_list(_):
    blocked = hosts.get_blocked()
    print("\n".join(blocked) if blocked else "No sites blocked.")


def cmd_clear(_):
    hosts.set_blocked([])
    print("All blocks removed.")


def cmd_scan(args):
    for url in args.urls:
        try:
            text = scrape(url)
        except Exception as e:
            print(f"[!] {url}: could not fetch ({e})")
            continue
        matched, scores = classify(text, args.threshold)
        wanted = set(args.categories) if args.categories else set(CATEGORIES)
        hits = [(c, n) for c, n in matched if c in wanted]
        print(f"{url}\n  scores: {scores or 'no pattern hits'}")
        if hits:
            print(f"  -> matches: {hits}")
            if args.block:
                hosts.block([url])
                print("  -> blocked")
        else:
            print("  -> no match, not blocked")


def build_parser():
    p = argparse.ArgumentParser(prog="website-blocker", description="Block websites via the hosts file.")
    sub = p.add_subparsers(dest="command", required=True)

    b = sub.add_parser("block", help="block one or more sites")
    b.add_argument("sites", nargs="*")
    b.set_defaults(func=cmd_block)

    u = sub.add_parser("unblock", help="unblock sites")
    u.add_argument("sites", nargs="+")
    u.set_defaults(func=cmd_unblock)

    sub.add_parser("list", help="show blocked sites").set_defaults(func=cmd_list)
    sub.add_parser("clear", help="remove all blocks").set_defaults(func=cmd_clear)

    s = sub.add_parser("scan", help="scrape sites and detect categories by pattern")
    s.add_argument("urls", nargs="+")
    s.add_argument("-c", "--categories", nargs="*", choices=list(CATEGORIES), help="only these categories")
    s.add_argument("-t", "--threshold", type=int, default=3, help="min pattern hits (default 3)")
    s.add_argument("--block", action="store_true", help="auto-block matching sites")
    s.set_defaults(func=cmd_scan)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except PermissionError:
        sys.exit("Permission denied: run as Administrator (Windows) or with sudo (Linux/macOS).")
