class SvwLatest < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.2"
  sha256 "a761c4fe346ca48a3474142ffd1b8527adbc41819cbd1b2d86df291e4c42c213"
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
