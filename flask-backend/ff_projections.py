import requests
import lxml.html as lh
import pandas
from bs4 import BeautifulSoup

# JS script that builds rankings table:
# https://g.espncdn.com/lm-static/ffl/tools/rankingsTable.js?slotCategoryId=0&scoringPeriodId=5&seasonId=2020&rankType=ppr&count=25&rand=2
# look for 'const getURl'
base_url = "https://fantasy.espn.com/football/tools/fantasyRankings"
params = ["slotCategoryId=0","scoringPeriodId=5","seasonId=2020","rankType=ppr","count=25","rand=2"]
full_url = base_url + "?" + "&".join(params)

def get_projections():
    r = requests.get(full_url)

    doc = lh.fromstring(r.content)
    tr_elements = doc.xpath('//tr')

    rankings = []
    # get analyst names as column headers
    th = tr_elements[0]
    header_row = [cell.text_content() for cell in th]

    # get player rankings
    all_tr = tr_elements[1:]
    for tr in all_tr:
        row = [cell.text_content().replace('\xa0',' ') for cell in tr]
        rankings.append(row)

    df = pandas.DataFrame(
            data=rankings,
            columns=header_row)

    # split column and re-order
    df[['Rank','Player']] = df["Rank, Player"].str.split('.', expand=True)
    df = df.drop("Rank, Player",1)
    cols = df.columns
    df = df[cols[-2:].append(cols[:-2])]
    return df.to_html()

def get_rankings():
    l = []
    base_url = "https://www.fantasypros.com/nfl/reports/leaders/qb.php?year=2020&start=4&end=4"
    r = requests.get(base_url,
                 headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all_tr = soup.find("tbody").find_all("tr")
    rankings = []
    for tr in all_tr:
        center_tds = tr.find_all("td", {"class":"center"})
        rank = center_tds[0].text
        team =  center_tds[1].text
        score = center_tds[2].text
        player = tr.find("a", {"class":"player-name"}).text
        player_team = "%s, %s" % (player, team)
        rankings.append([rank, player_team, score])
    df = pandas.DataFrame(
            data=rankings,
            columns=["Ranking","Player","Score"])
    return df.to_html()
