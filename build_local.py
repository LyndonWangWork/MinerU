#!/usr/bin/env python
"""
Local build script for MinerU executable
Usage: python build_local.py [--test]
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def print_step(message):
    """Print colored step message"""
    print(f"\n{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}\n")

def run_command(cmd, description):
    """Run command and handle errors"""
    print(f"⏳ {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        print(f"Error: {result.stderr}")
        return False

    print(f"✅ Success: {description}")
    if result.stdout:
        print(result.stdout)
    return True

def check_dependencies():
    """Check if required tools are installed"""
    print_step("Checking dependencies")

    # Check Python version
    version = sys.version_info
    if version.major != 3 or version.minor < 10:
        print(f"❌ Python 3.10+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

    # Check pip
    if not run_command("pip --version", "Check pip"):
        return False

    # Check PyInstaller
    result = subprocess.run("pyinstaller --version", shell=True,
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️  PyInstaller not found, installing...")
        if not run_command("pip install pyinstaller", "Install PyInstaller"):
            return False
    else:
        print(f"✅ PyInstaller {result.stdout.strip()}")

    # Check UPX (optional)
    result = subprocess.run("upx --version", shell=True,
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️  UPX not found (optional, for compression)")
        print("   Windows: Download from https://upx.github.io/")
        print("   macOS: brew install upx")
    else:
        print("✅ UPX installed")

    return True

def install_dependencies():
    """Install MinerU dependencies"""
    print_step("Installing MinerU dependencies")

    if not os.path.exists("requirements-minimal.txt"):
        print("❌ requirements-minimal.txt not found")
        return False

    if not run_command("pip install -r requirements-minimal.txt",
                      "Install dependencies"):
        return False

    if not run_command("pip install -e .", "Install MinerU"):
        return False

    return True

def verify_installation():
    """Verify MinerU installation"""
    print_step("Verifying installation")

    # Try importing mineru
    try:
        import mineru
        print(f"✅ MinerU version: {mineru.__version__}")
    except Exception as e:
        print(f"❌ Failed to import mineru: {e}")
        return False

    # Try running mineru command
    if not run_command("mineru --version", "Check mineru command"):
        return False

    return True

def build_executable():
    """Build executable with PyInstaller"""
    print_step("Building executable")

    if not os.path.exists("mineru-minimal.spec"):
        print("❌ mineru-minimal.spec not found")
        return False

    # Clean previous build
    if os.path.exists("build"):
        print("🧹 Cleaning build directory...")
        shutil.rmtree("build")

    if os.path.exists("dist"):
        print("🧹 Cleaning dist directory...")
        shutil.rmtree("dist")

    # Run PyInstaller
    if not run_command("pyinstaller mineru-minimal.spec --clean --noconfirm",
                      "Run PyInstaller"):
        return False

    return True

def verify_build():
    """Verify the built executable"""
    print_step("Verifying build")

    system = platform.system()
    if system == "Windows":
        exe_path = "dist/mineru/mineru.exe"
    else:
        exe_path = "dist/mineru/mineru"

    if not os.path.exists(exe_path):
        print(f"❌ Executable not found: {exe_path}")
        return False

    print(f"✅ Executable found: {exe_path}")

    # Get size
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"   Size: {size_mb:.2f} MB")

    # Try running
    if system == "Windows":
        cmd = f'"{exe_path}" --version'
    else:
        cmd = f'chmod +x "{exe_path}" && "{exe_path}" --version'

    if not run_command(cmd, "Test executable"):
        return False

    return True

def test_executable():
    """Test executable with sample PDF"""
    print_step("Testing executable (optional)")

    system = platform.system()
    if system == "Windows":
        exe_path = "dist/mineru/mineru.exe"
    else:
        exe_path = "dist/mineru/mineru"

    # Look for test PDF
    test_pdfs = list(Path(".").glob("**/*.pdf"))[:1]
    if not test_pdfs:
        print("⚠️  No test PDF found, skipping functional test")
        return True

    test_pdf = test_pdfs[0]
    test_output = "test_output"

    print(f"📄 Testing with: {test_pdf}")

    if system == "Windows":
        cmd = f'"{exe_path}" -p "{test_pdf}" -o "{test_output}"'
    else:
        cmd = f'"{exe_path}" -p "{test_pdf}" -o "{test_output}"'

    if run_command(cmd, "Parse test PDF"):
        print(f"✅ Test completed, output in: {test_output}")
    else:
        print("⚠️  Test failed, but build might still be usable")

    return True

def create_archive():
    """Create distribution archive"""
    print_step("Creating distribution archive")

    system = platform.system()
    arch = platform.machine().lower()

    if "x86_64" in arch or "amd64" in arch:
        arch = "x64"
    elif "arm64" in arch or "aarch64" in arch:
        arch = "arm64"

    if system == "Windows":
        archive_name = f"mineru-windows-{arch}.zip"
        cmd = f'powershell Compress-Archive -Path dist/mineru -DestinationPath {archive_name} -Force'
    elif system == "Darwin":
        archive_name = f"mineru-macos-{arch}.tar.gz"
        cmd = f'tar -czf {archive_name} -C dist mineru'
    else:  # Linux
        archive_name = f"mineru-linux-{arch}.tar.gz"
        cmd = f'tar -czf {archive_name} -C dist mineru'

    if run_command(cmd, f"Create {archive_name}"):
        size_mb = os.path.getsize(archive_name) / (1024 * 1024)
        print(f"✅ Archive created: {archive_name} ({size_mb:.2f} MB)")

        # Calculate checksum
        if system == "Windows":
            cmd = f'certutil -hashfile {archive_name} SHA256'
        else:
            cmd = f'shasum -a 256 {archive_name}'

        run_command(cmd, "Calculate checksum")
        return True

    return False

def main():
    """Main build process"""
    print("\n" + "="*60)
    print("  MinerU Executable Builder")
    print("="*60)

    test_mode = "--test" in sys.argv

    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed")
        return 1

    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed")
        return 1

    # Step 3: Verify installation
    if not verify_installation():
        print("\n❌ Verification failed")
        return 1

    # Step 4: Build executable
    if not build_executable():
        print("\n❌ Build failed")
        return 1

    # Step 5: Verify build
    if not verify_build():
        print("\n❌ Build verification failed")
        return 1

    # Step 6: Test (optional)
    if test_mode:
        test_executable()

    # Step 7: Create archive
    create_archive()

    # Success!
    print_step("Build completed successfully! 🎉")
    print("📦 Distribution package is ready")
    print("\nNext steps:")
    print("1. Test the executable in dist/mineru/")
    print("2. Extract and test the archive")
    print("3. Distribute to users")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
