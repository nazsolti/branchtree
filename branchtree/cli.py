import argparse
import sys
from typing import cast

from . import __version__, tree


class BranchtreeCliArgs(argparse.Namespace):
    regex: str | None
    local: bool | None
    remote: bool | None
    branch: str | None


parser = argparse.ArgumentParser(
    prog="branchtree",
    description="Get a tree representation of the branch hierarchy of the current git repository.",
)

parser.add_argument(
    "-V", "--version", action="version", version=f"%(prog)s {__version__}"
)
parser.add_argument("--regex", help="only show branches matching this regex")
parser.add_argument(
    "-l", "--local", action="store_true", help="only show local branches"
)
parser.add_argument(
    "-r",
    "--remote",
    action="store_true",
    help="only show remote branches from 'origin' (for differently named remotes, use --regex)",
)
parser.add_argument(
    "-b",
    "--branch",
    nargs="*",
    help="only show the specified branches and their children (if any)",
)
parser.add_argument(
    "-c",
    "--contains",
    nargs="*",
    help="only show branches which contain these branches (if more specified, show branches which contain all of them)",
)
parser.add_argument(
    "-t",
    "--tag",
    help="show for every branch whether it is included (merged into) the given tag",
)


def print_progress(
    progress: float, header: str = "", width: int = 20, clear=False
) -> None:
    filled_length = int(round(width * progress))
    bar = "=" * filled_length + " " * (width - filled_length)
    printable = f"{header}[{bar}] {(progress * 100):.0f}%"

    if clear:
        sys.stdout.write(f"\r{' ' * len(printable)}\r")
    else:
        sys.stdout.write(f"\r{printable}")

    sys.stdout.flush()


def get_args() -> BranchtreeCliArgs:
    return cast(BranchtreeCliArgs, parser.parse_args(namespace=BranchtreeCliArgs()))


def main() -> None:
    args = get_args()
    branchtree = tree.build_tree(args.local, args.remote, args.regex)
    tree.print_tree(branchtree, args.branch, args.contains, args.tag)
