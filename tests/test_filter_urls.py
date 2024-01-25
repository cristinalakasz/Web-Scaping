import warnings

import pytest
from filter_urls import find_articles, find_img_src, find_urls
from requesting_urls import get_html

# Test some random urls


@pytest.mark.task12
def test_find_urls():
    html = """
    <a href="#fragment-only">anchor link</a>
    <a id="some-id" href="/relative/path#fragment">relative link</a>
    <a href="//other.host/same-protocol">same-protocol link</a>
    <a href="https://example.com">absolute URL</a>
    """
    urls = find_urls(html, base_url="https://en.wikipedia.org")
    assert urls == {
        "https://en.wikipedia.org/relative/path",
        "https://other.host/same-protocol",
        "https://example.com",
    }


@pytest.mark.task12
@pytest.mark.parametrize(
    "url, links",
    [
        ("https://en.wikipedia.org/wiki/Nobel_Prize", ["x"]),
        ("https://en.wikipedia.org/wiki/Bundesliga", ["x"]),
        (
            "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup",
            ["x"],
        ),
    ],
)
def test_find_urls_pages(url, links):
    html = get_html(url)
    urls = find_urls(html)
    assert isinstance(urls, set)
    # print(urls)
    for url in urls:
        # make sure we've got full URLs
        assert not url.startswith("/")
        assert not url.startswith("#")
        assert " " not in url
        assert "://" in url
    # for link in links:
    #     assert link in urls


@pytest.mark.task13
@pytest.mark.parametrize(
    "url, expected",
    [
        (
            "https://en.wikipedia.org/wiki/Nobel_Prize",
            [
                "https://en.wikipedia.org/wiki/Nobel_Peace_Prize",
                "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country",
                "https://en.wikipedia.org/wiki/Ir%C3%A8ne_Joliot-Curie",
            ],
        ),
        (
            "https://en.wikipedia.org/wiki/Bundesliga",
            [
                "https://en.wikipedia.org/wiki/UEFA",
                "https://en.wikipedia.org/wiki/1963%E2%80%9364_Bundesliga",
                "https://en.wikipedia.org/wiki/List_of_football_clubs_in_Germany",
            ],
        ),
        (
            "https://en.wikipedia.org/wiki/2019%E2%80%9320_FIS_Alpine_Ski_World_Cup",
            [
                "https://en.wikipedia.org/wiki/Norway",
                "https://en.wikipedia.org/wiki/1970%E2%80%9371_FIS_Alpine_Ski_World_Cup",
            ],
        ),
    ],
)
def test_find_articles(url, expected):
    html = get_html(url)
    articles = find_articles(html)
    assert isinstance(articles, set)
    # TODO: more precise measure
    assert len(articles) > 10
    for article in articles:
        assert "://" in article
        proto, _, rest = article.partition("://")
        hostname, _, path = rest.partition("/")
        assert hostname.endswith("wikipedia.org"), f"Not a wikipedia link: {article}"
        assert path.startswith("wiki/"), f"Not a wikipedia article: {article}"
        _, after_wiki = path.split("/", 1)
        if ":" in after_wiki:
            # has a colon, likely a special page that should have been excluded
            # only check for known-bad prefixes
            category, rest = after_wiki.split(":", 1)
            assert category not in {
                "Special",
                "Wikipedia",
                "Help",
                "File",
                "Category",
                "Template",
                "Template_talk",
                "Talk",
            }, f"Got special page, not article: {article}"

            warnings.warn(f"Likely special page: {article}")
    import pprint

    pprint.pprint(articles)
    for article in expected:
        assert article in articles

    # check expected articles are present
    # for article in expected:
    #     assert article in articles


def test_find_img_src():
    html = """
    <img src="https://some.jpg">
    <img title="abc" src="/foo.png">
    <img nosrc>
    """
    src_set = find_img_src(html)
    assert src_set == {
        "https://some.jpg",
        "/foo.png",
    }
