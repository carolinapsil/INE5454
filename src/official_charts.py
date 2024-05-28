import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.models.chart_row import ChartRow
from src.utils.scraping_parse_utils import parse_song_status_uk


def extract_official_charts():
    official_page_url = 'https://www.officialcharts.com/charts/singles-chart/'

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(official_page_url)

    charts = []

    chart_rows = driver.find_element(By.CLASS_NAME, 'chart-items')

    for i in range(0, 100):
        chart_row = chart_rows.find_element(By.XPATH, f'./div[contains(@data-item, "item-437233-{i}")]')

        pos = chart_row.find_element(By.XPATH, './div[1]/div[1]/span/strong').text
        artist_photo_url = chart_row.find_element(By.XPATH, "./div[1]/div[1]/div/img[1]").get_attribute('src')

        song_status_span = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[1]/span[1]')

        song_status_class = song_status_span.get_attribute('class').split(' ')

        if len(song_status_class) > 1:
            song_status = song_status_class[1]
            if song_status == 'text-brand-pink':
                song_status = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[1]/span[1]').text
        else:
            song_status = song_status_class[0]

        song_status = parse_song_status_uk(song_status)

        song_name = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[1]/span[2]').text

        artist_name = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[2]/span').text

        last_week = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[1]/span/span').text
        peak_pos = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[2]/span[1]').text
        weeks_on_chart = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[3]/span').text

        award = 'null'
        charts.append(
            ChartRow('official_charts', 0, pos, artist_photo_url, song_status, song_name, artist_name, award, last_week,
                     peak_pos,
                     weeks_on_chart,
                     official_page_url).to_dict()
        )

    df = pd.DataFrame(charts)
    df.to_json('generated/charts_uk.json', orient='records', indent=2)