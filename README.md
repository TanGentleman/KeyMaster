# KeyMaster
## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Documentation](#documentation)
- [Workflows](#workflows)
- [Contributing](#contributing)
- [License](#license)

## Introduction
KeyMaster is a Python toolkit for collecting, analyzing, and generating keyboard event data. It is designed to scale the collection and analysis of keystroke data, as well as to create human-realistic simulation scripts. After countless "maybe I should clean this up first" moments have turned into hundreds of hours invested in the project, I'm proud to release the full source code for KeyMaster under the MIT License! With friendly documentation and open arms to Windows, Mac, and Linux users, I introduce the perfect tool to wield control over your keyboard.

## Installation

All you need need to install the two dependencies is the following terminal command:

```bash
pip install pynput==1.7.6 matplotlib==3.8.2
```

For convenience, I've included a `requirements.txt` file. To quickly get KeyMaster running from scratch, simply type the following commands in your terminal:

```bash
git clone https://github.com/TanGentleman/KeyMaster
cd KeyMaster
pip install -r requirements.txt
```
## Usage

For detailed usage of each class and method in KeyMaster, please refer to the `notebook.ipynb` jupyter notebook for a friendly walkthrough. For zero-code users, see the workflow examples for executable scripts.

## Features

KeyMaster offers a comprehensive suite of features designed to facilitate the collection, analysis, and simulation of keyboard event data. It consists of four main components:

- **Config**: This is the control center of KeyMaster. It allows you to manage the toolkit's behavior by setting simulation parameters, logging options, and data processing rules. The `Config` class offers fine-grain control over various settings, intelligent defaults, and seamless integration with other components of KeyMaster.

- **Analyze**: This component provides a suite of analytical tools to derive insights from keyboard event data. It offers versatile data handling, with methods for visualization, performance metrics, and more. With the `Analyze` class, you can effortlessly load and change log files, calculate words per minute (WPM), plot data without outliers, maintain clean datasets, and tailor the analysis environment to your needs.

- **Collect**: This is the gateway to capturing real-time keystroke data. It provides robust mechanisms to accurately record keyboard events and manage collected data. With the `Collect` class, you can capture and filter keystrokes as they occur in real-time, save collected data to log files, and pass the data to the Analyze or Generate objects with ease.

- **Generate**: This component is a powerful tool for creating realistic keystroke simulations. It enables users to generate and simulate typing behavior based on given strings or custom parameters. With the `Generate` class, you can match typing cadence, turn any string into rich keystroke data, and safely simulate keystrokes.

Each of these components is designed to work together seamlessly providing a comprehensive and user-friendly interface for keyboard event data collection, analysis, and simulation.

## Documentation

KeyMaster has documentation for each class and method, and can be referenced by markdown files in the `docs/` folder, amd in the docstrings of the appropriate files in the backend `classes/` and `utils`. Designed to be accessible for both beginners and advanced users, KeyMaster works best in conjunction with an IDE environment such as VSCode to take advantage of the strong type hints and hover documentation. I recommend experimenting using `notebook.ipynb` for an testing the deceptively simple and powerful structure of the toolkit.

## Workflows
- I've made some sample workflows for automation, with the backend in `scripts/simulate.py`, and an interface in `scripts/cli.py`
- This integrates well with a hotkey, for instance `option+v` to simulate typing of the clipboard contents (With custom speed, personalized behavior, exclusion of certain keys or unicode, etc.)

```bash
cd KeyMaster
python -m scripts.cli -s 'Use -c instead for clipboard string'
```

## Contributing
Contributions to KeyMaster are appreciated! If you have suggestions for improvements or new features, please feel free to create a new issue, and I'll get to it as soon as I can. Alternatively, fork the repository, make your changes, and submit a pull request!

## License
KeyMaster is released under the MIT License. This license allows you to use, modify, and distribute the code as you see fit. I believe strongly in the power of transparent, open-source code, and I hope to continue making this project accessible to everyone.

## Acknowledgments
Thank you for taking the time to explore KeyMaster. Despite it being a solo labor of love, I warmly welcome all feedback and contributions from the community!

Cheers,

Tan