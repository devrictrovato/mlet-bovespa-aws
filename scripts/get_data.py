from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


# 1. Selenium: obtém o HTML da tabela IBOV com todas as linhas
def get_html_with_selenium(url, show=False):
    chrome_options = Options()
    if not show:
        chrome_options.add_argument("--headless=new")  # descomente se quiser rodar sem interface
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Aguarda a tabela carregar
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )

        # Clica para mostrar todas as 120 linhas
        select = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, 'selectPage'))
        )
        select.click()
        time.sleep(1)

        # Seleciona a opção 120
        opt_120 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="selectPage"]/option[text()="120"]'))
        )
        opt_120.click()

        # Aguarda recarregamento
        time.sleep(5)

        html = driver.page_source
        return html

    finally:
        driver.quit()


# 2. BeautifulSoup: extrai cabeçalho + linhas
def parse_table_with_bs4(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if not table:
        raise ValueError("Tabela não encontrada")

    # Header
    headers = [th.get_text(strip=True) for th in table.find_all('th')]

    # Linhas (dados)
    rows_data = []
    for tr in table.find_all('tr'):
        tds = tr.find_all('td')
        if tds:
            row = [td.get_text(strip=True) for td in tds]
            rows_data.append(row)

    return headers, rows_data
