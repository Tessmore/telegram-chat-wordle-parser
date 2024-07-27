README
======

Parses Telegram chat export for shared Wordle scores.

## Setup:

1. Export your chat (history) in Telegram
2. Copy the `messages*.html` over to the `export/` folder that you want to parse

## Installation:

* Install `pipx` (https://pipx.pypa.io/stable/installation/)
* Install Poetry (https://python-poetry.org/docs/#installing-with-pipx)

```
pipx install poetry
```

* Install dependencies:

```
poetry install
```

## Usage

Extract scores from all `./export/*` files

```
poetry run python main.py export | sort -V &> ./output/scores.csv
```
