# Architecture and milestones

1. Establish source/build layout and XEX segment writer — implemented.
2. Install ANTIC display list and custom character set — implemented, full-system display check pending.
3. Implement steering, acceleration, traffic, projectiles, scoring and restart — implemented and CPU-tested.
4. Add tracking enemies, enemy fire, civilians, supplies, oil and difficulty — implemented and CPU-tested.
5. Ship reproducible artifacts and document remaining fidelity/validation work — implemented.

## Memory

- $2000 onward: executable, variables, graphics and display list (see dist/symbols.json).
- $6000–$63BF: 40x24 screen, safely inside one ANTIC 4 KB region.
- $6400–$67FF: copied OS character set, glyphs 64�127 replaced with multicolor tiles.
- $02E0–$02E1: executable run vector.

Uses the installed OS ROM character set at $E000 and OS shadow display/color/joystick registers. OS VBI remains enabled. No zero-page locations are reserved. Main waits on RTCLOK and updates on alternating ticks. Rendering uses self-modifying absolute store operands in RAM. Collision uses character-cell coordinates. Six object slots and one projectile per side bound CPU work. POKEY channel 1 produces engine and attack/crash sounds.

At the measured worst case in the seeded soak test, input/update/render consume 46,574 CPU cycles excluding OS VBI and ANTIC DMA. This is a budget estimate, not a frame-rate verification. Drawing occurs in place, so tearing remains possible and requires full-emulator assessment.

The assembler repeats symbol layout before a strict final pass. Unresolved labels provisionally use $2000 to keep forward RAM references in absolute addressing. Final branches are range-checked; overlapping segments are rejected. Tests execute the final binary rather than reimplementing gameplay logic.

## Manual emulator checklist (not yet executed)

Configure Atari 800XL, 64 KB, standard OS, BASIC off. Load XEX. Confirm 24 rows, legible HUD, distinct sprites, engine and weapon sound. Test port 1 diagonals/fire and console SELECT/OPTION; test three gears, truck reloading and the off-road boundary. Verify flashing immunity, three-life game over and repeated restarts. Repeat under NTSC and PAL. Leave an unattended run for 10 minutes and verify no crashes. Native MAC/65 assembly and physical hardware loading are separate outstanding checks.

## Multicolor revision

The first two rows use ANTIC 2 for the HUD; the remaining 22 use ANTIC 4. Vehicles occupy six tiles. A 24-byte edge table shifts bends down the screen. The lane-marking character patterns rotate by scanline using the speed accumulator. Oil/smoke share one timed rear effect. All code and tile data remain in the assembly source; tools/artwork.py is an optional source-art generator.

The latest build is prepared for user playtesting. Altirra was downloaded but no successful game load or interactive test was completed. The measured 46,574 cycles exceed one NTSC frame even before display DMA; do not infer 30 or 60 fps from the clock gate.
