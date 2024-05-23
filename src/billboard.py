from datetime import datetime, timedelta
from functools import reduce

import pandas as pd
from pandas import DataFrame
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src.models.chart_row import ChartRow
from src.utils.scraping_parse_utils import parse_song_status, parse_song_award


def extract_from_billboard():
    billboard_hot100_url = 'https://www.billboard.com/charts/hot-100'
    today = datetime.now()

    week_1 = today.strftime('%Y-%m-%d')
    week_2 = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    week_3 = (today - timedelta(days=14)).strftime('%Y-%m-%d')
    week_4 = (today - timedelta(days=21)).strftime('%Y-%m-%d')
    week_5 = (today - timedelta(days=28)).strftime('%Y-%m-%d')

    df_week_1 = extract_charts(page_url=f'{billboard_hot100_url}/{week_1}', week_number=1)
    df_week_2 = extract_charts(page_url=f'{billboard_hot100_url}/{week_2}', week_number=2)
    df_week_3 = extract_charts(page_url=f'{billboard_hot100_url}/{week_3}', week_number=3)
    df_week_4 = extract_charts(page_url=f'{billboard_hot100_url}/{week_4}', week_number=4)
    df_week_5 = extract_charts(page_url=f'{billboard_hot100_url}/{week_5}', week_number=5)

    df_final = pd.concat([df_week_1, df_week_2, df_week_3, df_week_4, df_week_5], ignore_index=True)

    df_final.to_json('generated/charts.json', orient='records', indent=2)


def extract_charts(page_url, week_number) -> DataFrame:
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
            ChartRow('billboard', week_number, pos, artist_photo_url, song_status, song_name, artist_name, award,
                     last_week, peak_pos, weeks_on_chart, page_url).to_dict()
        )

    return pd.DataFrame(charts)
