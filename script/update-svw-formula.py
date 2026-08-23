#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 code@svcomplex.ai
"""Generate an audited Homebrew formula from a public svw GitHub Release."""

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen


REPOSITORY = "svcomplex-dev/svw"
API_ROOT = f"https://api.github.com/repos/{REPOSITORY}"
TAG_PATTERN = re.compile(r"release-((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*))")
VERSION_OUTPUT = re.compile(r"^svw ([0-9]+\.[0-9]+\.[0-9]+)(?:\s|$)")


def fetch(url):
    headers = {"User-Agent": "svw-homebrew-tap-updater/1"}
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=120) as response:
        return response.read()


def fetch_json(url):
    return json.loads(fetch(url))


def parse_sidecar(payload, expected_name, digest):
    fields = payload.decode("ascii").strip().split()
    if fields != [digest, expected_name]:
        raise RuntimeError(f"invalid checksum sidecar for {expected_name}")


def parse_manifest(payload):
    fields = {}
    for line in payload.decode("utf-8").splitlines():
        if not line:
            continue
        if "=" not in line:
            raise RuntimeError("invalid package manifest line")
        key, value = line.split("=", 1)
        if not key or key in fields:
            raise RuntimeError(f"invalid package manifest key: {key}")
        fields[key] = value
    return fields


def audited_binary(archive, release_tag, release_manifest):
    asset_name = f"svw-{release_tag}-macos-arm64.tar.gz"
    digest = hashlib.sha256(archive).hexdigest()
    declared = {
        item["name"]: item["sha256"] for item in release_manifest.get("assets", [])
    }
    if declared.get(asset_name) != digest:
        raise RuntimeError("release manifest does not match the macOS archive")

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as package:
        files = {member.name.removeprefix("./"): member for member in package.getmembers()}
        if "bin/svw" not in files or "manifest.txt" not in files:
            raise RuntimeError("macOS archive is missing bin/svw or manifest.txt")
        binary_member = files["bin/svw"]
        manifest_member = files["manifest.txt"]
        if not binary_member.isfile() or not manifest_member.isfile():
            raise RuntimeError("macOS archive has invalid required members")
        binary = package.extractfile(binary_member).read()
        manifest = parse_manifest(package.extractfile(manifest_member).read())

    required = {
        "schema": "svw-release-v2",
        "name": "svw",
        "source_revision": release_manifest["authoritative_source_revision"],
        "platform": "macos-arm64",
        "build_type": "Release",
        "optimization": "-O3 -DNDEBUG",
        "unit_tests": "passed",
        "symbols": "stripped",
    }
    for key, expected in required.items():
        if manifest.get(key) != expected:
            raise RuntimeError(f"unexpected package manifest {key}: {manifest.get(key)!r}")
    if not binary.startswith((b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf", b"\xca\xfe\xba\xbe", b"\xbe\xba\xfe\xca")):
        raise RuntimeError("bin/svw is not a Mach-O binary")
    return binary, digest


def binary_version(binary):
    with tempfile.TemporaryDirectory(prefix="svw-version-") as temporary:
        executable = Path(temporary) / "svw"
        executable.write_bytes(binary)
        executable.chmod(0o755)
        result = subprocess.run(
            [str(executable), "--version"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    match = VERSION_OUTPUT.match(result.stdout.strip())
    if not match:
        raise RuntimeError(f"unexpected svw --version output: {result.stdout!r}")
    return match.group(1)


def class_name(channel):
    if channel == "stable":
        return "Svw"
    if channel == "latest":
        return "SvwATLatest"
    return "SvwAT" + "".join(channel.split("."))


def render_formula(release_tag, version, digest, channel, revision=0):
    lines = [
        f"class {class_name(channel)} < Formula",
        '  desc "Terminal waveform viewer for hardware design workflows"',
        '  homepage "https://svw.run"',
        f'  url "https://github.com/{REPOSITORY}/releases/download/{release_tag}/svw-{release_tag}-macos-arm64.tar.gz"',
        f'  version "{version}"',
        f'  sha256 "{digest}"',
        '  license "MIT"',
    ]
    if revision:
        lines.append(f"  revision {revision}")
    lines.extend(
        [
            "",
            "  depends_on arch: :arm64",
            "  depends_on macos: :big_sur",
        ]
    )
    if channel != "stable":
        lines.extend(["", "  keg_only :versioned_formula"])
    lines.extend(
        [
            "",
            "  def install",
            '    bin.install "bin/svw"',
            '    pkgshare.install Dir["share/svw/*"]',
            "  end",
            "",
            "  test do",
            '    system bin/"svw", "--version"',
            '    system bin/"svw", "--help"',
            "  end",
            "end",
            "",
        ]
    )
    return "\n".join(lines)


def current_formula_state(path):
    if not path.exists():
        return None, None, 0
    text = path.read_text(encoding="utf-8")
    version = re.search(r'^  version "([^"]+)"$', text, re.MULTILINE)
    digest = re.search(r'^  sha256 "([0-9a-f]{64})"$', text, re.MULTILINE)
    revision = re.search(r"^  revision ([0-9]+)$", text, re.MULTILINE)
    if not version or not digest:
        raise RuntimeError(f"cannot parse existing formula: {path}")
    return version.group(1), digest.group(1), int(revision.group(1)) if revision else 0


def semantic_version(value):
    fields = value.split(".")
    if len(fields) != 3 or any(not field.isdigit() for field in fields):
        raise RuntimeError(f"formula has invalid semantic version: {value}")
    return tuple(int(field) for field in fields)


def write_formula(path, desired, immutable=False):
    if path.exists() and path.read_text(encoding="utf-8") == desired:
        return False
    if immutable and path.exists():
        raise RuntimeError(f"refusing to replace immutable versioned formula: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(desired, encoding="utf-8")
    return True


def update(root, release_tag, product_version=None):
    match = TAG_PATTERN.fullmatch(release_tag)
    if release_tag != "latest" and not match:
        raise RuntimeError("tag must be latest or release-MAJOR.MINOR.PATCH")

    release = fetch_json(f"{API_ROOT}/releases/tags/{release_tag}")
    if release.get("tag_name") != release_tag:
        raise RuntimeError("GitHub returned a different release tag")
    assets = {asset["name"]: asset for asset in release.get("assets", [])}
    archive_name = f"svw-{release_tag}-macos-arm64.tar.gz"
    sidecar_name = f"{archive_name}.sha256"
    manifest_name = f"svw-{release_tag}-manifest.json"
    if not {archive_name, sidecar_name, manifest_name}.issubset(assets):
        raise RuntimeError("GitHub Release is missing required macOS assets")

    archive = fetch(assets[archive_name]["browser_download_url"])
    digest = hashlib.sha256(archive).hexdigest()
    parse_sidecar(fetch(assets[sidecar_name]["browser_download_url"]), archive_name, digest)
    release_manifest = json.loads(fetch(assets[manifest_name]["browser_download_url"]))
    expected_manifest = {
        "schema": "svw-github-release-v3",
        "repository": REPOSITORY,
        "github_release_tag": release_tag,
    }
    for key, expected in expected_manifest.items():
        if release_manifest.get(key) != expected:
            raise RuntimeError(f"unexpected release manifest {key}")
    binary, digest = audited_binary(archive, release_tag, release_manifest)

    version = match.group(1) if match else (product_version or binary_version(binary))
    if release_tag == "latest":
        path = root / "Formula" / "svw@latest.rb"
        old_version, old_digest, old_revision = current_formula_state(path)
        revision = (
            old_revision
            if old_digest == digest
            else old_revision + 1 if old_version == version and old_digest else 0
        )
        changed = write_formula(
            path,
            render_formula(release_tag, version, digest, "latest", revision),
        )
        print(path)
        return changed

    versioned_path = root / "Formula" / f"svw@{version}.rb"
    versioned_changed = write_formula(
        versioned_path,
        render_formula(release_tag, version, digest, version),
        immutable=True,
    )

    stable_path = root / "Formula" / "svw.rb"
    old_version, old_digest, old_revision = current_formula_state(stable_path)
    stable_changed = False
    if old_version is None or semantic_version(version) >= semantic_version(old_version):
        revision = (
            old_revision
            if old_digest == digest
            else old_revision + 1 if old_version == version and old_digest else 0
        )
        stable_changed = write_formula(
            stable_path,
            render_formula(release_tag, version, digest, "stable", revision),
        )
    print(stable_path)
    return versioned_changed or stable_changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--product-version")
    arguments = parser.parse_args()
    changed = update(arguments.root.resolve(), arguments.tag, arguments.product_version)
    print("updated" if changed else "unchanged")


if __name__ == "__main__":
    main()
