# MLS data scraping

Scripts that collect Major League Soccer data for analysis and modeling:

| Script | What it pulls | Source |
| --- | --- | --- |
| `data_fetcher.py` | Match results + shooting stats per team, 2019–2024 | fbref.com |
| `get_match_stats.py` | Form guide / recent results | mlssoccer.com |
| `get_team_stats.py` | Club season stats | mlssoccer.com |
| `get_player_stats.py` | Player season stats | mlssoccer.com |
| `upcoming_matches.py` | Upcoming schedule | mlssoccer.com (Playwright) |
| `retrieve_logos.py` | Club logos | mlssoccer.com |

## Setup

```bash
pip install -r requirements.txt
playwright install chromium   # for upcoming_matches.py
```

The Selenium scripts need Chrome installed. Requests time out after 30s and the fbref scraper sleeps between pages to stay polite; please respect each site's terms and rate limits.
