class SvwAT010 < Formula
  desc "Terminal waveform viewer for hardware design workflows"
  homepage "https://svw.run"
  url "https://github.com/svcomplex-dev/svw/releases/download/release-0.1.0/svw-release-0.1.0-macos-arm64.tar.gz"
  version "0.1.0"
  sha256 "615f6ea71f156dbda983d97c17115120bbbb73323d22a9572412903b0da9676a"
  license "MIT"
  revision 1

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
