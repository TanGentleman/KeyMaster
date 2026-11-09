import pytest

import utils.helpers


@pytest.fixture(autouse=True)
def log_dir(tmp_path, monkeypatch):
    """Keep every test away from the real logs/ directory."""
    monkeypatch.setattr(utils.helpers, "LOG_DIR", str(tmp_path))
    monkeypatch.setattr(utils.helpers, "ABSOLUTE_REG_FILEPATH", str(tmp_path / "keystrokes.json"))
    monkeypatch.setattr(utils.helpers, "ABSOLUTE_SIM_FILEPATH", str(tmp_path / "simulated-keystrokes.json"))
    return tmp_path


class FakeController:
    def __init__(self):
        self.taps = []

    def tap(self, key):
        self.taps.append(key)


@pytest.fixture
def keyboard(monkeypatch):
    """Replace the pynput keyboard controller and sleep, so simulation types nothing."""
    import classes.key_generator as key_generator

    fake = FakeController()
    fake.sleeps = []
    monkeypatch.setattr(key_generator, "Controller", lambda: fake)
    monkeypatch.setattr(key_generator, "sleep", fake.sleeps.append)
    return fake
