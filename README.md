# KeyMaster - Keyboard Event Toolkit

## Quick Start

Install dependencies, with pyperclip being optional for clipboard simulation:
```bash
pip install pynput matplotlib
pip install pyperclip
```
Clone KeyMaster:
```bash
git clone https://github.com/TanGentleman/KeyMaster
cd KeyMaster
```

## Features

KeyMaster is a Python toolkit for collecting, analyzing, and simulating keyboard events. The object oriented framework has four simple classes:

- **Config**: Customize settings, simulation parameters, and data processing.
- **Analyze**: Analyze data, visualize, and calculate metrics like WPM.
- **Collect**: Record real-time keystrokes, save to logs, and filter events.
- **Generate**: Create realistic typing simulations with custom parameters.

## Usage

For detailed usage, refer to the `notebook.ipynb` Jupyter notebook. To initiate a sample workflow, run:
```bash
python -m scripts.cli
```
For automated simulation, utilize the many simple flags found in the docs:
```bash
python -m scripts.cli -s 'Use the -c flag instead to simulate your clipboard'
```

## Docs & Contributing

- Docs: Check `docs/` folder and the notebook.
- Contributions: Raise issues, fork, make changes, and submit pull requests.

## License

KeyMaster is MIT licensed. Use, modify, and distribute freely.

Cheers,

`Tan`