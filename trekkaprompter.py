import argparse
import fandom
import sys
import traceback

fandom.set_wiki('memory-alpha')
fandom.set_lang('en')

EP_TITLE_MARKER = ' (episode)'
DEFAULT_COUNT = 4
NEXT_RELEASE_START_TOKEN = 'released in all'
NEXT_RELEASE_TITLE_START_TOKEN = 'title="'
NEXT_RELEASE_TITLE_END_TOKEN = '"'
FIRST_EP_NAME = 'The Man Trap (episode)'

argp = argparse.ArgumentParser(
    prog='trekkaprompter',
    description='calculates watch orders for Star Trek by scraping the Memory Alpha fandom wiki'
)
argp.add_argument('page_title', type=str, nargs="?")
argp.add_argument('count', type=int, nargs="?", default=DEFAULT_COUNT)

def get_substring_before(source, prefix):
    return source[:source.find(prefix)]

def get_substring_after(source, prefix):
    return source[source.find(prefix)+len(prefix):]

def describe(page) :
    infobox = page.content['infobox']
    lines = infobox.split('\n')
    ep_data = lines[0].split(', Episode ')
    if len(ep_data) == 2 :  # episode
        [series, episode_num] = ep_data
        print('{0} {1} "{2}"'.format(series, episode_num, page.title.replace(EP_TITLE_MARKER, '')))
    else :                  # movie?
        show_name = lines[1]
        print('{0} "{1}"'.format(show_name, page.title.replace(EP_TITLE_MARKER, '')))
    sys.stdout.flush()

def get_next_released(page) :
    next_title = get_substring_before(
        get_substring_after(
            get_substring_after(
                page.html,
                NEXT_RELEASE_START_TOKEN
            ),
            NEXT_RELEASE_TITLE_START_TOKEN
        ),
        NEXT_RELEASE_TITLE_END_TOKEN
    )
    next = fandom.page(next_title)
    return next

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
