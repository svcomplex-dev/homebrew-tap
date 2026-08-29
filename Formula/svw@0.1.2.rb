class SvwAT012 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.2/svw-release-0.1.2-macos-arm64.tar.gz"
  version "0.1.2"
  sha256 "9d7893bf4aee6227f65b4383760f08ab429a2fe55c0328d36a88e140bb3a686b"
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
