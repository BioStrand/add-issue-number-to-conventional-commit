# Conventional Commits Hook

Track your issue number in your [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).
This [pre-commit](https://pre-commit.com) compatible hook parses common issue numbers (e.g. `pre-10`) from your branch name
and appends it to your [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) according to the internal
convention used at BioStrand.

This is a fork from https://gitlab.com/codementors/pre-commit/add-issue-number-to-conventional-commit.

## Example:
A commit with the commit message `feat: Initial commit`on branch `feat/pre-10-awesome-feature`
will be expanded to: `feat: PRE-10 - Initial commit`. 

## Use this hook

Add this hook to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/BioStrand/add-issue-number-to-conventional-commit
    rev: v0.0.2 # Insert latest version from https://github.com/BioStrand/add-issue-number-to-conventional-commit/-/tags
    hooks:
      - id: add-issue-number
```

Make sure hooks of type `prepare-msg-commit` are installed properly, e.g. by adding it to your `.pre-commit-config.yaml`:

```yaml
default_install_hook_types:
  - pre-commit
  - prepare-commit-msg
```

## Development

Create virtual environment and install the dev dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
 
pip install '.[dev]'
```

Run tests:

```bash
tox
```
