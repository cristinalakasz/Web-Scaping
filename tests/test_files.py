from pathlib import Path

import pytest


@pytest.fixture
def assignment4():
    return Path(__file__).parent.parent.resolve()


def test_location(assignment4):
    # check that we're in repo root/assignment4
    assert (
        assignment4.name == "assignment4"
    ), "Assignment is not in the correct `assignment4` directory!"


@pytest.mark.parametrize(
    "filename",
    [
        "requesting_urls.py",
        "filter_urls.py",
        "collect_dates.py",
        "find_anniversaries.py",
        "fetch_olympic_statistics.py"
        # "wiki_race_challenge.py",
    ],
)
def test_files_exist(assignment4, filename):
    """Check if the required scripts and top-level files are submitted"""
    assert assignment4.joinpath(filename).exists()


def test_tables_of_anniversaries(assignment4):
    """Check if tables_of_anniversaries is present in the submission
    directory
    """
    assert (
        assignment4 / "tables_of_anniversaries"
    ).exists(), "Missing tables_of_anniversaries directory"


@pytest.mark.parametrize(
    "filename",
    [
        "anniversaries_january.md",
        "anniversaries_february.md",
        "anniversaries_march.md",
        "anniversaries_april.md",
        "anniversaries_may.md",
        "anniversaries_june.md",
        "anniversaries_july.md",
        "anniversaries_august.md",
        "anniversaries_september.md",
        "anniversaries_october.md",
        "anniversaries_november.md",
        "anniversaries_december.md",
    ],
)
def test_files_in_tables_of_anniversaries(assignment4, filename):
    """Check if tables_of_anniversaries contains all the required files"""
    assert (
        assignment4 / "tables_of_anniversaries" / filename
    ).exists(), f"Missing file {filename} inside tables_of_anniversaries directory"


def test_olympic_games_results(assignment4):
    """Check if olympic_games_results is present in the submission
    directory
    """
    assert (
        assignment4 / "olympic_games_results"
    ).exists(), "Missing olympic_games_results directory"


@pytest.mark.parametrize(
    "filename",
    [
        "Archery_medal_ranking.png",
        "Athletics_medal_ranking.png",
        "Cycling_medal_ranking.png",
        "Football_medal_ranking.png",
        "Handball_medal_ranking.png",
        "Sailing_medal_ranking.png",
        "total_medal_ranking.png",
        "best_of_sport_by_Gold.md",
    ],
)
def test_files_in_olympic_games_results(assignment4, filename):
    """Check if olympic_games_results contains all the required files"""

    assert (
        assignment4 / "olympic_games_results" / filename
    ).exists(), f"Missing file {filename} inside olympic_games_results directory"
