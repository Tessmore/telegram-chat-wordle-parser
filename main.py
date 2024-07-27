import os
import re
import sys
import argparse
import dateutil
import openpyxl
import concurrent.futures
from bs4 import BeautifulSoup

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

'''
Example usage:

poetry run python main.py export
'''

DEFAULT_DIRECTORY = "export"
DEFAULT_TZ = "Europe/Amsterdam"

WORDLE_PATTERN = r"^Wordle (\d+\.?\d+) ([1-6])/([1-6])"

# Processes single file
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        contents = file.read()

    for result in parse_telegram_export(contents):
        yield result

# Processes directory (concurrently)
def process_html_file(directory=DEFAULT_DIRECTORY):
    html_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.html')]

    extracted_data_list = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(read_file, file): file for file in html_files}

        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]

            try:
                data = future.result()
                extracted_data_list.extend(data)
            except Exception as exc:
                print('%r generated an exception: %s' % (file, exc))

    return extracted_data_list

# Helper function to parse a chat message and detect a shared "Wordle" solution result
def parse_wordle(text):
    if not text:
        return None

    match = re.match(WORDLE_PATTERN, text.strip())

    if match:
        version, attempts, total_attempts = match.groups()
        return (version, int(attempts), int(total_attempts))
    else:
        return None

# Modified from
# https://gist.github.com/mrtj/049024345d37ed625e923abb267dc396
def parse_telegram_export(html_str, tz_name=DEFAULT_TZ):
    soup = BeautifulSoup(html_str, 'html.parser')
    tz = dateutil.tz.gettz(tz_name) if tz_name else None

    for div in soup.select("div.message.default"):
        body = div.find('div', class_='body')

        if not body:
            continue

        # Get the name of poster
        # NOTE: We must always extract this, as you can post multiple messages
        # and each follow up message from the same poster will have its
        # `from_name` omitted.
        from_name_ = body.find('div', class_='from_name')
        if from_name_ is not None:
            from_name = from_name_.string.strip()

        text_div = body.find('div', class_='text')
        if not text_div:
            continue

        text = text_div.get_text().strip()
        wordleResult = parse_wordle(text)

        if not wordleResult:
            continue

        if not from_name:
            continue

        # Get the post date
        raw_date = body.find('div', class_='date')['title']
        naiv_date = dateutil.parser.parse(raw_date)
        date = naiv_date.astimezone(tz) if tz else naiv_date

        yield (from_name, date.strftime("%d-%m-%Y %H:%M"), wordleResult, text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process HTML for Wordle scores")
    parser.add_argument("directory", help="Path to a directory containing the Telegram export (HTML files).")
    args = parser.parse_args()

    for (person, date, (version, attempts, total), _) in process_html_file(args.directory):
        print(f"\"Wordle {version}\",\"{attempts}/{total}\",\"{person}\",\"{date}\"")
