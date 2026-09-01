class SvwAT013 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.3/svw-release-0.1.3-macos-arm64.tar.gz"
  version "0.1.3"
  sha256 "5f7dd1a061f2c115d5cb98486f9c800d6b9673cb06599d814bd8f8cab5584293"
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
