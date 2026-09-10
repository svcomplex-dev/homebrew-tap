class SvwAT015 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.5/svw-release-0.1.5-macos-arm64.tar.gz"
  version "0.1.5"
  sha256 "fc74d4eac4e2964a6865169bfc1fb20459c1abfa424ba873e487154fb5016a69"
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
