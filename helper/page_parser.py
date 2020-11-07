import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from flask import current_app as app

def parse_data(date_str, content_str):
    pattern_positives = r"(\d+) positive|nachgewiesen Infizierten auf (\d+)"
    pattern_revocered = r"(\d+) ehemals"
    pattern_deaths    = r"liegt[ nun]* bei (\d+)"
    pattern_kommunen  = r"\d+(/|\s{1,5})([\d]+)(/|\s{1,5})([\d]*)"

    reg = "".join(re.findall(pattern_positives, content_str)[0])
    recov = re.findall(pattern_revocered, content_str)[0]
    dead = re.findall(pattern_deaths, content_str)[0]
    m_kommunen = re.findall(pattern_kommunen, content_str)

    if m_kommunen is None or len(m_kommunen) < 10:
        print("No correct matches in for Kommunen data ", content_str)
        return None
    elif len(m_kommunen) == 10:
        m_kommunen.append(None)
        m_kommunen.append(None)
    elif len(m_kommunen) == 11:
        m_kommunen.insert(-1, None)
    elif len(m_kommunen) > 12:
        print("More items found for Kommunen please check...")
        FLAG_WARN = True

    aachen, alsdorf, baesweiler, eschweiler, herzogenrath, monschau, roetgen, simmerath, stolberg, wuerselen, not_associated, _ = list(map(lambda e: e[1], m_kommunen[:12]))

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
        "Januar": 1,
        "Februar": 2,
        "März": 3,
        "April": 4,
        "Mai": 5,
        "Juni": 6,
        "Juli": 7,
        "August": 8,
        "September": 9,
        "Oktober": 10,
        "November": 11,
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
        "cases_city": aachen,
        "recovered": recov,
        "deaths": dead,
        "orig_date_str": date_str,
        "orig_data_str": content_str,
        "alsdorf": alsdorf,
        "baesweiler": baesweiler,
        "eschweiler": eschweiler,
        "herzogenrath": herzogenrath,
        "monschau": monschau,
        "roetgen": roetgen,
        "simmerath": simmerath,
        "stolberg": stolberg,
        "wuerselen": wuerselen,
        "not_associated": not_associated
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