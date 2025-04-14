# Branchtree

`branchtree` is a command-line tool that displays a hierarchical representation of the branches in a Git repository.
It visualizes the relationships between branches, showing which branches are based on others and how they are related
through commits.

Alternatively it can also be imported and used as a Python module.

## Features

- **Branch hierarchy**: View a tree-like structure showing how branches are related to one another.
- **Filtering by regex**: Filter branches by a regular expression to display only relevant branches.
- **Local and remote branches**: Show either local or remote branches, or both.
- **Tag inclusion**: Display whether a branch is merged into a given tag.
- **Branch-specific view**: View a specific branch's hierarchy along with its children (if any).

## Installation

To use the `branchtree` tool, ensure you have Python (>= 3.11) installed on your system.

You can install `branchtree` via pip:

```bash
$ pip install branchtree
```

Alternatively, you can install it by cloning this repository and installing via pip locally:

```bash
$ git clone https://github.com/nazsolti/branchtree.git
$ cd branchtree
$ pip install .
````

After installation the `branchtree` command will be available in your terminal.

## Usage

```
usage: branchtree [-h] [--regex REGEX] [-l] [-r] [-b [BRANCH ...]] [-t TAG]
```

### Options:

- `-h, --help`: Show the help message and exit.
- `-V, --version`: Show the version number and exit.
- `--regex REGEX`: Only show branches matching the given regex.
- `-l, --local`: Only show local branches.
- `-r, --remote`: Only show remote branches from `origin`. For other remotes, use the `--regex` option.
- `-b [BRANCH ...], --branch [BRANCH ...]`: Only show the specified branches and their children.
- `-c [CONTAINS ...], --contains [CONTAINS ...]`: Only show branches which contain these revisions. This can be a branch, tag or any commit specifier. If there's more specified, show branches which contain all of them.
- `-N, --no-contains`: This only has effect if --contains is specified, also show branches which do not contain the given revisions, and instead specify the branches which do contain them.
- `-t TAG, --tag TAG`: Show whether each branch is included in the given tag (i.e., merged into the tag).

## Examples

### Displaying Remote Branches

```bash
$ branchtree -r
```

This command will display a tree of remote branches from `origin`.

```
🞄origin/feature-1234
  └── origin/bugfix-4567
🞄origin/bugfix-4567
🞄origin/feature-5678
🞄origin/release-2025-01
🞄origin/feature-6789
  └── origin/feature-1234
       └── origin/bugfix-4567
🞄origin/feature-7890
🞄origin/hotfix-3456
```

In this example, `origin/feature-6789` is the parent branch of `origin/feature-1234` and that is the parent of
`origin/bugfix-4567`.

### Filtering Branches with a Regex

```bash
$ branchtree -r --regex "feature"
```

This command will show only remote branches with names that match the regex pattern `feature`:

```
🞄origin/feature-1234
🞄origin/feature-5678
🞄origin/feature-6789
  └── origin/feature-1234
🞄origin/feature-7890
```

### Show Only Local Branches

```bash
$ branchtree -l
```

This command will display the hierarchy of **local** branches in the repository.

```
🞄feature/login-setup
🞄feature/dashboard-UI
  └── feature/login-setup
🞄hotfix/ui-bug
🞄feature/profile-settings
  └── feature/dashboard-UI
       └── feature/login-setup
```

### Show Only Specific Branches

```bash
$ branchtree -b feature/login-setup feature/dashboard-UI
```

This command will display the hierarchy for only the specified branches and their children.

```
🞄feature/login-setup
🞄feature/dashboard-UI
  └── feature/login-setup
```

### Show Branches Merged Into a Tag

```bash
$ branchtree -r -t v1.2
```

This command will display all remote branches and indicate whether they are merged into the `v1.2` tag.

```
🞄origin/feature-1234
  └── origin/bugfix-4567 (in v1.2)
🞄origin/bugfix-4567
🞄origin/feature-5678
🞄origin/release-2025-01
🞄origin/feature-6789
  └── origin/feature-1234
       └── origin/bugfix-4567 (in v1.2)
🞄origin/feature-7890
🞄origin/hotfix-3456 (in v1.2)
```

In this particular example branches `origin/bugfix-4567` and `origin/hotfix-3456` are merged into the `v1.2` tag.

This can be useful to check whether a branch has been released already.

### Show Branches Containing a Branch

```bash
$ branchtree -c feature/login-setup
```

This command will only display the hierarchy for the branches that contain the specified branch. 

```
🞄feature/dashboard-UI
  └── feature/login-setup
```

Similarly to the `-b` argument, multiple branches can be specified.
