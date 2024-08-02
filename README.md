## update-release-version
This action automatically increments the semantic version for a new release in a GitHub Actions pipeline. 

## Requirements
The [checkout](https://github.com/actions/checkout) action must be invoked in a prior step in the workflow, to ensure that the repository's `git` history is available for this action to query.

This action also requires that the release version is being stored in a repository variable.

The release version must adhere to the [SemVer specification](https://semver.org/), i.e. `{$MAJOR_VERSION}.{$MINOR_VERSION}.{$PATCH_VERSION}`.
See https://semver.org/

## How it works
This action tries to determine which digit in the semantic version to increment based on the prefix of the latest commit. These prefixes should adhere to the [Conventional Commit specification](https://www.conventionalcommits.org/en/v1.0.0/).
- Commits that break backwards compatibility (typically prefaced with `BREAKING CHANGE:`) result in a major version increment.
- Commits that add non-breaking features (typically prefaced with `feat:`) result in a minor version increment.
- Commits for bug fixes, refactoring, or performance improvements (typically prefaced with `fix:`, `refactor:`, `perf:`, or `test:`) result in patch version increments.
- All other commits do not result in any release version increment.

In addition to updating the release version via API, the incremented version is also passed to other stages of the current GitHub Actions run via $GITHUB_OUTPUT.
See https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs

The action writes the incremented release version to [$GITHUB_OUTPUT](https://docs.github.com/en/actions/using-jobs/defining-outputs-for-jobs) to be consumed by later steps in the workflow, such as the [create-release](https://github.com/actions/create-release) action. It also calls the [GitHub API](https://docs.github.com/en/rest/actions/variables?apiVersion=2022-11-28#update-a-repository-variable) to increment the value of the release version repository variable to ensure that this change persists.

## Tests
The `.vscode/launch.json` file defines unit and integration tests than can be run with the [VS Code debugger](https://code.visualstudio.com/docs/editor/debugging). 
