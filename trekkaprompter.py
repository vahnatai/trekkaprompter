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

argp = argparse.ArgumentParser(
    prog='trekkaprompter',
    description='calculates watch orders for Star Trek by scraping the Memory Alpha fandom wiki'
)
argp.add_argument('page_title', type=str, nargs="?")
argp.add_argument('count', type=int, nargs="?", default=DEFAULT_COUNT)

def describe(page) :
    infobox = page.content['infobox']
    first_line, _, remainder = infobox.partition('\n')
    episode_match = re.compile(r'^(.*), Episode (.*)$').match(first_line)
    if episode_match :  # episode
        series, episode_num = episode_match.groups()
        print('{0} {1} "{2}"'.format(series, episode_num, page.title.replace(EP_TITLE_MARKER, '')))
    else :                  # movie?
        show_name, _, _ = remainder.partition('\n')
        print('{0} "{1}"'.format(show_name, page.title.replace(EP_TITLE_MARKER, '')))
    sys.stdout.flush()

def get_next_released(page) :
    match = re.compile(r'released in all.*?title="([^"]+)"', re.DOTALL).search(page.html)
    if match:
        next_title = match.group(1)
        return fandom.page(next_title)
    raise ValueError(f"Could not find next episode in release order")

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

    if not page_title.endswith(EP_TITLE_MARKER) :
        try :
            page = fandom.page(page_title + EP_TITLE_MARKER)
        except :
            pass
    if not page :
        page = fandom.page(page_title)

    for i in range(count) :
        try :
            page = get_next_released(page)
            describe(page)
        except Exception as e :
            print('Exception:', e)
            traceback.print_exception(e)
            exit()
