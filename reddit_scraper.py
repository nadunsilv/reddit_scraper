import praw
import pandas as pd
from datetime import datetime, timezone
from typing import List, Dict, Generator
from concurrent.futures import ThreadPoolExecutor


class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def search_posts(self, query: str) -> Generator[Dict, None, None]:
        """Search for all past posts on Reddit mentioning the query."""
        for submission in self.reddit.subreddit('all').search(query, limit=None):
            post_data = self._extract_post_data(submission)
            yield post_data

    @staticmethod
    def _extract_post_data(submission) -> Dict:
        """Extract relevant data from a Reddit submission."""
        return {
            'title': submission.title,
            'subreddit': submission.subreddit.display_name,
            'subscribers': submission.subreddit.subscribers,
            'subreddit_type': submission.subreddit.subreddit_type,
            'comments': submission.num_comments,
            'url': submission.url,
            'text': submission.selftext,
            'author': str(submission.author),
            'created_utc': datetime.fromtimestamp(submission.created_utc, timezone.utc),
            'id': submission.id,
            # 'upvotes': submission.score
        }

    @staticmethod
    def calculate_score(post: Dict) -> float:
        """Calculate the score for a post based on upvotes and comments."""
        upvotes = post['upvotes']
        comments = post['comments']
        
        score = upvotes + (2 * comments)
        
        return score

    def export_to_csv(self, posts: List[Dict], filename: str) -> None:
        """Export the collected posts data to a CSV file."""
        df = pd.DataFrame(posts)
        df.to_csv(filename, index=False)

    def scrape_and_export(self, query: str, filename: str) -> None:
        """Scrape Reddit posts and export them to a CSV file."""
        posts = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for post in self.search_posts(query):
                futures.append(executor.submit(self._process_post, post))
            for future in futures:
                posts.append(future.result())
        
        self.export_to_csv(posts, filename)

    def _process_post(self, post: Dict) -> Dict:
        """Process a single post to calculate its score."""
        post['score'] = self.calculate_score(post)
        return post


def main():
    client_id='YOUR_CLIENT_ID'
    client_secret='YOUR_CLIENT_SECRET'
    user_agent='YOUR_USER_AGENT'

    scraper = RedditScraper(client_id, client_secret, user_agent)
    query = "hungarian paprika"
    filename = 'reddit_posts.csv'

    scraper.scrape_and_export(query, filename)


if __name__ == "__main__":
    main()
