from pathlib import Path

import pytest
from fetch_olympic_statistics import (
    find_best_country_in_sport,
    get_scandi_stats,
    get_sport_stats,
    report_scandi_stats,
)

# NOTE: The wiki links are permanent links, meaning they point to snapshots of
# the corresponding wiki page at a certain time. These links were retrieved in July 2023,
# so the real statistics at the current time might differ from the ones
# in these snapshots.


@pytest.mark.task41
@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://en.wikipedia.org/w/index.php?title=All-time_Olympic_Games_medal_table&oldid=1165685442",
            {
                "Denmark": {
                    "url": "https://en.wikipedia.org/wiki/Denmark_at_the_Olympics",
                    "medals": {"Summer": 48, "Winter": 0},
                },
                "Norway": {
                    "url": "https://en.wikipedia.org/wiki/Norway_at_the_Olympics",
                    "medals": {"Summer": 61, "Winter": 148},
                },
                "Sweden": {
                    "url": "https://en.wikipedia.org/wiki/Sweden_at_the_Olympics",
                    "medals": {"Summer": 147, "Winter": 65},
                },
            },
        ),
    ],
)
def test_get_scandi_stats(url, expected):
    country_dict = get_scandi_stats(url)
    assert sorted(country_dict.keys()) == ["Denmark", "Norway", "Sweden"]
    assert country_dict == expected


@pytest.mark.task42
@pytest.mark.parametrize(
    "country_url, sport, expected",
    [
        (
            "https://en.wikipedia.org/w/index.php?title=Norway_at_the_Olympics&oldid=1153387488",
            "Sailing",
            {
                "Gold": 17,
                "Silver": 11,
                "Bronze": 4,
            },
        ),
        (
            "https://en.wikipedia.org/w/index.php?title=Sweden_at_the_Olympics&oldid=1153383474",
            "Canoeing",
            {
                "Gold": 15,
                "Silver": 11,
                "Bronze": 4,
            },
        ),
        (
            "https://en.wikipedia.org/w/index.php?title=Denmark_at_the_Olympics&oldid=1163665180",
            "Cycling",
            {
                "Gold": 8,
                "Silver": 11,
                "Bronze": 10,
            },
        ),
    ],
)
def test_get_sport_stats(country_url, sport, expected):
    medals = get_sport_stats(country_url, sport)
    assert isinstance(medals, dict), f"Expected dictionary, but received {type(medals)}"
    assert medals == expected, "Dictionaries do not match"


@pytest.mark.task43
@pytest.mark.parametrize(
    "results, medal, expected",
    [
        (
            {
                "Norway": {"Gold": 2, "Silver": 2, "Bronze": 3},
                "Sweden": {"Gold": 1, "Silver": 2, "Bronze": 3},
                "Denmark": {"Gold": 1, "Silver": 2, "Bronze": 3},
            },
            "Gold",
            "Norway",
        ),
        (
            {
                "Norway": {"Gold": 2, "Silver": 2, "Bronze": 3},
                "Sweden": {"Gold": 1, "Silver": 5, "Bronze": 3},
                "Denmark": {"Gold": 1, "Silver": 2, "Bronze": 3},
            },
            "Silver",
            "Sweden",
        ),
        (
            {
                "Norway": {"Gold": 2, "Silver": 2, "Bronze": 1},
                "Sweden": {"Gold": 1, "Silver": 2, "Bronze": 3},
                "Denmark": {"Gold": 1, "Silver": 2, "Bronze": 3},
            },
            "Bronze",
            "Sweden/Denmark",
        ),
        (
            {
                "Norway": {"Gold": 2, "Silver": 2, "Bronze": 1},
                "Sweden": {"Gold": 2, "Silver": 1, "Bronze": 3},
                "Denmark": {"Gold": 2, "Silver": 2, "Bronze": 3},
            },
            "Gold",
            "None",
        ),
    ],
)
def test_find_best_country_in_sport(results, medal, expected):
    country = find_best_country_in_sport(results, medal)
    assert isinstance(country, str), f"Expected string, but received {type(country)}"
    if "/" in expected:
        assert "/" in expected
        # order-independent comparison using sets
        expected = set(expected.split("/"))
        country = set(country.split("/"))
    assert country == expected


@pytest.mark.task44
def test_report_scandi_stats(tmpdir):
    url = "https://en.wikipedia.org/w/index.php?title=All-time_Olympic_Games_medal_table&oldid=1165685442"
    summer_sports = [
        "Sailing",
        "Athletics",
        "Handball",
        "Football",
        "Cycling",
        "Archery",
    ]
    tmpdir.chdir()

    tmpdir = Path(tmpdir).absolute()
    report_scandi_stats(url, summer_sports, work_dir=tmpdir)
    dest_dir = tmpdir / "olympic_games_results"
    assert dest_dir.exists(), "Direcotry does not exist"
    print(list(dest_dir.iterdir()))
    assert (dest_dir / "Archery_medal_ranking.png").is_file()
    assert (dest_dir / "Athletics_medal_ranking.png").is_file()
    assert (dest_dir / "Cycling_medal_ranking.png").is_file()
    assert (dest_dir / "Football_medal_ranking.png").is_file()
    assert (dest_dir / "Handball_medal_ranking.png").is_file()
    assert (dest_dir / "Sailing_medal_ranking.png").is_file()
    assert (dest_dir / "total_medal_ranking.png").is_file()
    assert (dest_dir / "best_of_sport_by_Gold.md").is_file()
