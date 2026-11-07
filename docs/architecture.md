# Architecture and milestones

1. Establish source/build layout and XEX segment writer — implemented.
2. Install ANTIC display list and custom character set — implemented, full-system display check pending.
3. Implement steering, acceleration, traffic, projectiles, scoring and restart — implemented and CPU-tested.
4. Add tracking enemies, enemy fire, civilians, supplies, oil and difficulty — implemented and CPU-tested.
5. Ship reproducible artifacts and document remaining fidelity/validation work — implemented.

## Memory

- $2000 onward: executable, variables, graphics and display list (see dist/symbols.json).
- $6000–$63BF: 40x24 screen, safely inside one ANTIC 4 KB region.
- $6400–$67FF: copied OS character set, first eight glyphs replaced.
- $02E0–$02E1: executable run vector.

Uses the installed OS ROM character set at $E000 and OS shadow display/color/joystick registers. OS VBI remains enabled. No zero-page locations are reserved. Main waits on RTCLOK and updates on alternating ticks. Rendering uses self-modifying absolute store operands in RAM. Collision uses character-cell coordinates. Six object slots and one projectile per side bound CPU work. POKEY channel 1 produces engine and attack/crash sounds.

At the measured worst case in the seeded soak test, input/update/render consume 24,368 CPU cycles excluding OS VBI and ANTIC DMA. This is a budget estimate, not a frame-rate verification. Drawing occurs in place, so tearing remains possible and requires full-emulator assessment.

The assembler repeats symbol layout before a strict final pass because forward references may initially select zero-page opcodes. Final branches are range-checked; overlapping segments are rejected. Tests execute the final binary rather than reimplementing gameplay logic.

## Manual emulator checklist (not yet executed)

Configure Atari 800XL, 64 KB, standard OS, BASIC off. Load XEX. Confirm 24 rows, legible HUD, distinct sprites, engine and weapon sound. Test port 1 diagonals/fire and console SELECT. Verify flashing immunity, three-life game over and repeated restarts. Repeat under NTSC and PAL. Leave an unattended run for 10 minutes and verify no crashes. Native MAC/65 assembly and physical hardware loading are separate outstanding checks.
