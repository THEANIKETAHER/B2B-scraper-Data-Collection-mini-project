import re
from datetime import datetime

def clean_record(rec):
    rec["title"] = (rec.get("title") or "").strip()
    rec["price_min"] = parse_price(rec.get("price_min"))
    rec["price_max"] = parse_price(rec.get("price_max"))
    rec["scrape_date"] = rec.get("scrape_date") or datetime.utcnow().isoformat()
    return rec

def parse_price(value):
    if value is None:
        return None
    try:
        return float(value)
    except:
        s = str(value)
        m = re.findall(r'[\d,.]+', s)
        return float(m[0].replace(",", "")) if m else None

