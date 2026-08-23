class Svw < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "e720e5e08151bbded981eb51c248f5cec1b55a72b30b00672f610fb0950b5c8e"
  license "MIT"
  revision 5

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
