# Repository rules

- This repository is the distribution-only Homebrew tap for `svw`; do not add
  product source code.
- Formulae must use audited public GitHub Release assets and exact SHA-256
  digests. `Formula/svw.rb` follows the highest immutable release,
  `latest` may replace only `Formula/svw@latest.rb`, and versioned
  `Formula/svw@X.Y.Z.rb` files are immutable.
- Every formula update must install and smoke test `svw --version` and
  `svw --help` on Apple Silicon macOS.
- Git author and committer email must both be `code@svcomplex.ai`.
