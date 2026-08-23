#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 code@svcomplex.ai
"""Focused channel and immutability tests for the svw formula updater."""

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).with_name("update-svw-formula.py")
SPEC = importlib.util.spec_from_file_location("update_svw_formula", SCRIPT)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)


class FormulaUpdaterTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="svw-tap-test-")
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def run_update(self, tag, version):
        archive_name = f"svw-{tag}-macos-arm64.tar.gz"
        archive = f"archive:{tag}".encode()
        digest = hashlib.sha256(archive).hexdigest()
        release = {
            "tag_name": tag,
            "assets": [
                {"name": archive_name, "browser_download_url": "asset:archive"},
                {"name": f"{archive_name}.sha256", "browser_download_url": "asset:sidecar"},
                {
                    "name": f"svw-{tag}-manifest.json",
                    "browser_download_url": "asset:manifest",
                },
            ],
        }
        manifest = {
            "schema": "svw-github-release-v3",
            "repository": UPDATER.REPOSITORY,
            "github_release_tag": tag,
            "authoritative_source_revision": "a" * 40,
            "assets": [{"name": archive_name, "sha256": digest}],
        }

        def fetch(url):
            return {
                "asset:archive": archive,
                "asset:sidecar": f"{digest}  {archive_name}\n".encode(),
                "asset:manifest": json.dumps(manifest).encode(),
            }[url]

        with (
            mock.patch.object(UPDATER, "fetch_json", return_value=release),
            mock.patch.object(UPDATER, "fetch", side_effect=fetch),
            mock.patch.object(
                UPDATER, "audited_binary", return_value=(b"Mach-O", digest)
            ),
        ):
            return UPDATER.update(self.root, tag, product_version=version)

    def test_latest_is_isolated_from_stable_formula(self):
        self.assertTrue(self.run_update("latest", "0.1.0"))
        latest = (self.root / "Formula/svw-latest.rb").read_text()
        self.assertIn("class SvwLatest < Formula", latest)
        self.assertIn("releases/download/latest/", latest)
        self.assertFalse((self.root / "Formula/svw.rb").exists())
        self.assertFalse(self.run_update("latest", "0.1.0"))

    def test_release_promotes_stable_without_allowing_downgrade(self):
        self.assertTrue(self.run_update("release-0.1.0", "0.1.0"))
        stable = self.root / "Formula/svw.rb"
        versioned = self.root / "Formula/svw@0.1.0.rb"
        self.assertIn("class Svw < Formula", stable.read_text())
        self.assertNotIn("keg_only", stable.read_text())
        self.assertIn("keg_only :versioned_formula", versioned.read_text())

        self.assertTrue(self.run_update("release-0.2.0", "0.2.0"))
        self.assertIn("release-0.2.0", stable.read_text())
        self.assertFalse(self.run_update("release-0.1.0", "0.1.0"))
        self.assertIn("release-0.2.0", stable.read_text())

    def test_versioned_formula_is_immutable(self):
        self.run_update("release-0.1.0", "0.1.0")
        path = self.root / "Formula/svw@0.1.0.rb"
        path.write_text(path.read_text().replace("0.1.0", "9.9.9", 1))
        with self.assertRaisesRegex(RuntimeError, "refusing to replace immutable"):
            self.run_update("release-0.1.0", "0.1.0")

    def test_fetch_uses_actions_token_when_available(self):
        seen = {}

        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self):
                return b"payload"

        def opener(request, timeout):
            seen["request"] = request
            seen["timeout"] = timeout
            return Response()

        with (
            mock.patch.dict(os.environ, {"GITHUB_TOKEN": "actions-token"}),
            mock.patch.object(UPDATER, "urlopen", side_effect=opener),
        ):
            self.assertEqual(UPDATER.fetch("https://example.invalid"), b"payload")
        self.assertEqual(seen["timeout"], 120)
        self.assertEqual(seen["request"].headers["Authorization"], "Bearer actions-token")


if __name__ == "__main__":
    unittest.main()
