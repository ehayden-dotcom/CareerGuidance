# Contributing to AI Career Pathways Advisor

Thank you for considering contributing to the project!  We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements and pull requests.

## Branch Strategy

- The **`main`** branch contains the latest stable code.  All work should happen in topic branches or forks and be merged into `main` through pull requests (PRs).
- For larger changes, please open an issue first to discuss the idea.  This helps avoid duplicated work and ensures the change fits with the project goals.
- Pull requests should target `main` and will trigger the CI pipeline (lint, tests and builds).  Once the CI checks pass and at least one maintainer approves the PR, it can be merged.

## Commit Style

Please write clear, concise commit messages following the conventional commits style (e.g. `feat: add recommendation endpoint`, `fix: correct scoring formula`).  Each commit should represent a logical unit of work.

## Pull Request Checklist

Before opening a PR:

1. Ensure your branch is up to date with `main`.
2. Run `make fmt` to format and lint the backend and frontend code.
3. Run `make test` to ensure all tests pass.
4. Update documentation (README and docs) if your change affects public interfaces or behaviour.
5. Include any relevant screenshots or recordings if the change is visual.

## Issue Labels

- **bug** – Something isn’t working as expected.
- **enhancement** – New feature or request.
- **documentation** – Changes or additions to docs.
- **good first issue** – Great for newcomers to open source.
- **help wanted** – Extra attention is needed.

## Releases

When we accumulate enough changes for a new version, maintainers will tag a release on `main`.  Semantic versioning (e.g. `v1.2.0`) is used.

## Code of Conduct

By participating, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).  Please report unacceptable behaviour to the maintainers listed in the README.