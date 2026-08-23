class Svw < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "6c1b8acd6fce7a9ee5e251b288009bf633de037c7538d55738cf29e138161722"
  license "MIT"
  revision 1

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
