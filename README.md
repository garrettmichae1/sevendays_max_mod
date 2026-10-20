# 7 Days Max Level 2000

A small XML modlet that raises the **player level cap from 300 to 2000**, so an existing character can keep earning levels.

**Target:** 7 Days to Die **V3.3.0 stable, PC/Steam**, the latest stable release checked on October 20, 2026. **Validation status:** all five patches apply to real V3.2 game XML; V3.3.0 runtime compatibility has not been verified. Try a copy of your save first. [Research and validation details](docs/compatibility.md).

## Download and install

1. [Download SevenDaysMaxLevel2000-v1.0.0.zip](https://github.com/garrettmichae1/sevendays_max_mod/raw/refs/heads/main/dist/SevenDaysMaxLevel2000-v1.0.0.zip). You must be signed in to GitHub while this repository is private.
2. Exit the game and back up your save. On Windows, default saves are under `%APPDATA%\7DaysToDie\Saves`; custom user-data locations may differ.
3. In Steam, right-click **7 Days to Die → Manage → Browse local files**.
4. Create a `Mods` folder there if needed. Extract the ZIP into it.
5. Check that the path is exactly:

   ```text
   7 Days To Die/
     Mods/
       SevenDaysMaxLevel2000/
         ModInfo.xml
         Config/
           progression.xml
           entityclasses.xml
           buffs.xml
   ```

6. Launch the game and load a **copy** of your existing save to check it before continuing your main save.

Windows also supports `%APPDATA%\7DaysToDie\Mods`; use one install location. If you use GitHub's **Code → Download ZIP**, copy only the inner `SevenDaysMaxLevel2000` folder into `Mods`, not the entire repository folder.

No game files need replacing, and no DLL, Harmony, or mod manager is needed. This XML-only mod does not require disabling Easy Anti-Cheat.

## How leveling works

- The player cap becomes **2000**. Your character is intended to continue from its current level; the mod does not grant XP or reset progression.
- The existing XP curve and skill points per level are preserved. In vanilla, XP cost stops increasing after level 60, and each new level awards one skill point.
- The death XP penalty's cap checks move to 2000 together. Your selected death settings still apply, including any setting that disables XP loss.
- Perk ranks, crafting skills, and health/stamina growth keep their existing rules. Extra levels do not add new perks; points can accumulate after you have bought everything.

Higher player levels still participate in the game's normal difficulty calculations. This mod adds progression headroom, not new enemies, quests, or an overhaul.

## Multiplayer and other mods

Install on the host or dedicated server for a hosted game. A client-only installation cannot raise the cap on another person's server. These configuration patches are intended to use the server's normal XML synchronization; multiplayer has not been tested here.

Use one level-cap mod at a time. Mods that replace progression, modify the same cap checks, or overhaul death penalties need separate compatibility testing. Your other XP-rate settings are preserved because this mod does not write them.

## Check your installed version

The repository includes an optional **read-only** checker using Python 3, with no extra packages:

```powershell
python tools/check_compatibility.py --config-dir "C:\Program Files (x86)\Steam\steamapps\common\7 Days To Die\Data\Config"
```

Run it from this repository after changing the path to your actual installation. It verifies that every XPath selects exactly one existing attribute, then simulates the changes in memory. It does not change your installation or save. Passing this check confirms the configuration layout, not runtime behavior or compatibility with other mods.

For an in-game check, use a disposable save and check the F1 console/log for `SevenDaysMaxLevel2000` and XML patch errors. Use `help giveselfxp` before granting test XP, and give XP in moderate batches to check the **300 → 301**, **1999 → 2000**, and capped-at-2000 boundaries. Save, quit, and reload the test character to confirm the level and XP persist. Check death XP behavior below and at 2000 if XP-loss death settings are enabled. Do not run XP tests on your main character.

## Returning to vanilla

Keep the mod installed once a character exceeds level 300. Removing it restores the game's lower cap, and behavior for an over-cap character has not been verified. Restore your pre-mod save backup to return to vanilla.

## Build the install ZIP

```text
python tools/check_compatibility.py
python tools/build.py
```

The ZIP contains only the installable `SevenDaysMaxLevel2000` folder and its short instructions. Python is for development/checking only; the game loads the XML directly.
