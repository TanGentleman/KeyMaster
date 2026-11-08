# KeyMaster

Records how you type, measures it, and types text back with human-like timing. Built on [pynput](https://pynput.readthedocs.io/); runs on your machine with no network.

```bash
git clone https://github.com/TanGentleman/KeyMaster && cd KeyMaster
uv sync --all-extras
uv run python -m scripts.demo   # record, analyze and generate made-up keystrokes; types nothing
```

Needs Python 3.11+ and [uv](https://docs.astral.sh/uv/); on Linux, an X server (`xvfb-run -a` without a display). Details: [IMPLEMENTATION.md](IMPLEMENTATION.md), [ROADMAP.md](ROADMAP.md).

MIT licensed.
