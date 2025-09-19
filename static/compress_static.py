#!/usr/bin/env python3
"""
Compress all static files for optimal serving
"""
import gzip
import os
import subprocess
from pathlib import Path


def compress_file(filepath):
    """Compress a file with both gzip and brotli"""
    # Skip if already compressed
    if filepath.endswith((".gz", ".br")):
        return

    # Create gzip version
    gz_path = f"{filepath}.gz"
    with open(filepath, "rb") as f_in:
        with gzip.open(gz_path, "wb", compresslevel=9) as f_out:
            f_out.write(f_in.read())

    # Create brotli version if available
    try:
        subprocess.run(
            ["brotli", "-k", "-9", filepath], check=True, capture_output=True
        )
        print(f"Compressed: {filepath}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Gzipped only: {filepath} (brotli not available)")


def main():
    # Get the static directory
    static_dir = Path(__file__).parent

    # File extensions to compress
    compress_extensions = {".css", ".js", ".json", ".svg", ".xml", ".txt", ".html"}

    # Walk through all static files
    for root, _dirs, files in os.walk(static_dir):
        for file in files:
            filepath = os.path.join(root, file)
            file_ext = Path(filepath).suffix.lower()

            # Compress if it's a compressible file type
            if file_ext in compress_extensions:
                compress_file(filepath)


if __name__ == "__main__":
    main()
