# KeyMaster roadmap

KeyMaster records your own typing with pynput, reports WPM and per-key delays, plots them, and
replays text (or your clipboard) as keystrokes with human-like timing. It is a personal
typing-analytics tool for your own keyboard, for one person at a terminal, not a library or service.

## Status (checked on upstream `bb5e6c0`, 2024-04-12)

- Install: `requirements.txt` pinned `pynput==1.7.6`, matplotlib unpinned; no lockfile, no CI.
  `pip install -r requirements.txt` works on Python 3.12.
- Tests: `python -m tests.run_tests` failed with `TypeError: Config.__init__() got an unexpected
  keyword argument 'disable_simulation'`; after fixing that it still asserted equality of two runs
  with random delays. `tests/compatibility.py` (codec tests) passed but was not collected by pytest.
- Bugs: `Analyze.get_stats(ks)`, `wpm(ks)`, `get_average_delay(ks)`, `visualize(ks)` and
  `get_highest_keystroke_times(ks)` ignored `ks` and used every loaded log. Plot labels for special
  keys never matched. The collector's first delay mixed `time()` and `perf_counter()`.
- CLI: `python -m scripts.cli -d -n -s "hello"` runs. Typing (`-s`) runs under Xvfb. Live
  recording (`-l`) is not verified: under Xvfb the pynput listener never returned, so it needs a
  manual check on a real desktop.
- Broken: `notebook.ipynb` calls `Analyze.visualize_keystroke_times()`, which does not exist.
  `scripts/convert.py` reads `logs/keystrokes.log`, a format nothing writes any more.
- Links: README/CHANGELOG links (GitHub issues, keepachangelog.com, pynput docs) return 200/302.
- Sensitive: `logs/` held real keystroke logs (see Needs Tan).

## Signal vs noise

Keep: `utils/validation.py` (Keystroke, KeystrokeList, JSON codec), `classes/key_analyzer.py`,
`classes/key_collector.py`, `classes/key_generator.py`, `client/` (the documented API),
`scripts/cli.py` + `scripts/simulate.py`, `utils/`.

Cut: `logs/*` (personal data), `UNUSED/`, `notebook.ipynb`, `init.py`, `classes/converter.py` +
`scripts/convert.py` and the constants only they use, `scripts/document.py` + `scripts/format.py` and
the generated `docs/client/` they produce.

## Stack

- `KeyMaster-1`: exact import, Analyze/collector fixes, pyproject + uv.lock, offline pytest
  suite (fake keyboard controller, recorded events, temp log dir), GitHub Actions CI, README, this file.
- `KeyMaster-2`: remove committed `logs/`, create `logs/` on first save.
- `KeyMaster-3`: cut the converter, `UNUSED/`, notebook, `init.py` and generated docs.
- `KeyMaster-4`: `--stats` CLI flag prints WPM and delays for your recorded logs.
- `KeyMaster-5`: pynput 1.8.2, matplotlib 3.11.2, pyperclip 1.11.0, pytest 9.2.0; Python 3.11+;
  CI on 3.11 and 3.14 with checkout v7.0.1, setup-uv v10.3.3 (SHA-pinned) and uv 0.13.7. Box plot
  moves from the deprecated `vert=False` to `orientation='horizontal'`. Tests for both plots (Agg)
  and the CLI's typing, clipboard and `--initial-lag` paths. README rewrite.
- `KeyMaster-6`: README explains the design (keystroke model, codec, timing model, Shift, stop
  conditions, banned keys, analysis) with a demo. `scripts/demo.py` runs record, save, analyze and
  generate on made-up keystrokes and redraws `docs/timing.png`; `tests/test_design.py` pins the
  described behaviour and the README's demo output. Fixes generated Shift insertion (behind
  `GENERATE_SHIFTS`, off by default), which put a Shift before every `#` in `##`.
- `KeyMaster-7`: README cut to 70 words; details moved to IMPLEMENTATION.md (`tests/test_design.py` reads
  the demo output from there).
- Not started, lower confidence: import pynput lazily so analysis runs without a display (the key
  model in `utils/validation.py` and `utils/settings.py` uses `pynput.keyboard.Key` directly), and
  package it as an installable `keymaster` command (needs renaming the top-level `classes`,
  `client`, `utils` and `scripts` packages).

## Apply upstream

In a clean upstream checkout. The import commit is `6534d06`; to apply the whole stack:

```bash
git -C <kranti-sandbox> fetch origin
git -C <kranti-sandbox> format-patch --relative=KeyMaster --stdout 6534d06..origin/KeyMaster-7 > km.patch
git am km.patch
uv sync --locked --all-extras && uv run pytest   # Linux without a display: xvfb-run -a uv run pytest
```

For one branch, use `origin/KeyMaster-(N-1)..origin/KeyMaster-N` instead.

## Needs Tan

1. `logs/example.log`, `logs/keystrokes.json` and `logs/simulated-keystrokes.json` contain real
   typed text (shell commands, chat prompts, personal prose). `KeyMaster-2` deletes them, but they
   stay in upstream history. Decide whether to rewrite history (e.g. `git filter-repo --path logs
   --invert-paths`) or accept it; nothing looked like a password, but check.
2. Live recording (`-l`) and typing into a real window were not verified (no desktop). Try
   `uv run python -m scripts.cli -l -d` and `-s "hi"` on your Mac. The macOS permission wording in
   IMPLEMENTATION.md is from pynput's docs, not tested.
3. CI has not run on GitHub: the workflow only triggers once it sits at the upstream repo root.
   Its commands were run locally on Python 3.11 and 3.14.
4. `KeyMaster-5` drops Python 3.10 (end of life since 2026-10; matplotlib 3.11 needs 3.11).
5. `KeyMaster-3` deletes the generated `docs/client/` pages and the notebook. Drop that branch if
   you want them; the notebook needs `visualize_keystroke_times` renamed to `visualize` first.
6. Generated keystrokes are scaled by the speed multiplier twice: once when their delays are drawn
   and again when typed, so the CLI default (speed 3) types about 9 times faster than speed 1
   (~14 ms a key). `KeyMaster-6` documents and tests this rather than changing it; decide whether
   typing should divide only recordings by speed.
