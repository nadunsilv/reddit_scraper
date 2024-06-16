# Reddit Scraper for "Hungarian Paprika" Mentions

This script scrapes Reddit for all past posts mentioning "hungarian paprika" and exports the data to a CSV file.

## Requirements

- Python 3.x
- PRAW (Python Reddit API Wrapper)
- Pandas

## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:nadunsilv/reddit_scraper.git
    cd reddit_scraper
    ```

2. Install the required packages:
    ```bash
    pip install praw pandas
    ```

3. Set up your Reddit API credentials in the script:
    ```python
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    user_agent = 'YOUR_USER_AGENT'
    ```

## Usage

Run the script:
```bash
python reddit_scraper.py
