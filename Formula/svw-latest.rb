class SvwLatest < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/latest/svw-latest-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "89ebeeee336dfc10ec036463108a55547500948bb60a3fac3532cf3b3e4fb0a1"
  license "MIT"
  revision 18

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
