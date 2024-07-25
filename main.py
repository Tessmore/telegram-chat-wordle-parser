from bs4 import BeautifulSoup
import dateutil
import argparse

'''
Example usage:

python main.py ./export/messages.html
'''

DEFAULT_TZ = "Europe/Amsterdam"

def process_html_file(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as html_file:
            contents = html_file.read()
            for line in parse_telegram_export(contents):
                print(line)
                # print(date, from_name)
                # print(text)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")

# Modified from
# https://gist.github.com/mrtj/049024345d37ed625e923abb267dc396
def parse_telegram_export(html_str, tz_name=DEFAULT_TZ):
    ''' Parses a Telegram html export.
    Params:
      - html_str (str): The html string containing the Telegram export.
      - tz_name (str|None): The name of the timezone where the export was made (eg. "Italy/Rome").
        If None, no time zone will be set for the resulting datetime.
    '''
    soup = BeautifulSoup(html_str, 'html.parser')
    tz = dateutil.tz.gettz(tz_name) if tz_name else None

    for div in soup.select("div.message.default"):
        body = div.find('div', class_='body')

        if not body:
            break

        from_name_ = body.find('div', class_='from_name')

        if from_name_ is not None:
            from_name = from_name_.string.strip()

        text_div = body.find('div', class_='text')

        if text_div:
            text = text_div.get_text().strip()

        raw_date = body.find('div', class_='date')['title']
        naiv_date = dateutil.parser.parse(raw_date)
        date = naiv_date.astimezone(tz) if tz else naiv_date

        yield (from_name, date, text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process HTML for Wordle scores")
    parser.add_argument("input_file", help="Path to the HTML file")
    args = parser.parse_args()

    process_html_file(args.input_file)
