# KeyMaster

Records your own typing with [pynput](https://pynput.readthedocs.io/), reports WPM and per-key
delays, plots them, and replays text as keystrokes with randomized delays. Runs on your machine;
no network.

## Quick start

Needs Python 3.11+ and [uv](https://docs.astral.sh/uv/) (CI uses uv 0.13.7).

```bash
git clone https://github.com/TanGentleman/KeyMaster && cd KeyMaster
uv sync --all-extras
uv run python -m scripts.cli -d -n -s "hello world"   # dry run: types nothing, logs nothing
uv run python -m scripts.cli --stats                  # "No recorded keystrokes yet" on a fresh clone
```

On Linux, pynput needs an X server, and its `evdev` dependency builds from source, so a system
Python needs its headers (`python3-dev`). uv's managed Python already has them
(`uv sync --managed-python --all-extras`).

## Commands

`uv run python -m scripts.cli [flags]`. With no script flag it types `-s STRING` into the focused
window after the initial lag.

| Flag | Effect |
| --- | --- |
| `-s STRING`, `--string` | Text to type. |
| `-c`, `--clipboard` | Type the clipboard instead (needs the `clipboard` extra, pyperclip). |
| `-l`, `--listen` | Record your typing for up to 30 s or 50 words; Esc or `*` stops. Then replays it unless `-d`. |
| `--stats` | Print log count, keystrokes, WPM and delays for `logs/keystrokes.json`, then exit. |
| `-d`, `--disable` | Don't type anything. |
| `-n`, `--no-log` | Don't append to the log files. |
| `-il SECONDS`, `--initial-lag` | Wait before typing; 0 to 30, default 3. |
| `-nn`, `--no-newlines` | Skip newlines when typing. |
| `-nu`, `--no-unicode` | Skip non-ASCII characters. |

Exit codes: `0` on success; `1` with a `ValueError` traceback for an `--initial-lag` outside 0-30.

Recorded runs are appended to `logs/keystrokes.json` and typed runs to
`logs/simulated-keystrokes.json`, both under the checkout. `logs/` is created on the first save and
is git-ignored.

## Python

```python
from client.analyze import Analyze
from client.generate import Generate
from client.configurate import Config

ks = Generate(Config(disable=True)).simulate_string("The quick brown fox")  # types nothing
print(Analyze(Config(logging=False)).get_stats(ks))
# {'keystroke_count': 19, 'average_delay': 0.0423, ...}; delays are random

Analyze().visualize()             # bar chart of average delay per key, from logs/keystrokes.json
Analyze().visualize(mode="box")   # box plot of all delays
```

## Test

```bash
uv sync --locked --all-extras
uv run pytest            # Linux without a display: xvfb-run -a uv run pytest
```

The tests fake the keyboard controller, the clipboard and `plt.show`, so they never type, listen or
open a window. CI runs the same two commands on Python 3.11 and 3.14 under `xvfb-run`.

## Boundaries

- Typing and recording act on whatever window has focus. macOS asks for Accessibility permission
  for your terminal (and Input Monitoring for `-l`), per pynput's docs.
- Never verified on a real desktop: live recording (`-l`) and typing into another window. Under
  Xvfb the pynput listener never returns, so only the faked paths are tested.
- Logs hold everything you typed while recording, in plain JSON.

## License

MIT
