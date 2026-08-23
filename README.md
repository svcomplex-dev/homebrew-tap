# svcomplex Homebrew tap

Install `svw` on Apple Silicon macOS 11 or newer:

```sh
brew install svcomplex-dev/tap/svw
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
formula. The update workflow serializes `latest` and versioned release events;
the authoritative Gitea release CI dispatches each update only after all GitHub
Release assets have been published successfully.
