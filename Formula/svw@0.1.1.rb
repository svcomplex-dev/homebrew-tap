class SvwAT011 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.1/svw-release-0.1.1-macos-arm64.tar.gz"
  version "0.1.1"
  sha256 "782d83224924008fd862241bd6fae85f978082fd6922bd4cf23aaee757fa518d"
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
