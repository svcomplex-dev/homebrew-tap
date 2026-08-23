class Svw < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.0/svw-release-0.1.0-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "3d8dadfb87e84ede95b9356d567f0e2368afa503c0aa09930dd6b70d311210e3"
  license "MIT"
  revision 9

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
