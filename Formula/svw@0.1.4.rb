class SvwAT014 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.4/svw-release-0.1.4-macos-arm64.tar.gz"
  version "0.1.4"
  sha256 "727010698dcfb87214d3a7f4151ac7e139e9caf573d0b8b09b33944155cc4c7a"
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
