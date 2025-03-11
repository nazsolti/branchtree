from . import git, cli


class TreeBranch(git.GitBranch):
    _children: dict[str, "TreeBranch"]

    def __init__(self, name: str, sha: str):
        super().__init__(name, sha)

        self._children: dict[str, "TreeBranch"] = {}

    def add_child(self, child: "TreeBranch"):
        if child.sha in self._children:
            return

        self._children[child.sha] = child

    def remove_child(self, child: "TreeBranch"):
        if child.sha not in self._children:
            return

        del self._children[child.sha]

    @property
    def children(self) -> list["TreeBranch"]:
        return list(self._children.values())

    def print_tree(self, _header="", _last=None):
        # ref: https://stackoverflow.com/a/76691030
        elbow, pipe, tee, blank = " └── ", " │   ", " ├── ", "     "
        if _last is None:
            print("🞄" + str(self))
        else:
            print(_header + (elbow if _last else tee) + str(self))
        for i, child in enumerate(self._children.values()):
            child.print_tree(
                _header=_header + (blank if _last else " " if _last is None else pipe),
                _last=i == len(self.children) - 1,
            )

    def __contains__(self, item: "TreeBranch") -> bool:
        return item.sha in self._children

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"BranchtreeBranch(name='{self.name}', sha='{self.sha}')"


def build_tree(
    local_only: bool | None = None,
    remote_only: bool | None = None,
    regex: str | None = None,
    progress=False,
) -> list[TreeBranch]:
    regexes = []

    if local_only:
        regexes.append(r"^(?!.*\/)")

    if remote_only:
        regexes.append(r"origin/")

    if regex:
        regexes.append(regex)

    tree: dict[str, TreeBranch] = {}

    # collect all branches matching the regexes
    for branch in git.get_branches(regexes):
        if branch.sha not in tree:
            tree[branch.sha] = TreeBranch(branch.name, branch.sha)
            continue
        tree[branch.sha].name += ", " + branch.name

    # build tree (add each branch as children to each of its parent)
    for i, branch in enumerate(tree.values()):
        progress and cli.print_progress(i / len(tree), header="Building tree... ")

        parents = git.get_parents(branch, regexes)

        for parent in parents:
            tree[parent.sha].add_child(branch)

    progress and cli.print_progress(1, header="Building tree... ", clear=True)

    # prune tree (remove duplicates, i.e. direct descendants which can be reached through a child at any depth)
    for branch in tree.values():
        for child in branch.children:
            for grandchild in child.children:
                if grandchild in branch:
                    branch.remove_child(grandchild)

    return list(tree.values())


def has_name(branch: TreeBranch, name: str) -> bool:
    if name in branch.name.split(", "):
        return True

    return False


def has_child_name(branch: TreeBranch, child_name: str) -> bool:
    if any(has_name(child, child_name) for child in branch.children):
        return True

    for grandchild in branch.children:
        if has_child_name(grandchild, child_name):
            return True

    return False


def print_tree(
    tree: list[TreeBranch],
    branches: list[str] | None = None,
    contains: list[str] | None = None,
    tag: str | None = None,
):
    merged_branches = git.get_merged(tag) if tag else []

    for merged_branch in merged_branches:
        for branch in tree:
            if branch.sha == merged_branch.sha:
                branch.name += f" (in {tag})"

    for branch in tree:
        if branches and not any(name in branch.name for name in branches):
            continue
        if contains and not any(
            has_child_name(branch, branch_name) for branch_name in contains
        ):
            continue
        branch.print_tree()
