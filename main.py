import pandas as pd
import matplotlib.pyplot as plt

from src.billboard import extract_billboard_charts
from src.official_charts import extract_official_charts

if __name__ == '__main__':
    # df_billboard = extract_billboard_charts()
    # df_official_charts = extract_official_charts()
    #
    # df_final = pd.concat([df_billboard, df_official_charts], ignore_index=True)
    #
    # df_final.to_json('generated/charts.json', orient='records', indent=2)

    df = pd.read_json('generated/charts.json')

    bar_color = '#0000FF'
    pie_colors = ['#0000FF', '#FF00FF', '#5A64FF', '#A2609A', '#FF5449']
    line_colors = ['#0000FF', '#FF00FF', '#5A64FF', '#A2609A', '#FF5449']
    plt.figure(figsize=(10, 6))

    # Set up the plotting area
    fig, axs = plt.subplots(2, 2, figsize=(20, 25))

    # 1. Status Distribution
    df_status_dist = df['song_status'].value_counts()
    df_status_dist.plot(kind='pie', ax=axs[0, 0], title='Distribuição dos Status das Músicas', colors=pie_colors, autopct='%1.1f%%')

    # 2. Song Award Distribution
    df_award_dist = df['award'].value_counts()
    df_award_dist.plot(kind='pie', ax=axs[0, 1], title='Distribuição dos Prêmios das Músicas', colors=pie_colors, autopct='%1.1f%%')

    # 3. Top Artists by Number of Songs
    df_top_artists = df['artist_name'].value_counts().head(10)
    df_top_artists.plot(kind='bar', ax=axs[1, 0], title='Top 10 Artistas por Quantidade de Músicas', color=[bar_color]*10)
    axs[1, 0].set_xlabel('Nome do artista')
    axs[1, 0].set_ylabel('Quantidade de músicas')

    # 4. Trends in Song Status Over Weeks
    df_status_trend = df.groupby(['week_number', 'song_status']).size().unstack().fillna(0)
    df_status_trend.plot(kind='line', ax=axs[1, 1], title='Evolução dos Status das Músicas', color=line_colors)
    axs[1, 1].set_xlabel('Semana')
    axs[1, 1].set_ylabel('Quantidade de músicas')

    plt.tight_layout()
    plt.show()

    # Distribution of Songs by Week
    # df_week_dist = df.groupby(['chart_site', 'week_number']).size().unstack().transpose()
    # df_week_dist.plot(kind='bar', ax=axs[0, 0], title='Distribution of Songs by Week')
    # axs[0, 0].set_xlabel('Week Number')
    # axs[0, 0].set_ylabel('Number of Songs')

    # Peak Position Analysis
    # df['peak_pos'] = pd.to_numeric(df['peak_pos'], errors='coerce')
    # df_peak_pos = df['peak_pos'].dropna()
    # df_peak_pos.plot(kind='hist', bins=20, ax=axs[2, 0], title='Peak Position Analysis')
    # axs[2, 0].set_xlabel('Peak Position')
    # axs[2, 0].set_ylabel('Frequency')

    # Weeks on Chart Distribution
    # df['weeks_on_chart'] = pd.to_numeric(df['weeks_on_chart'], errors='coerce')
    # df_weeks_on_chart = df['weeks_on_chart'].dropna()
    # df_weeks_on_chart.plot(kind='hist', bins=20, ax=axs[2, 1], title='Weeks on Chart Distribution')
    # axs[2, 1].set_xlabel('Weeks on Chart')
    # axs[2, 1].set_ylabel('Frequency')

    # Comparison of Peak Positions by Chart Site
    # df_peak_by_site = df.dropna(subset=['peak_pos'])
    # df_peak_by_site.boxplot(column='peak_pos', by='chart_site', ax=axs[3, 0])
    # axs[3, 0].set_title('Comparison of Peak Positions by Chart Site')
    # axs[3, 0].set_xlabel('Chart Site')
    # axs[3, 0].set_ylabel('Peak Position')
    # plt.suptitle('')

    # Most Frequent Awards by Chart Site
    # df_awards_by_site = df.groupby(['chart_site', 'award']).size().unstack().fillna(0)
    # df_awards_by_site.plot(kind='bar', ax=axs[4, 0], title='Most Frequent Awards by Chart Site')
    # axs[4, 0].set_xlabel('Chart Site')
    # axs[4, 0].set_ylabel('Number of Awards')

    # Top Artists with Performance Gain
    # df_performance_gain = df[df['award'].str.contains('Performance Gain', na=False)]
    # df_top_perf_gain_artists = df_performance_gain['artist_name'].value_counts().head(10)
    # df_top_perf_gain_artists.plot(kind='bar', ax=axs[4, 1], title='Top Artists with Performance Gain')
    # axs[4, 1].set_xlabel('Artist Name')
    # axs[4, 1].set_ylabel('Number of Performance Gain Awards')
