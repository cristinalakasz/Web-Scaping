"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

# Month names to submit for, from Wikipedia:Selected anniversaries namespace
months_in_namespace = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def extract_anniversaries(html: str, month: str) -> list[str]:
    """Extract all the passages from the html which contain an anniversary, and save their plain text in a list.
        For the pages in the given namespace, all the relevant passages start with a month href
         <p>
            <b>
                <a href="/wiki/April_1" title="April 1">April 1</a>
            </b>
            :
            ...
        </p>

    Parameters:
        - html (str): The html to parse
        - month (str): The month in interest, the page name of the Wikipedia:Selected anniversaries namespace

    Returns:
        - ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parentheses); Event 2; Event 3, something, something\n'
                                {Month} can be any month in the namespace and {day} is a number 1-31
    """
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all paragraph elements
    paragraphs = soup.find_all('p')

    ann_list = []

    # Iterate over each paragraph
    for p in paragraphs:
        # Check if the paragraph contains a date link
        date_link = p.find('a', href=re.compile(
            r'^/wiki/{}_\d+$'.format(month)))
        if date_link:
            # Check if the date link is at the start of the paragraph
            if p.text.strip().startswith(date_link.text):
                # Extract the plain text of the paragraph
                text = p.get_text().replace('\n', '')
                ann_list.append(text)
    return ann_list


def anniversary_list_to_df(ann_list: list[str]) -> pd.DataFrame:
    """Transform the list of anniversaries into a pandas dataframe.

    Parameters:
        ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parenthesis); Event 2; Event 3, something, something\n'
                                {Month} can be any month in months list and {day} is a number 1-31
    Returns:
        df (pd.Dataframe): A (dense) dataframe with columns ["Date"] and ["Event"] where each row represents a single event
    """
    # Initialize an empty list to store the data
    data = []

    # Iterate over each annotation
    for ann in ann_list:
        # Partition the annotation into date and events using ':' as the separator
        date, _, events = ann.partition(':')

        if events:
            # Split events by semicolon, but ignore semicolons within parentheses
            event_list = re.split(r';(?![^(]*\))', events)

            # Iterate over each event
            for event in event_list:
                # Remove leading and trailing spaces from the event
                event = event.strip()

                if event:
                    # Append the date and event as a tuple to the data list
                    data.append((date, event))

    # Convert the data list into a pandas DataFrame with 'Date' and 'Event' as column names
    df = pd.DataFrame(data, columns=['Date', 'Event'])

    return df


def anniversary_table(
    namespace_url: str, month_list: list[str], work_dir: str | Path
) -> None:
    """Given the namespace_url and a month_list, create a markdown table of highlighted anniversaries for all of the months in list,
        from Wikipedia:Selected anniversaries namespace

    Parameters:
        - namespace_url (str):  Full url to the "Wikipedia:Selected_anniversaries/" namespace
        - month_list (list[str]) - List of months of interest, referring to the page names of the namespace
        - work_dir (str | Path) - (Absolute) path to your working directory

    Returns:
        None
    """
    # Loop through all months in month_list
    # Extract the html from the url (use one of the already defined functions from earlier)
    # Gather all highlighted anniversaries as a list of strings
    # Split into date and event
    # Render to a df dataframe with columns "Date" and "Event"
    # Save as markdown table

    # Convert work_dir to Path object for convenience
    work_dir = Path(work_dir)
    # Create output directory if it doesn't exist
    output_dir = work_dir / "tables_of_anniversaries"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Loop through each month
    for month in month_list:
        # Construct URL for the month-specific page
        page_url = f"{namespace_url}{month}"
        # Send GET request to the URL
        response = requests.get(page_url)
        # Get the HTML content from the response
        html = response.text

        # Extract list of anniversaries from the HTML
        ann_list = extract_anniversaries(html, month)
        # Convert list of anniversaries to DataFrame
        df = anniversary_list_to_df(ann_list)

        # Convert DataFrame to markdown table
        table = df.to_markdown(index=False)
        # Write markdown table to file
        with open(output_dir / f"anniversaries_{month.lower()}.md", 'w', encoding='utf-8') as f:
            f.write(table)


if __name__ == "__main__":
    # make tables for all the months
    work_dir = 'C:/Users/crist/OneDrive/Desktop/IN3110/IN3110-cristila/assignment4'
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    anniversary_table(namespace_url, months_in_namespace, work_dir)
