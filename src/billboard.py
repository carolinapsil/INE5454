import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.models.chart_row import ChartRow
from src.utils.scraping_parse_utils import parse_song_status, parse_song_award


def extract_charts():
    page_url = 'https://www.billboard.com/charts/hot-100/'

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(page_url)

    chart_rows = driver.find_elements(By.CLASS_NAME, 'o-chart-results-list-row')

    charts = []
    for chart_row in chart_rows:
        pos = chart_row.find_element(By.XPATH, './li[1]/span').text
        artist_photo_url = chart_row.find_element(By.XPATH, './li[2]/div/div/img').get_attribute('src')

        song_status_li = chart_row.find_element(By.XPATH, './li[3]')
        try:
            song_status = parse_song_status(song_status_li.find_element(By.TAG_NAME, 'g').get_attribute('data-name'))
        except NoSuchElementException:
            song_status = parse_song_status(song_status_li.find_element(By.TAG_NAME, 'span').text)

        song_name = chart_row.find_element(By.XPATH, './li[4]/ul/li[1]/h3').text
        artist_name = chart_row.find_element(By.XPATH, './li[4]/ul/li[1]/span').text

        song_status_li = chart_row.find_element(By.XPATH, './li[4]/ul/li[3]')
        try:
            award = parse_song_award(song_status_li.find_element(By.TAG_NAME, 'g').get_attribute('data-name'))
        except NoSuchElementException:
            try:
                award = parse_song_award(song_status_li.find_element(By.TAG_NAME, 'path').get_attribute('data-name'))
            except NoSuchElementException:
                award = parse_song_award('')

        last_week = chart_row.find_element(By.XPATH, './li[4]/ul/li[4]/span').text
        peak_pos = chart_row.find_element(By.XPATH, './li[4]/ul/li[5]/span').text
        weeks_on_chart = chart_row.find_element(By.XPATH, './li[4]/ul/li[6]/span').text

        charts.append(
            ChartRow(pos, artist_photo_url, song_status, song_name, artist_name, award, last_week, peak_pos, weeks_on_chart, page_url).to_dict()
        )

    df = pd.DataFrame(charts)
    df.to_json('generated/charts.json', orient='records', indent=2)

    driver.quit()
