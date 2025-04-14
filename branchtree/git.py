import re
import subprocess
from typing import Iterable


class GitError(Exception):
    def __init__(self, code: int) -> None:
        super().__init__(f"Command failed with code {code}")
        self.code = code


class GitBranch:
    def __init__(self, name: str, sha: str) -> None:
        self.name = name
        self.sha = sha

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"GitBranch(name='{self.name}', sha='{self.sha}')"


def _run_cmd(command: list[str]) -> list[str]:
    try:
        return [
            line.decode().strip()
            for line in subprocess.check_output(command).splitlines()
        ]
    except subprocess.CalledProcessError as exc:
        raise GitError(exc.returncode) from exc


def _run_cmd_code(command: list[str]) -> int:
    try:
        subprocess.check_call(command)
        return 0
    except subprocess.CalledProcessError as exc:
        return exc.returncode


def _check_regex(regex: str | Iterable[str] | None, value: str) -> bool:
    if regex:
        if isinstance(regex, Iterable):
            return all(re.search(r, value) for r in regex)
        return bool(re.search(regex, value))
    return True


def get_branches(regex: str | Iterable[str] | None = None) -> list[GitBranch]:
    # run git shell command to get all branches
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    return [branch for branch in branches if _check_regex(regex, branch.name)]


def get_sha_of_rev(rev: str) -> str | None:
    try:
        return _run_cmd(["git", "rev-parse", "--verify", "--short", "--quiet", rev])[0]
    except GitError:
        return None


def get_contains(name: str, regex: str | Iterable[str] | None = None) -> list[GitBranch]:
    # run git shell command to get all branches that contain a specific branch
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--contains",
            name,
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    sha_of_name = get_sha_of_rev(name)

    # filter out self
    branches = [branch for branch in branches if branch.sha != sha_of_name]

    return [branch for branch in branches if _check_regex(regex, branch.name)]


def get_merged(name: str, regex: str | Iterable[str] | None = None) -> list[GitBranch]:
    # run git shell command to get all branches that contain a specific branch
    output = _run_cmd(
        [
            "git",
            "branch",
            "--all",
            "--merged",
            name,
            "--format=%(refname:short) %(objectname:short)",
        ]
    )
    branches = [GitBranch(*line.split()) for line in output]

    return [branch for branch in branches if _check_regex(regex, branch.name)]


def tag_exists(tag: str) -> bool:
    return _run_cmd_code(["git", "show-ref", "--quiet", "--tags", tag]) == 0
