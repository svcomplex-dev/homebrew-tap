class SvwLatest < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "5dfc2b54a2685e63433cdf999493684df58bdfdc8ccd2368ffb5d23abc85ec93"
  license "MIT"
  revision 8

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
