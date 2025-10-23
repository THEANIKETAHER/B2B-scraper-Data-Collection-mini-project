from bs4 import BeautifulSoup
import re
from datetime import datetime

def parse_indiamart_listing_list(html):
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href")
        if not href:
            continue
        href = href.strip()
        # Skip irrelevant or app links
        if any(x in href for x in ["itunes.apple", "play.google", "youtube", "facebook", "twitter", "linkedin"]):
            continue
        if "product" in href or "supplier" in href or "proddetail" in href:
            links.append(href)
    return list(dict.fromkeys(links))

def parse_indiamart_product(html, url):
    soup = BeautifulSoup(html, "lxml")

    def text(sel):
        el = soup.select_one(sel)
        return el.get_text(strip=True) if el else None

    title = text("h1") or text(".product-title")
    price_raw = text(".price") or text(".prd-price")
    price_min, price_max, currency = None, None, None
    if price_raw:
        nums = re.findall(r'[\d,.]+', price_raw)
        if nums:
            price_min = float(nums[0].replace(",", ""))
            if len(nums) > 1:
                price_max = float(nums[1].replace(",", ""))
        if "₹" in price_raw or "INR" in price_raw:
            currency = "INR"

    seller_name = text(".supplier-name") or text(".seller-name")
    location = text(".location") or text(".seller-location")
    description = text(".description") or text("#description")

    images = [img["src"] for img in soup.select("img") if "http" in img.get("src", "")]
    return {
        "source": "indiamart",
        "scrape_date": datetime.utcnow().isoformat(),
        "title": title,
        "description": description,
        "price_min": price_min,
        "price_max": price_max,
        "price_currency": currency,
        "seller_name": seller_name,
        "location": location,
        "product_url": url,
        "image_urls": images
    }

