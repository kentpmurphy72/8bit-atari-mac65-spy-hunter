# Road Agent â€” Atari 800XL

An original, compact Spy Hunter-inspired survival driving game. All runtime code is NMOS 6502 assembly in MAC/65-compatible syntax. Python is used only on the development machine for building and CPU-level tests. No original arcade assets or music are included.

## Play

Load `dist/road-agent.xex` using an Atari 800XL/64 KB emulator with BASIC disabled (hold OPTION during boot on hardware). Use joystick port 1:

- Left/right: steer across the highway.
- Up/down: increase/decrease gear (1–3). Gear persists when released.
- Fire: shoot ahead; hold for repeated shots.
- SELECT: deploy oil behind the car.
- OPTION: deploy a wider smoke effect behind the car.
- Release the console button before using another charge; only one rear effect can be active.
- Fire after GAME OVER: restart with three lives and three charges of each rear weapon.

The white car is yours. Red cars are enemies; blue cars are civilians. The armored tracking enemy resists bullets and fires at you. Shooting civilians temporarily suppresses scoring. Align with a supply truck in gear 1 for twelve updates to replenish both rear weapons. Collisions, enemy bullets, and leaving the road cost lives; flashing marks temporary invulnerability. Score increases with survival, passing vehicles, and destroying enemies. After 100 points, spawn opportunities double. The HUD shows score, lives, oil, smoke, and gear.

## Build and check

Python 3.10+ is the only prerequisite. The pinned BSD-licensed py65 1.2.0 dependency is included under `tools/vendor`, so the build needs no network or package installation.

```text
python tools/build.py
python tests/test_game.py
```

Output: `dist/road-agent.xex`, `dist/symbols.json`, and `dist/game.mac` (numbered ATASCII source for MAC/65 ENTER). The XEX contains the code/data segment and RUNAD at $02E0. Repeating the build produces identical bytes. See `docs/architecture.md` for memory and timing details.

The build tool implements only the MAC/65 subset used here, not the complete MAC/65 language. The source avoids cross-assembler-specific macros. Native MAC/65 assembly has not yet been tested; loading numbered source and selecting an object file through MAC/65's normal disk output workflow still requires validation.

## Validation and scope

The current executable passes py65 NMOS 6502 tests for steering, shooting, collisions, invulnerability, truck reloading, oil/smoke activation, armored enemies, road bends, off-road damage, drawing bounds, enemy bullets, game over, and 2,000 randomized updates. This does **not** emulate ANTIC, GTIA, POKEY, OS VBI, or joystick hardware. Altirra was obtained, but interactive testing was stopped before the game was loaded. The user will playtest this build. Display, sound, PAL/NTSC pacing, native MAC/65 assembly, and physical 800XL loading remain unvalidated.

This revision replaces tiny monochrome cars with 2x3-tile multicolor vehicles (8x24 multicolor pixels), adds a bending highway, animated lane markings, persistent gears, oil and smoke effects, armored enemies, and simplified truck reloading. It remains a work in progress, not a finished arcade-faithful port. Boats, helicopters, road forks, terrain transitions, arcade music, saved high scores, and pause are absent. Rear effects have a fixed lifetime/location rather than fully simulated world motion; smoke's collision area is wider than its graphic. Truck docking uses overlap at low speed rather than a loading animation. Vehicle movement remains cell-based. Rendering is not double-buffered, and pacing/tearing need playtesting.

## Repository

- `src/game.asm`: all game runtime and graphics data.
- `tools/build.py`: deterministic assembler frontend and XEX writer.
- `tools/artwork.py`: optional regeneration of the original tile art embedded in the assembly.
- `tools/vendor`: pinned py65 and its original license.
- `tests/test_game.py`: execution tests against the built binary.
- `dist`: ready-to-load executable and source export.
- `docs`: architecture and test notes.

Reference: [MAC/65 reference manual](https://www.atarimania.com/documents/MAC-65-Reference-Manual.pdf).
