# Compatibility and research

Checked October 20, 2026.

## Current stable target

The Fun Pimps' [official Steam announcements](https://steamcommunity.com/app/251570/announcements/) list **V3.3.0 Stable**, released October 5, 2026, as the newest stable announcement. This is the PC/Steam version targeted by this mod. The official release announcement establishes the version; it does not certify this mod's compatibility.

## Sources and implementation

The game uses an XML `progression/level` element for the level cap and XP curve. Its own comment says the cap is also referenced by near-death-trauma buffs and entity classes. Actual V3.2 files were inspected from the versioned game-data mirror at [tassoneroberto/7dtd-assets](https://github.com/tassoneroberto/7dtd-assets/tree/d2267a3311ca2a1de92f29153c93d55000932de9/v3.2/Config), revision `d2267a3311ca2a1de92f29153c93d55000932de9`.

| Source file | Relevant settings |
| --- | --- |
| [progression.xml](https://github.com/tassoneroberto/7dtd-assets/blob/d2267a3311ca2a1de92f29153c93d55000932de9/v3.2/Config/progression.xml#L8) | Cap 300; base XP 10000; multiplier 1.05; cost clamp at 60; one skill point per level. |
| [entityclasses.xml](https://github.com/tassoneroberto/7dtd-assets/blob/d2267a3311ca2a1de92f29153c93d55000932de9/v3.2/Config/entityclasses.xml#L476) | Two playerMale death-XP branches split at 300. playerFemale inherits playerMale. |
| [buffs.xml](https://github.com/tassoneroberto/7dtd-assets/blob/d2267a3311ca2a1de92f29153c93d55000932de9/v3.2/Config/buffs.xml) | A cap check when adding near-death trauma and another when removing its marker. |

The mod sets these **five attributes** to 2000 with targeted XPath patches. It neither ships the full game configuration nor replaces progression trees. XP requirements, skill-point rewards, health/stamina effects, and perk ranks are untouched.

Research also found [Level Cap 500](https://little-method.itch.io/sdtd-mod-level-cap-500), whose author describes the same three-file approach, and [High Level Cap and HP Stamina Limit Remover](https://www.nexusmods.com/7daystodie/mods/7769), whose page was hidden when checked. The former targets a different cap and the latter changes additional stats. This repository implements the user's requested 2000 cap independently; no files from either mod were copied.

## Validation performed

- All mod XML parses, and ModInfo has the required identity, display name, description, author, and version fields.
- Each of the five patch selectors matches exactly one attribute in the inspected V3.2 files. Every matched source value is 300.
- Applying the patches in memory changes only those five attributes. The XP curve, skill-point rewards, other buff rules, and all remaining game XML are preserved.
- The two death-XP branches and the trauma removal condition use the same new boundary. The trigger retains vanilla's `LTE` comparison.
- The install ZIP was checked for the expected folder layout, contents, and matching source bytes.

**Limit:** V3.3.0 game XML and a running V3.3.0 client/server were not available for direct validation. These checks do not prove engine behavior at level 2000, save/reload behavior, multiplayer synchronization, or compatibility with other mods. The current build is a candidate for V3.3.0, configuration-validated against V3.2. Run the read-only checker on your installed files and the disposable-save procedure in the README before using a long-running save.

SHA-256 of inspected source files:

```text
progression.xml   8da3edd4f23c41d3a1ac9b4b645132f4453ebab5fa2df4be10590702c6c42db8
entityclasses.xml 61273a18ef343ee13adeb60a507d881892840f98fbf0dbeccf53f07440a833f7
buffs.xml         1ee7fdfc38931657688659e8c497b305db4b80e3c5d97d8b789340237d8a4cdb
```
