#!/usr/bin/env python3
# simulate_realistic_sessions.py
import time, random, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIGURAÇÃO ==========
BASE = "http://aidrupalinsights.ericvinicius.com.br"
PAGES = [
    "/", "/admissions", "/programs", "/apply", "/our-campus", "/donate",
    "/digital-media-design-ba", "/business-administration-bba",
    "/computer-science-bsc", "/environmental-studies-ba", "/nursing-bscn"
]
SEARCH_URL = BASE + "/search/node?keys="

# 👇 Novas rotas inexistentes (para simular páginas 404)
BROKEN_PATHS = [
    "/random-page-xyz", "/about-us-404", "/faculty/dr-john-snowe",
    "/academics/businessx", "/undefined-path", "/page-not-exist"
]

# Configuração de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# ========== FUNÇÕES DE APOIO ==========

def human_sleep(a=2.0, b=6.0):
    """Espera aleatória simulando comportamento humano."""
    time.sleep(random.uniform(a, b))

def scroll_page(driver):
    """Faz rolagem gradual da página, simulando leitura."""
    total_height = driver.execute_script("return document.body.scrollHeight")
    viewport = driver.execute_script("return window.innerHeight")
    pos = 0
    while pos < total_height:
        step = random.randint(int(viewport * 0.2), int(viewport * 0.8))
        pos += step
        driver.execute_script(f"window.scrollTo(0, {pos});")
        human_sleep(0.8, 2.5)
        if random.random() < 0.05:
            driver.execute_script(f"window.scrollBy(0, -{int(step * 0.5)});")
            human_sleep(0.5, 1.2)
    if random.random() < 0.3:
        driver.execute_script("window.scrollTo(0, 0);")
        human_sleep(0.5, 1.0)

def do_search(driver, term):
    """Executa busca simulada."""
    driver.get(SEARCH_URL + term)
    logging.info("Performing search: %s", term)
    human_sleep(1.5, 3.0)
    scroll_page(driver)

    if "Your search yielded no results" in driver.page_source:
        logging.info("❌ Search with zero results detected for term '%s'", term)
        js = """
        if (typeof gtag === 'function') {
          gtag('event', 'search_no_results', {
            search_term: arguments[0],
            event_label: 'Zero Results Detected'
          });
        }
        """
        driver.execute_script(js, term)
    else:
        logging.info("✅ Search returned results for term '%s'", term)
        js = """
        if (typeof gtag === 'function') {
          gtag('event', 'search_with_results', {
            search_term: arguments[0],
            event_label: 'Results Found'
          });
        }
        """
        driver.execute_script(js, term)

def click_some_program(driver):
    """Tenta clicar em um link de programa se existir."""
    try:
        el = driver.find_element(
            By.CSS_SELECTOR,
            "a[href*='-ba'], a[href*='-bsc'], a[href*='-bscn'], a[href*='-bba']"
        )
        href = el.get_attribute("href")
        logging.info("Click program link %s", href)
        el.click()
        human_sleep(2.0, 6.0)
        scroll_page(driver)
    except Exception as e:
        logging.debug("No program link clicked: %s", e)

def visit_404_page(driver):
    """Acessa uma página inexistente (simula erro 404)."""
    broken = random.choice(BROKEN_PATHS)
    logging.info("Visiting 404 page: %s", broken)
    driver.get(BASE + broken)
    human_sleep(1.5, 3.0)
    scroll_page(driver)
    if "Page not found" in driver.page_source or driver.title.startswith("Page not found"):
        js = """
        if (typeof gtag === 'function') {
          gtag('event', 'page_not_found', {
            page_path: arguments[0],
            event_label: '404 Page Accessed'
          });
        }
        """
        driver.execute_script(js, broken)
        logging.info("🚫 Triggered GA4 event: page_not_found for %s", broken)

def simulate_session(driver):
    """Executa uma sessão de navegação realista."""
    landing = random.choice(PAGES)
    logging.info("Session landing on %s", landing)
    driver.get(BASE + landing)
    human_sleep(1.5, 4.0)
    scroll_page(driver)

    # Navega, busca ou acessa 404 aleatoriamente
    for _ in range(random.randint(2, 5)):
        roll = random.random()
        if roll < 0.6:
            path = random.choice(PAGES)
            driver.get(BASE + path)
            human_sleep(1.0, 3.0)
            scroll_page(driver)
            if random.random() < 0.3:
                click_some_program(driver)
        elif roll < 0.85:
            term = (
                random.choice(["Nursing", "computer", "design", "business", "environment"])
                if random.random() < 0.7
                else ''.join(random.choices("zxqwjplk", k=10))
            )
            do_search(driver, term)
        else:
            visit_404_page(driver)
        human_sleep(2.0, 8.0)

# ========== FUNÇÃO PRINCIPAL ==========

def main():
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        sessions = 10
        for i in range(sessions):
            logging.info("Starting session %d/%d", i + 1, sessions)
            simulate_session(driver)
            time.sleep(random.uniform(5, 30))
    finally:
        driver.quit()

# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    main()
