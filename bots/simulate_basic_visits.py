#!/usr/bin/env python3
# simulate_basic_visits.py
import requests, random, time, string, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

BASE = "http://aidrupalinsights.ericvinicius.com.br"
PAGES = [
    "/", "/admissions", "/programs", "/apply", "/our-campus", "/donate",
    "/digital-media-design-ba", "/business-administration-bba",
    "/computer-science-bsc", "/environmental-studies-ba", "/nursing-bscn"
]

SEARCH_PATH = "/search/node?keys="

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
]

def random_string(n=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def visit_page(session, path):
    url = BASE + path
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        r = session.get(url, headers=headers, timeout=10)
        logging.info("GET %s -> %s", url, r.status_code)
    except Exception as e:
        logging.warning("Error GET %s : %s", url, e)

def simulate_search(session, term):
    url = BASE + SEARCH_PATH + requests.utils.quote(term)
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        r = session.get(url, headers=headers, timeout=10)
        logging.info("SEARCH %s -> %s (len=%d)", term, r.status_code, len(r.text))
    except Exception as e:
        logging.warning("Error SEARCH %s : %s", term, e)

def main():
    session = requests.Session()
    rounds = 10
    for i in range(rounds):
        # pick behavior: browse pages or search
        if random.random() < 0.7:
            # sequence of page visits to simulate a session
            pages_count = random.randint(1, 4)
            for _ in range(pages_count):
                path = random.choice(PAGES)
                visit_page(session, path)
                # short delay between navigation
                time.sleep(random.uniform(1.0, 4.0))
        else:
            # simulate search: sometimes a real term, sometimes random (0 results)
            if random.random() < 0.6:
                term = random.choice(["Nursing", "computer", "design", "business"])
            else:
                term = random_string(12)  # likely zero-result
            simulate_search(session, term)
            time.sleep(random.uniform(1.0, 3.0))

        # inter-session pause
        time.sleep(random.uniform(2.0, 6.0))

if __name__ == "__main__":
    main()
