import argparse
import fandom
import re
import sys
import traceback

fandom.set_wiki('memory-alpha')
fandom.set_lang('en')

EP_TITLE_MARKER = ' (episode)'
DEFAULT_COUNT = 4
FIRST_EP_NAME = 'The Man Trap (episode)'

EPISODE_RE = re.compile(r'^(.*), Episode (.*)$')
MOVIE_NUM_RE = re.compile(r'(?:← )?(\d+)(?:st|nd|rd|th) of ')
NEXT_RELEASED_RE = re.compile(r'released in all.*?title="([^"]+)"', re.DOTALL)

argp = argparse.ArgumentParser(
    prog='trekkaprompter',
    description='calculates watch orders for Star Trek by scraping the Memory Alpha fandom wiki'
)
argp.add_argument('page_title', type=str, nargs="?")
argp.add_argument('count', type=int, nargs="?", default=DEFAULT_COUNT)

def describe(page):
    infobox = page.content['infobox']
    first_line, _, remainder = infobox.partition('\n')
    episode_match = EPISODE_RE.match(first_line)
    if episode_match:  # episode
        series, episode_num = episode_match.groups()
        print(f'{series} {episode_num} "{page.title.replace(EP_TITLE_MARKER, "")}"')
    else:              # movie?
        movie_num_line = remainder.split('\n')[1]
        movie_num = MOVIE_NUM_RE.match(movie_num_line).group(1)
        print(f'FLM {movie_num} "{page.title}"')
    sys.stdout.flush()

def get_next_released(page):
    match = NEXT_RELEASED_RE.search(page.html)
    if match:
        next_title = match.group(1)
        return fandom.page(next_title)
    raise ValueError("Could not find next episode in release order")

if __name__ == '__main__' :
    args = argp.parse_args()

    count = args.count

    page = None

    if args.page_title :
        page_title = args.page_title
    else :
        page_title = FIRST_EP_NAME
        page = fandom.page(page_title)
        describe(page)
        count -= 1

    if not page_title.endswith(EP_TITLE_MARKER):
        try:
            page = fandom.page(page_title + EP_TITLE_MARKER)
        except Exception:
            pass
    if page is None:
        try:
            page = fandom.page(page_title)
        except fandom.error.PageError as e:
            print(e)
            sys.exit(1)

    for _ in range(count):
        try:
            page = get_next_released(page)
            describe(page)
        except Exception as e:
            print('Exception:', e)
            traceback.print_exception(e)
            sys.exit(1)
