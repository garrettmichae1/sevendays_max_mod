#!/usr/bin/env python3
"""Build a reproducible install ZIP containing only the mod folder."""

from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

from check_compatibility import inspect_package


def main():
    inspect_package()
    root = Path(__file__).resolve().parents[1]
    mod = root / "SevenDaysMaxLevel2000"
    version = ET.parse(mod / "ModInfo.xml").getroot().find("Version").get("value")
    output = root / "dist" / f"SevenDaysMaxLevel2000-v{version}.zip"
    output.parent.mkdir(exist_ok=True)
    files = [mod / "ModInfo.xml", mod / "README.txt", *sorted((mod / "Config").glob("*.xml"))]
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            entry = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 10, 20, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP integrity check failed")
        for path in files:
            if archive.read(path.relative_to(root).as_posix()) != path.read_bytes():
                raise ValueError(f"ZIP/source mismatch: {path}")
    print(output)


if __name__ == "__main__":
    main()
