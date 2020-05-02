import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from flask import current_app as app

def parse_data(date_str, content_str):
    pattern = r"(\d+)"

    m = re.findall(pattern, content_str)

    if m is None or len(m) < 4:
        print("No correct matches in ", content_str)
        return None
    elif len(m) > 4:
        print("More items found please check...")
        FLAG_WARN = True

    for match in m:
        print(match)
    reg, city, recov, dead, _ = m

    date_pattern = r"(\d{1,2}).[ ]?(\d{1,2}|\w*)[. ]?(\d{4}|), (\d{1,2}).(\d{2})"
    m = re.findall(date_pattern, date_str)
    # print(date_str)

    ## print(reg, city, recov, dead)

    day, month, year, hour, minute = [None] * 5

    if m is None or len(m) < 1:
        print("No matches in ", date_str)
    else:
        day, month, year, hour, minute = m[0]
    ## print(year, month, day, hour, minute)

    monthsmap = {
        "April": 4,
        "Mai": 5,
        "Juni": 6,
        "Juli": 7,
        "August": 8,
        "September": 9,
        "Oktober": 10,
        "Novemver": 11,
        "Dezember": 12

    }
    if month is not None and len(month) > 2:
        month = monthsmap[month]

    if year is not None and len(year) == 0:
        year = datetime.now().year

    try:
        date = datetime(
            year=int(year),
            month=int(month),
            day=int(day),
            hour=int(hour),
            minute=int(minute)
        )
    except:
        date = None

    result = {
        "timestamp": date,
        "cases_region": reg,
        "cases_city": city,
        "recovered": recov,
        "deaths": dead,
        "orig_date_str": date_str,
        "orig_data_str": content_str
    }
    # # print(result)
    return result


def fetch_and_parse_page_data():
    resp = requests.get(app.config["AACHEN_DATA_LINK_FULL"])
    if resp.status_code != 200:
        raise Exception("ExternalPageError")

    html = resp.text

    soup = BeautifulSoup(html, features="html.parser")
    page_contents_div = soup.find('div', 'content')
    content_sections = page_contents_div.find_all("h2")

    results = []
    for section in content_sections:
        # print("Current Node:", section.text)

        nextNode = section
        while True:
            if nextNode is None:
                break

            nextNode = nextNode.next_sibling
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = ""

            if tag_name == "h2":
                # print("*****")
                break
            elif tag_name == "ul":
                text = nextNode.find('li')
                parsed_data = parse_data(section.text, text.text)

                if parsed_data is not None:
                    results.append(parsed_data)
                # print("*****")
                break
            else:
                pass

    print("Results", results)
    return results