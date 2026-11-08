#!/usr/bin/env python3
"""What the vendor kernel needs to mount the /usr/lib squashfs image.

build-image.sh stores /usr/lib as an LZ4 squashfs file inside the ext4 root and
rcS mounts it through a loop device. A kernel without one of these built in
would start with no libraries at all, so the build asks before it composes.

Usage: lib_image.py check TARGET
"""
from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import kernel_abi  # noqa: E402

IMAGE = "/usr/share/baseos/usr-lib.sqfs"
REQUIRED = ("CONFIG_BLK_DEV_LOOP=y", "CONFIG_SQUASHFS=y", "CONFIG_SQUASHFS_LZ4=y")


def kernel_config(kernel: bytes) -> set[str]:
    """The options of the configuration the kernel carries (CONFIG_IKCONFIG)."""
    start = kernel.find(b"IKCFG_ST")
    end = kernel.find(b"IKCFG_ED", start)
    if start < 0 or end < 0:
        raise ValueError("kernel carries no configuration")
    return set(gzip.decompress(kernel[start + 8:end]).decode().splitlines())


def comp(kernel: bytes) -> str:
    config = kernel_config(kernel)
    if "CONFIG_SQUASHFS_ZSTD=y" in config:
        return "zstd"
    if "CONFIG_SQUASHFS_LZ4=y" in config:
        return "lz4"
    raise ValueError("kernel lacks both LZ4 and ZSTD squashfs compression")


def missing(kernel: bytes) -> list[str]:
    config = kernel_config(kernel)
    absent = []
    if "CONFIG_BLK_DEV_LOOP=y" not in config:
        absent.append("CONFIG_BLK_DEV_LOOP=y")
    if "CONFIG_SQUASHFS=y" not in config:
        absent.append("CONFIG_SQUASHFS=y")
    if "CONFIG_SQUASHFS_LZ4=y" not in config and "CONFIG_SQUASHFS_ZSTD=y" not in config:
        absent.append("CONFIG_SQUASHFS_LZ4=y")
    return absent


def target_kernel(target: str) -> bytes:
    work = ROOT / "work" / target
    layout = json.loads((work / "source.json").read_text(encoding="utf-8"))["layout"]
    boot = next(p for p in layout["partitions"] if p["number"] == 4)
    return kernel_abi.extract_kernel(work / "boot-prefix.img", boot["start_sector"])


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "comp"):
        raise SystemExit("Usage: lib_image.py check|comp TARGET")
    command, target = sys.argv[1], sys.argv[2]
    kernel = target_kernel(target)
    if command == "comp":
        print(comp(kernel))
        return
    absent = missing(kernel)
    if absent:
        raise SystemExit(f"{target}: the kernel cannot mount the /usr/lib image, it lacks {' '.join(absent)}")
    compressor = comp(kernel)
    print(f"{target}: kernel mounts {compressor.upper()} squashfs through a loop device")


if __name__ == "__main__":
    main()
