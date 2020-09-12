import requests
import sys
import pandas as pd

from bs4 import BeautifulSoup


def parse_html(content: str) -> dict:
    soup = BeautifulSoup(content, 'html.parser')
    if not soup:
        sys.exit("Could not make some soup. Sorry :(")

    programs = soup.findAll("ul", {"class":"program-list"})

    if len(soup) == 0:
        sys.exit("No data. Sorry :(")

    comph_programs = list()
    url_and_classes = dict()
    
    for program in programs:
            comph_programs += program.findAll('a')
    
    for i in comph_programs:
            url_and_classes[i.string] = f"https://catalog.usfca.edu/{i.get('href')}"

    return url_and_classes


def perf_request(url: str) -> dict:
    request = requests.get(url)

    if request.status_code != 200:
        sys.exit("Request not Valid. Sorry :(")

    parsed_data = parse_html(request.text)
    return parsed_data


def main():
    url = "https://catalog.usfca.edu/content.php?catoid=22&navoid=3107"
    program_dict = perf_request(url)
    df = pd.DataFrame.from_dict(program_dict, orient='index')
    df.to_csv('programs.csv')


if __name__ == '__main__':
    main()

