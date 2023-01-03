## PyPod

[![PyPI](https://img.shields.io/pypi/v/python-pod)](https://pypi.org/project/python-pod/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/python-pod)


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)


![screenshot](https://github.com/bmwant/pypod/blob/main/assets/player_ui.png)


Python console music player

### Installation

```bash
$ pip install python-pod
```

### Usage
```bash
$ pypod <path-to-directory>  # play everything under the folder
$ pypod filename.wav  # play single file
```

### Development

```bash
$ brew install portaudio
$ poetry install --with dev

$ make debug  # run app in debug mode
$ make console  # run textual dev console
```
