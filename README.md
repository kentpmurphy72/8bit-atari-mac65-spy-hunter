# Road Agent — Atari 800XL

An original, compact Spy Hunter-inspired survival driving game. All runtime code is NMOS 6502 assembly in MAC/65-compatible syntax. Python is used only on the development machine for building and CPU-level tests. No original arcade assets or music are included.

## Play

Load `dist/road-agent.xex` using an Atari 800XL/64 KB emulator with BASIC disabled (hold OPTION during boot on hardware). Use joystick port 1:

- Left/right: steer across the highway.
- Up: accelerate (traffic approaches faster).
- Fire: shoot ahead; hold for repeated shots.
- SELECT: expend one oil charge to clear nearby traffic behind/alongside the car. Release before using again.
- Fire after GAME OVER: restart with three lives and three oil charges.

Your car faces up near the bottom. Enemy cars face down; tracking enemies move toward your column and fire. Civilian cars have square windows: shooting them suppresses scoring temporarily. Supply vehicles replenish oil to three charges when touched. A collision or enemy bullet costs a life, followed by flashing invulnerability. Passing vehicles earns points; destroying enemies earns two. After 100 points, spawn opportunities double. The HUD shows score, lives, and oil. There is no final level: survive and improve your score.

## Build and check

Python 3.10+ is the only prerequisite. The pinned BSD-licensed py65 1.2.0 dependency is included under `tools/vendor`, so the build needs no network or package installation.

```text
python tools/build.py
python tests/test_game.py
```

Output: `dist/road-agent.xex`, `dist/symbols.json`, and `dist/game.mac` (numbered ATASCII source for MAC/65 ENTER). The XEX contains the code/data segment and RUNAD at $02E0. Repeating the build produces identical bytes. See `docs/architecture.md` for memory and timing details.

The build tool implements only the MAC/65 subset used here, not the complete MAC/65 language. The source avoids cross-assembler-specific macros. Native MAC/65 assembly has not yet been tested; loading numbered source and selecting an object file through MAC/65's normal disk output workflow still requires validation.

## Validation and scope

The shipped executable is tested in py65's NMOS 6502 CPU simulator. Tests cover XEX entry metadata, steering, shooting, collisions, invulnerability, supplies, oil edge detection, enemy shots, game over, and 2,000 randomized updates. This does **not** emulate ANTIC, GTIA, POKEY, OS VBI, or joystick hardware. Display, sound, PAL/NTSC pacing, and loading in a full Atari emulator or on a physical 800XL remain unvalidated. No full Atari emulator was found in the inspected command path.

This is a compact playable first release, not an arcade-faithful finished recreation. Graphics are 8x8 monochrome character sprites with a scrolling lane-marker effect and a fixed straight road. There are no boats, helicopters, weapon trucks/docking, smoke, road forks, terrain transitions, arcade music, saved high scores, or pause menu. Oil is an immediate area attack rather than a persistent road hazard. PAL runs slower than NTSC. These are known scope limitations, not validated hardware restrictions.

## Repository

- `src/game.asm`: all game runtime and graphics data.
- `tools/build.py`: deterministic assembler frontend and XEX writer.
- `tools/vendor`: pinned py65 and its original license.
- `tests/test_game.py`: execution tests against the built binary.
- `dist`: ready-to-load executable and source export.
- `docs`: architecture and test notes.

Reference: [MAC/65 reference manual](https://www.atarimania.com/documents/MAC-65-Reference-Manual.pdf).
