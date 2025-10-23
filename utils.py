import asyncio
import random
import requests
from urllib.parse import urljoin, urlparse
from robotexclusionrulesparser import RobotExclusionRulesParser

async def async_sleep_jitter(min_s=0.5, max_s=2.5):
    await asyncio.sleep(random.uniform(min_s, max_s))

def is_allowed_by_robots(url, user_agent="*"):
    """Check if scraping is allowed by robots.txt"""
    parsed = urlparse(url)
    robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
    try:
        r = requests.get(robots_url, timeout=5)
        parser = RobotExclusionRulesParser()
        parser.parse(r.text)
        return parser.is_allowed(user_agent, url)
    except:
        return True  # if robots.txt fails, assume allowed (still be polite)

def exponential_backoff_retry_delay(attempt):
    return min(60, (2 ** attempt) + random.random())

