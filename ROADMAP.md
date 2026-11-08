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
- Sensitive: `logs/` holds real keystroke logs (see Needs Tan).

## Signal vs noise

Keep: `utils/validation.py` (Keystroke, KeystrokeList, JSON codec), `classes/key_analyzer.py`,
`classes/key_collector.py`, `classes/key_generator.py`, `client/` (the documented API),
`scripts/cli.py` + `scripts/simulate.py`, `utils/`.

Cut: `logs/*` (personal data), `UNUSED/`, `notebook.ipynb`, `init.py`, `classes/converter.py` +
`scripts/convert.py` and the constants only they use, `scripts/document.py` + `scripts/format.py` and
the generated `docs/client/` they produce.

## Stack

- `KeyMaster-1` (done): exact import, Analyze/collector fixes, pyproject + uv.lock, offline pytest
  suite (fake keyboard controller, recorded events, temp log dir), GitHub Actions CI, README, this file.
- `KeyMaster-2` (planned): remove committed `logs/`, create `logs/` on first write.
- `KeyMaster-3` (planned): cut dead code, experiments and generated docs listed above.

## Apply upstream

In a clean upstream checkout, one branch at a time. The base of `KeyMaster-1` is the import commit
`6534d06`; the base of `KeyMaster-N` is `KeyMaster-(N-1)`.

```bash
git -C <kranti-sandbox> fetch origin
git -C <kranti-sandbox> format-patch --relative=KeyMaster --stdout 6534d06..origin/KeyMaster-1 > km1.patch
git am km1.patch
uv sync --all-extras && uv run pytest   # Linux without a display: xvfb-run -a uv run pytest
```

## Needs Tan

1. `logs/example.log`, `logs/keystrokes.json` and `logs/simulated-keystrokes.json` contain real
   typed text (shell commands, chat prompts, personal prose). `KeyMaster-2` deletes them, but they
   stay in upstream history. Decide whether to rewrite history (e.g. `git filter-repo --path logs
   --invert-paths`) or accept it; nothing looked like a password, but check.
2. Live recording (`-l`) and typing into a real window were not verified (no desktop). Try
   `uv run python -m scripts.cli -l -d` and `-s "hi"` on your Mac.
3. macOS permission wording in the README (Accessibility, Input Monitoring) is from pynput's docs,
   not tested.
4. CI has not run on GitHub: the workflow only triggers once it sits at the upstream repo root.
   Its steps were run locally on Python 3.10 and 3.13 (`uv sync --locked --all-extras`, then
   `xvfb-run -a uv run pytest`: 23 passed).
5. Python floor raised to 3.10 (code already used `X | None`); CI runs 3.10 and 3.13.
6. pyperclip moved to an optional `clipboard` extra.
