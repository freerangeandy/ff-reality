import requests
import lxml.html as lh
import pandas
from bs4 import BeautifulSoup

slotIDs = { "qb": "0", "rb": "2", "wr": "4", "te": "6"}
def get_projections(week, position):
    # JS script that builds projections table:
    # https://g.espncdn.com/lm-static/ffl/tools/rankingsTable.js?slotCategoryId=0&scoringPeriodId=5&seasonId=2020&rankType=ppr&count=25&rand=2
    # look for 'const getURl'
    base_url = "https://fantasy.espn.com/football/tools/fantasyRankings"
    slotID = slotIDs[position]
    params = ["slotCategoryId=%s" % (slotID),"scoringPeriodId=%s" % (week),"seasonId=2020","rankType=ppr"]
    if position == "qb":
        params.append("count=25")
    full_url = base_url + "?" + "&".join(params)
    r = requests.get(full_url)

    doc = lh.fromstring(r.content)
    tr_elements = doc.xpath('//tr')

    rankings = []
    # get analyst names as column headers
    th = tr_elements[0]
    header_row = [cell.text_content() for cell in th]
    header_row[1] = "Opponent"

    # get player projections
    all_tr = tr_elements[1:]
    for tr in all_tr:
        row = [cell.text_content().replace('\xa0',' ') for cell in tr]
        rankings.append(row)

    df = pandas.DataFrame(
            data=rankings,
            columns=header_row)
    # split column and re-order
    df[['Projected Ranking (consensus)','Player']] = df["Rank, Player"].str.split('.', n=1, expand=True)
    df = df.drop("Rank, Player",1)
    cols = df.columns
    df = df[cols[0:1].append(cols[-2:]).append(cols[1:-2])]
    df['Player'] = df['Player'].apply(normalized_player)
    df.set_index("Player", inplace=True)
    print("week %s projections loading..." % (week))
    return df

def get_rankings(week, position):
    l = []
    base_url = "https://www.fantasypros.com/nfl/reports/leaders/%s.php?year=2020&start=%s&end=%s" % (position, week, week)
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
            columns=["Actual Ranking","Player","PPR Score"])
    df['Player'] = df['Player'].apply(normalized_player)
    df.set_index("Player", inplace=True)
    print("week %s rankings loading..." % (week))
    return df

def normalized_player(full_str):
    split_str = full_str.strip().split(' ', 2)
    if split_str[1][-1] == ',':
        split_str[1] = split_str[1][:-1]
    return "%s %s" % (split_str[0], split_str[1])

analysts = ['Berry', 'Karabell', 'Yates', 'Cockcroft', 'Clay', 'Dopp']
positions = ['qb', 'rb', 'wr', 'te']
# dataframe row methods
def diff_analyst_result(row, analyst):
    try:
        return int(row[analyst]) - int(row['Actual Ranking'])
    except ValueError as ve:
        return 26 - int(row['Actual Ranking'])
def diff_consensus_result(row):
    try:
        return int(row['Projected Ranking (consensus)']) - int(row['Actual Ranking'])
    except ValueError as ve:
        return 26 - int(row['Actual Ranking'])
def analyst_std_dev(df, cols):
    std_devs = [df[col].std() for col in cols]
    return [std_devs]

def get_comparison(week, position, analyst=None):
    rankings_df = get_rankings(week, position)
    if rankings_df.empty == True:
        return None
    projections_df = get_projections(week, position)

    df = projections_df.join(other=rankings_df, on='Player')
    if analyst != None:
        drop_analysts = analysts
        drop_analysts.remove(analyst)
        df.drop(columns=drop_analysts, inplace=True)
        df['Diff (analyst - result)'] = df.apply(diff_analyst_result, axis=1, analyst=analyst)
        df['Diff (consensus - result)'] = df.apply(diff_consensus_result, axis=1)
    return df

def get_full_comparison(week, position):
    rankings_df = get_rankings(week, position)
    if rankings_df.empty == True:
        return None
    projections_df = get_projections(week, position)
    deviation_df = projections_df.join(other=rankings_df, on='Player')
    # replace analyst (and consensus) projections with deviations from actual rankings
    for analyst in analysts:
        deviation_df[analyst] = deviation_df.apply(diff_analyst_result, axis=1, analyst=analyst)
    deviation_df['Consensus'] = deviation_df.apply(diff_consensus_result, axis=1)
    # shorten/drop column names
    deviation_df.drop(columns=['PPR Score','Projected Ranking (consensus)', 'AVG'], inplace=True)
    deviation_df = deviation_df.rename(columns={'Actual Ranking':'Actual'})
    # shift Actual column
    cols = deviation_df.columns
    cols = cols[0:1].append(cols[-2:-1]).append(cols[1:-2]).append(cols[-1:])
    deviation_df = deviation_df[cols]
    # shorten column names for projections table
    projections_df = projections_df.rename(columns={'Projected Ranking (consensus)':'Consensus'})
    # shift Consensus column
    cols = projections_df.columns
    cols = cols[0:1].append(cols[2:]).append(cols[1:2])
    projections_df = projections_df[cols]
    # std dev table
    std_dev_columns = analysts
    std_dev_columns.append('Consensus')
    std_dev_df = pandas.DataFrame(
        index=['Standard Deviation'],
        data=analyst_std_dev(deviation_df, std_dev_columns),
        columns=std_dev_columns
    )

    return (projections_df, deviation_df, std_dev_df)
