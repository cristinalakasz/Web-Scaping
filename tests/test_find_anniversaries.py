from pathlib import Path

import pandas as pd
import pytest
from find_anniversaries import (
    anniversary_list_to_df,
    anniversary_table,
    extract_anniversaries,
)

sample_HTML = """
<p></p>
<p>Nothing about a month here</p>
<p>October 3:</p>
<p><a href="/wiki/October_1" title="October 1">October 1</a></p>
<p><b><a href="/wiki/October_19" title="October 19">October 19</a></b></p>
<p>Text that should not be there<b><a href="/wiki/October_10" title="October 10">October 10</a></b></p>
<p><a href="October_29" title="October 29">October 29</a></p>
<table>
</table>
"""


@pytest.mark.task31
def test_extract_anniversaries():
    res = extract_anniversaries(sample_HTML, "October")
    sol = ["October 1", "October 19"]

    assert isinstance(res, list), f"Return type was {type(res)}, expected list"
    assert res != [], "Returned an empty list, but should not"
    assert isinstance(res[0], str), f"List contained {type[res[0]]}, expected string"
    assert len(res) == len(sol), "Wrong number of elements"
    assert res == sol


sample_list = [
    "May 19: The creator has birthday! ; Beautiful day\n",
    "December 1: just a beautiful day (always?); Winter is coming (No daylight past 15:00)",
    "November 2: ",
    "October 1",
    "June 3: Another beautiful day; hmmm, (1999)\n",
    "May 3: Just an exuse to put ugly character in test 35$56781-dg///c.*@",
]


@pytest.mark.task32
def test_anniversary_list_to_df():
    res_df = anniversary_list_to_df(sample_list)
    sol_list = [
        ["May 19", "The creator has birthday!"],
        ["May 19", "Beautiful day"],
        ["December 1", "just a beautiful day (always?)"],
        ["December 1", "Winter is coming (No daylight past 15:00)"],
        ["June 3", "Another beautiful day"],
        ["June 3", "hmmm, (1999)"],
        ["May 3", "Just an exuse to put ugly character in test 35$56781-dg///c.*@"],
    ]

    sol_df = pd.DataFrame(sol_list, columns=["Date", "Event"])
    assert isinstance(
        res_df, pd.DataFrame
    ), f"The return value was {type(res_df)}, expected pd.Dataframe"
    assert "Date" in res_df.columns, "Missing 'Date' column"
    assert "Event" in res_df.columns, "Missing 'Event' column"
    assert list(res_df["Date"]) == list(sol_df["Date"])
    assert list(res_df["Event"]) == list(sol_df["Event"])


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


@pytest.mark.task33
def test_anniversary_table(tmpdir):
    tmpdir.chdir()
    tmpdir = Path(tmpdir).absolute()

    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    anniversary_table(namespace_url, months_in_namespace, work_dir=tmpdir)
    dest_dir = tmpdir / "tables_of_anniversaries"
    assert dest_dir.exists(), f"Directory {dest_dir.name} does not exist"
    print(list(dest_dir.iterdir()))
    assert (dest_dir / "anniversaries_january.md").is_file()
    assert (dest_dir / "anniversaries_february.md").is_file()
    assert (dest_dir / "anniversaries_march.md").is_file()
    assert (dest_dir / "anniversaries_april.md").is_file()
    assert (dest_dir / "anniversaries_may.md").is_file()
    assert (dest_dir / "anniversaries_june.md").is_file()
    assert (dest_dir / "anniversaries_july.md").is_file()
    assert (dest_dir / "anniversaries_august.md").is_file()
    assert (dest_dir / "anniversaries_september.md").is_file()
    assert (dest_dir / "anniversaries_october.md").is_file()
    assert (dest_dir / "anniversaries_november.md").is_file()
    assert (dest_dir / "anniversaries_december.md").is_file()
