# svcomplex Homebrew tap

Install `svw` on Apple Silicon macOS 11 or newer:

```sh
brew install svcomplex-dev/tap/svw
```

The unversioned formula follows the newest immutable `release-X.Y.Z` release.
Install the replaceable rolling build only when explicitly requested:

```sh
brew install svcomplex-dev/tap/svw@latest
```

Install a fixed release tag through its immutable versioned formula:

```sh
brew install svcomplex-dev/tap/svw@0.1.0
```

The formula installs the audited macOS arm64 binary from the public
[`svcomplex-dev/svw`](https://github.com/svcomplex-dev/svw) GitHub Release.
Product source is maintained outside this distribution-only tap.

Commits in this checkout use the tracked `.githooks/pre-commit` identity gate and
must use `code@svcomplex.ai` for both author and committer email addresses.

`script/update-svw-formula.py` verifies the public Release manifest, checksum
sidecar, archive checksum, package manifest and Mach-O payload before changing a
formula. A `latest` event updates only `svw@latest`; a newer immutable release
updates both `svw` and its `svw@X.Y.Z` formula. The workflow serializes both event types;
the authoritative Gitea release CI dispatches each update only after all GitHub
Release assets have been published successfully.

Every candidate formula is installed through svw's public `install.sh` on an
Apple Silicon GitHub runner before the formula commit is pushed. This exercises
the user-facing macOS installation path rather than only a direct Brew command.
