class Svw < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "67ec2686519643407e7fcfb8df91d0fbafcde798dbd60d2ed17d6e9717661cef"
  license "MIT"
  revision 4

  depends_on arch: :arm64
  depends_on macos: :big_sur

  def install
    bin.install "bin/svw"
    pkgshare.install Dir["share/svw/*"]
  end

  test do
    system bin/"svw", "--version"
    system bin/"svw", "--help"
  end
end
