# trekkaprompter

A small CLI that prints upcoming Star Trek watch-order entries by scraping the Memory Alpha wiki via the `fandom` Python package. Currently focused on the "Next released in all" ordering.

## Requirements

- Python 3.9+
- Internet access
- Package dependency:
need my fixed fork of fandom-py

```bash
pip install git+https://github.com/vahnatai/fandom-py-fixes.git
```

## Usage

```bash
python trekkaprompter.py [page_title] [count]
```

- `page_title` (optional): Episode/movie page title to start from.
  - If omitted, starts from `The Man Trap (episode)`.
  - You can pass either with or without the ` (episode)` suffix.
- `count` (optional): Number of entries to print after the starting point.
  - Default: `4`

## Examples

Start from the default first TOS episode:

```bash
python trekkaprompter.py
```

Start from a specific episode and print the next 6 entries:

```bash
python trekkaprompter.py "The Naked Time" 6
```

Start from a movie page title:

```bash
python trekkaprompter.py "Star Trek: The Motion Picture" 3
```

## Output format

- Episode pages:
  - `<Series> <EpisodeNumber> "<EpisodeTitle>"`
- Non-episode pages (for example movies):
  - `<ShowOrFranchiseName> "<Title>"`

## Notes

- Data is scraped live from Memory Alpha (`memory-alpha` wiki, English).
- If page structure changes on the wiki, parsing may fail and print an exception.
