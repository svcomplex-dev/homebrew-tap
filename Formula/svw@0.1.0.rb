class SvwAT010 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.0/svw-release-0.1.0-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "09a830e101252764e82d979efa9b47aeab54f23a5f34412c1c9b603313a07c3c"
  license "MIT"

  depends_on arch: :arm64
  depends_on macos: :big_sur

  keg_only :versioned_formula

  def install
    bin.install "bin/svw"
    pkgshare.install Dir["share/svw/*"]
  end

  test do
    system bin/"svw", "--version"
    system bin/"svw", "--help"
  end
end
