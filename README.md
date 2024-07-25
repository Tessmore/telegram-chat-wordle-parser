README
======

Parses Telegram chat export for shared Wordle scores.

## Setup:

1. Export your chat (history) in Telegram
2. Copy the `messages*.html` over to the `export/` folder that you want to parse

## Installation:

```
pip install beautifulsoup4
```

## Usage

Extract scores from all `./export/*` files and write them into an Excel sheet

```
bash extract.sh
```

## Testing

Run script directly on a file. This will list the found Wordle scores.

```
python main.py ./export/messages.html
```
