#!/usr/bin/env python3
"""Check the package and optionally simulate its patches on game XML, read-only."""

import argparse
import copy
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "SevenDaysMaxLevel2000"


def inspect_package():
    metadata = ET.parse(MOD / "ModInfo.xml").getroot()
    if metadata.tag != "xml":
        raise ValueError("ModInfo.xml must have an xml root")
    for field in ("Name", "DisplayName", "Description", "Author", "Version"):
        node = metadata.find(field)
        if node is None or not node.get("value", "").strip():
            raise ValueError(f"Missing metadata field: {field}")
    patches = {}
    for name in ("progression.xml", "entityclasses.xml", "buffs.xml"):
        root = ET.parse(MOD / "Config" / name).getroot()
        if root.tag != "configs":
            raise ValueError(f"{name}: expected configs root")
        operations = []
        for node in root:
            xpath = node.get("xpath", "")
            value = (node.text or "").strip()
            if node.tag != "set" or "/@" not in xpath or value != "2000":
                raise ValueError(f"{name}: unexpected patch operation")
            operations.append((xpath, value))
        patches[name] = operations
    if [len(patches[name]) for name in patches] != [1, 2, 2]:
        raise ValueError("Expected one progression patch and two patches per other file")
    return patches


def select_attribute(root, xpath):
    """Evaluate this mod's simple attribute XPath subset using the standard library."""
    element_path, attribute = xpath.rsplit("/@", 1)
    prefix = f"/{root.tag}/"
    if not element_path.startswith(prefix):
        raise ValueError(f"Wrong XML root for {xpath}")
    nodes = root.findall("./" + element_path[len(prefix):])
    matches = [(node, attribute) for node in nodes if attribute in node.attrib]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one attribute, found {len(matches)}: {xpath}")
    return matches[0]


def check_config(config_dir, patches):
    for name, operations in patches.items():
        original = ET.parse(config_dir / name).getroot()
        simulated = copy.deepcopy(original)
        undo = []
        for xpath, value in operations:
            node, attribute = select_attribute(simulated, xpath)
            old_value = node.get(attribute)
            if old_value != "300":
                raise ValueError(
                    f"{name}: expected vanilla cap 300, found {old_value!r}: {xpath}"
                )
            undo.append((node, attribute, old_value))
            node.set(attribute, value)
            print(f"OK {name}: {old_value} -> {value}")
        for node, attribute, old_value in undo:
            node.set(attribute, old_value)
        if ET.tostring(simulated) != ET.tostring(original):
            raise ValueError(f"{name}: unexpected changes outside cap attributes")
    print("All five patches matched and simulated successfully. No files were changed.")
    print("This checks the base XML layout, not game runtime or other mod conflicts.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, help="Installed game's Data/Config folder")
    args = parser.parse_args()
    try:
        patches = inspect_package()
        print("Package XML and metadata checks passed.")
        if args.config_dir:
            check_config(args.config_dir, patches)
        else:
            print("Use --config-dir to also check the five targets against your game XML.")
    except (OSError, ET.ParseError, ValueError, SyntaxError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
