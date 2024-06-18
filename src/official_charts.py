from datetime import datetime, timedelta

import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.models.chart_row import ChartRow
from src.utils.scraping_parse_utils import parse_song_status_uk


def extract_official_charts() -> DataFrame:
    official_page_url = 'https://www.officialcharts.com/charts/singles-chart/'
    today = datetime.now()

    week_2 = (today - timedelta(days=7)).strftime('%Y%m%d')
    week_3 = (today - timedelta(days=14)).strftime('%Y%m%d')
    week_4 = (today - timedelta(days=21)).strftime('%Y%m%d')
    week_5 = (today - timedelta(days=28)).strftime('%Y%m%d')

    df_week_1 = extract_charts(page_url=official_page_url, week_number=1)
    df_week_2 = extract_charts(page_url=f'{official_page_url}/{week_2}/7501/', week_number=2)
    df_week_3 = extract_charts(page_url=f'{official_page_url}/{week_3}/7501/', week_number=3)
    df_week_4 = extract_charts(page_url=f'{official_page_url}/{week_4}/7501/', week_number=4)
    df_week_5 = extract_charts(page_url=f'{official_page_url}/{week_5}/7501/', week_number=5)

    return pd.concat([df_week_1, df_week_2, df_week_3, df_week_4, df_week_5], ignore_index=True)


def extract_charts(page_url, week_number) -> DataFrame:

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(page_url)

    chart_rows = driver.find_elements(By.CLASS_NAME, 'chart-item')
    for chart_row in chart_rows:
        row_classes = chart_row.get_attribute('class')
        if 'chart-ad' in row_classes:
            chart_rows.remove(chart_row)

    charts = []
    for chart_row in chart_rows:
        pos = chart_row.find_element(By.XPATH, './div[1]/div[1]/span/strong').text
        artist_photo_url = chart_row.find_element(By.XPATH, "./div[1]/div[1]/div/img[1]").get_attribute('src')

        song_status_span = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[1]/span[1]')
        song_status_classes = song_status_span.get_attribute('class')

        song_status = parse_song_status_uk(song_status_classes)

        song_name = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[1]/span[2]').text
        artist_name = chart_row.find_element(By.XPATH, './div[1]/div[2]/p/a[2]/span').text
        last_week = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[1]/span/span').text
        peak_pos = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[2]/span[1]').text
        weeks_on_chart = chart_row.find_element(By.XPATH, './div[1]/div[2]/div/ol/li[3]/span').text

        award = 'null'
        charts.append(
            ChartRow('official_charts', week_number, pos, artist_photo_url, song_status, song_name, artist_name, award, last_week,
                     peak_pos,
                     weeks_on_chart,
                     page_url).to_dict()
        )

    return pd.DataFrame(charts)
