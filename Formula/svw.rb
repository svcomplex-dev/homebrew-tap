class Svw < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "2716713ed8671b4516940ac24ddf4551d4f36c48affffebde395360e07b11cc5"
  license "MIT"
  revision 3

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
