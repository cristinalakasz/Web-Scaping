"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt
import pandas as pd

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics",
                 "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats
    work_dir = Path(work_dir)
    country_dict = get_scandi_stats(url)

    stats_dir = work_dir / "olympic_games_results"
    stats_dir.mkdir(parents=True, exist_ok=True)

    # Plot the total number of gold medals for summer and winter Olympics using plot_scandi_stats function
    plot_scandi_stats(country_dict, stats_dir)

    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport

    best_in_sport = []
    medal = "Gold"

    for sport in sports_list:
        results = {}
        for country, country_info in country_dict.items():
            results[country] = get_sport_stats(country_info['url'], sport)

        # Plot the total number of gold, silver and bronze medals in the selected summer sports
        countries = list(results.keys())
        gold_medals = [results[country]['Gold'] for country in countries]
        silver_medals = [results[country]['Silver'] for country in countries]
        bronze_medals = [results[country]['Bronze'] for country in countries]

        plt.bar(countries, gold_medals, color='gold')
        plt.bar(countries, silver_medals, bottom=gold_medals, color='silver')
        plt.bar(countries, bronze_medals, bottom=[
                i+j for i, j in zip(gold_medals, silver_medals)], color='#cd7f32')
        plt.title(f'Total number of medals in {sport}')
        plt.savefig(stats_dir / f'{sport}_medal_ranking.png')
        plt.close()

        # Find the best country in number of gold medals in each sport
        best_country = find_best_country_in_sport(results, medal)
        best_in_sport.append((sport, best_country))

    # Create and save the md table of best in each sport stats
    with open(stats_dir / 'best_of_sport_by_Gold.md', 'w') as f:
        f.write('| Sport | Best Country |\n')
        f.write('|-------|--------------|\n')
        for sport, best_country in best_in_sport:
            f.write(f'| {sport} | {best_country} |\n')


def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """
    # Send a GET request to the provided URL
    response = requests.get(url)

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the 'List of NOCs with medals' table in the parsed HTML
    table = soup.find('table', {'class': ['wikitable', 'sortable']})

    country_dict = {}

    # If the table is found, iterate over each row (representing a country) in the table
    if table is not None:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')

            # If cells are found in the row, extract country name and medal counts
            if cells:
                country_link = cells[0].find('a')

                # If a link is found in the first cell (representing country name), extract information
                if country_link:
                    country_name = country_link.text.strip()

                    # If the country is a Scandinavian country, store its name, Wikipedia URL, and medal counts
                    if country_name in scandinavian_countries:
                        summer_medals = int(
                            cells[2].text.strip().replace(',', ''))
                        winter_medals = int(
                            cells[7].text.strip().replace(',', ''))
                        country_dict[country_name] = {
                            "url": "https://en.wikipedia.org" + country_link['href'],
                            "medals": {
                                "Summer": summer_medals,
                                "Winter": winter_medals,
                            },
                        }

    # Return the dictionary containing information about Scandinavian countries and their medal counts
    return country_dict


def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    response = requests.get(country_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with the title 'Medals by summer sport'
    table = soup.find('span', string=re.compile(
        'medals by summer sport', re.IGNORECASE)).find_parent('table')

    medals = {"Gold": 0, "Silver": 0, "Bronze": 0}

    # Find all rows in the table
    rows = table.find_all('tr')

    for row in rows:
        # Find all cells in the row
        header = row.find('th')
        if header:
            # The header contains the sport name
            sport_name = header.get_text(strip=True)
            if sport_name.lower() == sport.lower():
                # Find all cells in this row
                cells = row.find_all('td')
                if len(cells) >= 3:
                    # The first three cells contain the medal counts
                    medals["Gold"] = int(cells[0].get_text(strip=True))
                    medals["Silver"] = int(cells[1].get_text(strip=True))
                    medals["Bronze"] = int(cells[2].get_text(strip=True))
                break

    return medals


def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    # Initialize the best country and the maximum medal count
    best_country = []
    max_medals = 0

    # Iterate over each country and its medal counts
    for country, medals in results.items():
        # Check if this country has more of the given medal than the current best
        if medals.get(medal, 0) > max_medals:
            # Update the best country and the maximum medal count
            best_country = [country]
            max_medals = medals[medal]
        elif medals.get(medal, 0) == max_medals:
            # If there is a tie, add this country to the list of best countries
            best_country.append(country)

    # If all or none of the countries lead, return 'None'
    if len(best_country) in [0, len(results)]:
        return 'None'
    else:
        # Return the name(s) of the best country(ies)
        return '/'.join(best_country)


# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country names and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """
    # Convert output_parent to Path object if it's not None
    if output_parent is not None:
        output_parent = Path(output_parent)

    # Plot the total number of gold medals for summer and winter Olympics
    countries = list(country_dict.keys())
    summer_medals = [country_dict[country]['medals']['Summer']
                     for country in countries]
    winter_medals = [country_dict[country]['medals']['Winter']
                     for country in countries]

    plt.bar(countries, summer_medals, color='gold')
    plt.bar(countries, winter_medals, bottom=summer_medals, color='blue')
    plt.title('Total number of gold medals for summer and winter Olympics')

    # Save the plot if output_parent is provided
    if output_parent is not None:
        plt.savefig(output_parent / 'total_medal_ranking.png')

    plt.close()


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = 'C:/Users/crist/OneDrive/Desktop/IN3110/IN3110-cristila/assignment4'
    report_scandi_stats(url, summer_sports, work_dir)
