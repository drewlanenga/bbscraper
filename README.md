bbsraper
========

# Getting Started

- Install MySQL.  If you prefer something else (MariaDB, Postgres, etc.), I don't think you'd have any schema problems, but this does utilize the `_mysql` package.
- Load the schema from `ncaa_bb.sql`.
- Install [`scrapy`](https://scrapy.org/).

# Scraping

There are a couple of scrapy spiders here.

| Scraper Name | Description |
| ------------ | ----------- |
| `espn_roster` | Get all rosters and players. |
| `espn` | Scrape boxscores. |
| `espn_playbyplay` | Scrape play-by-play data. |
| `espn_adhoc` | I honestly can't remember why I made it.  It was probably to fix something once. |

To scrape, run `scrapy crawl <spidername>`.

Each scraper has a hard coded season (year) and seasontype (1 = preseason, 2 = season, 3 = postseason).  If you want to scrape a different season, you have to currently change the year and rerun the scraper.


# Jankiness

This package makes a couple of assumptions, and at this point I'm too lazy to improve them.  (If you'd like to, PRs are welcome!)

- It assumes the existence of a database user with username `jackboot` and an empty password.
- Each spider has a starting URL, which currently point to NCAA resources (like http://espn.go.com/mens-college-basketball/teams).  To scrape NBA data, change URLs accordingly.

### Disclaimer

This scraper pulls data from espn.com &mdash; a site to which I have no affiliation, nor do I have any rights to its data.
