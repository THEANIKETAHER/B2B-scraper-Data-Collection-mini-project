import asyncio
import aiohttp
import async_timeout
import random
import logging
from urllib.parse import urljoin
from crawler.user_agents import USER_AGENTS
from crawler.utils import async_sleep_jitter, exponential_backoff_retry_delay, is_allowed_by_robots
from crawler.parsers import parse_indiamart_listing_list, parse_indiamart_product
import json, os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncCrawler:
    def __init__(self, concurrency=3, timeout=15, max_retries=3):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout = timeout
        self.max_retries = max_retries

    async def fetch(self, session, url, headers=None, attempt=1):
        try:
            async with self.semaphore:
                async with async_timeout.timeout(self.timeout):
                    async with session.get(url, headers=headers) as resp:
                        if resp.status != 200:
                            raise Exception(f"HTTP {resp.status}")
                        return await resp.text()
        except Exception as e:
            if attempt <= self.max_retries:
                delay = exponential_backoff_retry_delay(attempt)
                logger.info(f"Retry {attempt} for {url} after {delay:.1f}s due to {e}")
                await asyncio.sleep(delay)
                return await self.fetch(session, url, headers=headers, attempt=attempt+1)
            logger.error(f"Failed to fetch {url}: {e}")
            return None

    async def crawl_listing(self, start_url):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, start_url, headers=headers)
            if not html:
                return []
            product_urls = parse_indiamart_listing_list(html)
            return [urljoin(start_url, u) for u in product_urls]

    async def crawl_products(self, product_urls, output_file="sample_output/products.jsonl"):
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        os.makedirs("sample_output", exist_ok=True)
        async with aiohttp.ClientSession() as session:
            for url in product_urls:
                html = await self.fetch(session, url, headers=headers)
                if not html:
                    continue
                record = parse_indiamart_product(html, url)
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                logger.info(f"Saved: {record.get('title')}")
                await async_sleep_jitter(1, 3)

async def run_example():
    start_url = "https://dir.indiamart.com/search.mp?ss=soldering+iron&prdsrc=1&v=4&mcatid=&catid=&crs=xnh-city&trc=xium&cq=Thane&tags=res:RC3|ktp:N0|stype:attr=1|mtp:S|wc:2|lcf:3|cq:thane|qr_nm:gl-gd|cs:17870|com-cf:nl|ptrs:na|mc:19308|cat:846|qry_typ:P|lang:en|tyr:2|qrd:251021|mrd:251001|prdt:251023|msf:ms|pfen:1|gli:G1I2|gc:Mumbai|ic:Pune|scw:1"
    crawler = AsyncCrawler(concurrency=3)
    product_urls = await crawler.crawl_listing(start_url)
    await crawler.crawl_products(product_urls)

if __name__ == "__main__":
    asyncio.run(run_example())

