"""
Bonus task
"""
from __future__ import annotations
import requests
from bs4 import BeautifulSoup
from collections import deque


def find_path(start: str, finish: str) -> list[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    # Initialize dictionary, to track of visited URLs and their parent URLs
    visited = {start: None}
    # Initialize queue with start URL
    queue = deque([start])

    # Continue until queue is empty
    while queue:
        # Pop the next URL from the front of the queue
        url = queue.popleft()
        if url == finish:
            path = []
            # Follow the path backward from finish to start
            while url is not None:
                path.append(url)
                url = visited[url]
            # Reverse the path so it goes from start to finish and return it
            return path[::-1]

        try:
            # Fetch the content of the current URL, and parse with BeautifulSoup
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Iterate over all 'a' tags (links) in the HTML content
            for link in soup.find_all('a'):
                href = link.get('href')
                # If this link is a relative link to another Wikipedia article, follow it
                if href and href.startswith('/wiki/') and ':' not in href:
                    next_url = 'https://en.wikipedia.org' + href
                    # If this URL has not been visited yet, add it to the queue and mark it as visited
                    if next_url not in visited:
                        visited[next_url] = url
                        queue.append(next_url)
        except Exception as e:
            print(f"Error: {e}")
    # If visited all reachable URLs without finding the finish URL, return empty list
    return []


if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"
    path = find_path(start, finish)
    assert path[0] == start
    assert path[-1] == finish

    if path is None:
        print(f"No path found from {start} to {finish}")
    else:
        print(f"Got from {start} to {finish} in {len(path)-1} links")
