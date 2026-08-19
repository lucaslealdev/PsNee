# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PSNee is AVR firmware for a PlayStation 1 modchip. It removes disc region locks by sniffing the
CD-ROM controller's SUBQ subchannel data and, when it detects the region-check lead-in area,
injecting a fake SCEx license string on the DATA line. On consoles whose BIOS enforces a second,
independent region check, it additionally does a real-time BIOS patch: it overrides the BIOS data
bus (DX) for a few CPU cycles at a precisely counted address-bus (AX/AY) pulse, forcing an
alternate code path. There is no host-side tooling, app, or test suite — this is a single Arduino
sketch flashed onto the chip that goes inside the console.

## Repository layout

- `PSNee/PSNee.ino` — main firmware: console model `#define`s (commented, exactly one must be
  uncommented), `Bios_Patching()`, `BoardDetection()`, `CaptureSUBQ()`, `FilterSUBQSamples()`,
  `PerformInjectionSequence()`, `Init()`/`main()`.
- `PSNee/settings.h` — per-console-family timing constants (`SILENCE_THRESHOLD`, `PULSE_COUNT`,
  `BIT_OFFSET_CYCLES`, `OVERRIDE_CYCLES`, etc.), region selection (`INJECT_SCEx`), debug-log
  helpers, and compile-time sanity checks (`#error`/`#pragma message`).
- `PSNee/MCU.h` — per-MCU-family (`ATmega328/168`, `ATmega32U4`, `ATtiny25/45/85`, plus
  work-in-progress `ATtiny88_48`/`ATtiny214_414`/`LGT8F328P` sections) pin/register mappings,
  interrupt vector wiring, and `OptimizePeripherals()` (power-down of unused peripherals, run in
  `.init3` before `main()`).
- `changelog` — chronological project history; check it for the rationale behind
  non-obvious timing/logic choices before changing them.
- `images/` — wiring diagrams, board photos, MCU pinouts referenced by the README/Wiki.
- `wiki/` — local mirror of the [project Wiki](https://github.com/kalymos/PsNee/wiki) (gitignored,
  not committed — re-fetch with `git clone https://github.com/kalymos/PsNee.wiki.git` if missing).
  Detailed hardware install instructions, board/BIOS diagrams, per-board pinouts, protected-game
  lists, and anti-modchip background live here, not in this repo's tracked files.
- `docs/` — static, framework-free GitHub Pages site (English/Portuguese/Spanish) documenting how
  PSNee works, the Arduino Nano flashing guide, and one installation page per PS1 motherboard
  (PU-7/8/16/18/20/22/23, PM-41, PM-41 (2)). Set the repo's Pages source to `main` / `/docs` to
  publish it. The HTML pages (`index.html`, `devices/*.html`, `boards/*.html`) are **generated,
  not hand-edited** — content/structure lives in `docs/tools/gen_site.py` (board data, page
  templates, the `fig()` helper); edit that script and rerun `python3 docs/tools/gen_site.py`
  rather than editing the `.html` output directly, or edits will be lost on the next regen. All
  pages share `assets/css/style.css` and `assets/js/i18n.js`; page text lives in
  `assets/i18n/{en,pt,es}.json` under `data-i18n="a.b.c"` keys (see `docs/assets/js/i18n.js` for the
  lookup/array/HTML-attr conventions) — edit the JSON, not hardcoded strings, and keep all three
  language files structurally identical. Board/Arduino/BIOS photos are re-compressed copies of the
  root `images/` originals (via Pillow, JPEG ~1400px) living under `docs/assets/images/`; if source
  images change, regenerate rather than copying the multi-MB originals in directly. Every content
  image also has a small `*-thumb.*` sibling (via `python3 docs/tools/gen_thumbs.py`, ~640px) that
  `fig()` uses for the inline preview — the lightbox zoom and "open in new tab" link still point at
  the full-resolution file, so a page never downloads a 1400px photo just to show a small preview.
  `HAS_THUMB` in `gen_site.py` and `CONTENT_IMAGES` in `gen_thumbs.py` must stay in sync; a few
  already-tiny line-art diagrams (PSNee pinout, LED/switch wiring) are deliberately excluded since
  downsizing them further doesn't help.

## Configuring and building

This is a plain Arduino sketch with no build system checked into the repo (no `platformio.ini`,
no `Makefile`, no CI). Configuration is done by editing source before compiling:

1. In `PSNee/PSNee.ino`, uncomment **exactly one** `SCPH_xxxx` console-model `#define` at the top
   of the file. Compilation deliberately fails (`#error`) if zero or more than one is selected.
   Models requiring a BIOS patch are listed separately from those that only need standard SCEx
   injection; check the BIOS-version/CRC comments next to each — BIOS version matters more than
   the SCPH number.
2. In `PSNee/settings.h`, adjust options as needed (`REQUEST_INJECT_TRIGGER`,
   `REQUEST_INJECT_GAP`, `LED_RUN`, `PATCH_SWITCHE`, `DEBUG_SERIAL_MONITOR`) — comments above each
   `#define` explain valid ranges and hardware wiring implications.
3. Compile and flash with the Arduino IDE (or `arduino-cli`) targeting the matching board
   (ATmega328/168, ATmega32U4, or ATtiny25/45/85 per the supported-hardware list in `README.md`).
   **Models that require a BIOS patch must be flashed via an ISP programmer, not the Arduino
   bootloader** — the bootloader's startup delay is long enough to miss the boot-time patch
   window. Fuse settings for ATmega32U4 and ATtiny are documented in the pinout/fuses table at
   the top of `settings.h`'s companion comments in `PSNee.ino`.
4. There is no automated test suite; validation is done on real console hardware (or a logic
   analyzer capturing SQCK/SUBQ/WFCK/DATA), which Claude Code cannot do. State explicitly when a
   change is unverified on hardware.

## Architecture notes

- **MCU abstraction via macros, not HAL functions.** `MCU.h` defines one macro set
  (`PIN_DATA_INPUT`, `PIN_SQCK_READ`, `PIN_AX_INTERRUPT_ENABLE`, ...) per MCU family, guarded by
  `#if defined(__AVR_...__)`. `PSNee.ino` and `settings.h` are written against these macro names
  only and never touch AVR registers directly. When adding a new MCU family, add a new guarded
  block defining the full macro set (including `OptimizePeripherals()`) rather than adding
  `#ifdef`s to the shared logic.
- **Two independent state machines run in sequence:** `Bios_Patching()` (optional, only for
  consoles whose BIOS does its own region check) runs once at boot inside `Init()`, before the
  main loop starts. The main loop in `main()` then continuously calls `CaptureSUBQ()` →
  `FilterSUBQSamples()` → conditionally `PerformInjectionSequence()`. These do not share pins or
  state and should be reasoned about separately.
- **`Bios_Patching()` is hard-realtime and cycle-counted, not just interrupt-driven.** It
  synchronizes to the AX address-pulse edge, counts a fixed number of silent windows to identify
  the boot stage, then arms an ISR (`PIN_AX_INTERRUPT_VECTOR`) that fires on the Nth pulse and
  uses `__builtin_avr_delay_cycles()` (not `_delay_us()`) for sub-instruction-accurate bus timing.
  The per-console constants in `settings.h` (`SILENCE_THRESHOLD`, `PULSE_COUNT`,
  `BIT_OFFSET_CYCLES`, `OVERRIDE_CYCLES`) were tuned empirically per MCU family/clock speed on
  real hardware — do not adjust them without a way to verify against actual console timing.
  `PHASE_TWO_PATCH` consoles (SCPH-1000/3000) repeat the same pattern on a second address line
  (AY) via a second ISR.
- **`BoardDetection()` picks the injection method at boot** by sampling WFCK: legacy boards
  (PU-7..PU-20) hold it as a static gate signal, while PU-22+ boards drive it as an oscillating
  clock. The result (`wfck_mode`) branches `PerformInjectionSequence()` between pulse-counted sync
  (modern boards) and a fixed `_delay_us()` timing loop (legacy boards).
- **`FilterSUBQSamples()` has a distinct SCPH-5903 variant** (`#ifdef SCPH_5903`) because that
  console's VCD (Video CD) drive emits SUBQ patterns that would otherwise be misidentified as the
  region-check lead-in; it explicitly excludes VCD lead-in sub-mode markers that the standard
  variant doesn't need to check for.
- **`request_counter` is a hysteresis/debounce counter, not a simple flag**: it increments on
  matching SUBQ patterns and decrements on mismatches, only triggering injection once it crosses
  `REQUEST_INJECT_TRIGGER`, then resets to `REQUEST_INJECT_TRIGGER - REQUEST_INJECT_GAP` (not to
  0) so a natural gap follows each injection. This mimics genuine CD timing to defeat anti-mod
  detection — `settings.h` comments document the safe tuning ranges for both constants.
- **`DEBUG_SERIAL_MONITOR` changes runtime behavior, not just logging verbosity**: it pulls in
  `Serial`/`Serial1`/`SoftwareSerial` depending on MCU family, and on ATtiny it's mutually
  exclusive with `LED_RUN` (both want PB3) — enforced by a compile-time `#error` in `settings.h`.
