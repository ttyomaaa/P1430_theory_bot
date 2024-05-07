import pandas as pd
import seaborn as snus
import io
from app.get_data_service import get_results, get_results_by_chapter
import matplotlib.ticker as ticker

buf = io.BytesIO()


async def get_stats(id_chapter=None, mode=0):
    if id_chapter:
        results = await get_results_by_chapter(id_chapter)
    else:
        results = await get_results()
    df = pd.DataFrame(results)
    max_q = list(zip([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                     [7, 10, 7, 5, 7, 13, 7, 10, 5, 8, 14, 8]))

    df['result'] = df['result'].astype(float)
    pd.to_datetime(df['created_date'])

    for idx, series in df.iterrows():
        for chapter_n, maximum in max_q:
            if chapter_n == int(df.at[idx, 'id_chapter']):
                df.at[idx, 'result'] /= maximum
                df.at[idx, 'result'] *= 10
    if mode == 0:
        get_bar(df)
    else:
        get_line(df)
    return


def get_line(df):
    data = df[['result', 'id_chapter', 'created_date']]
    line = snus.lineplot(x='created_date', y='result', hue='id_chapter', palette='hls', data=data)
    line.xaxis.set_major_locator(ticker.LinearLocator(3))
    line.set(xlabel='Время', ylabel='Средний результат (из 10)')
    line.set(ylim=(0, 10))
    fig = line.get_figure()
    fig.savefig(buf, format='png')
    return


def get_bar(df):
    df = df.sort_values(by=['id_chapter'], ascending=True)
    data = df[['result', 'id_chapter']].groupby('id_chapter').mean()
    bar = snus.barplot(x='id_chapter', y='result', palette='hls', data=data)
    bar.set(xlabel='Глава', ylabel='Результат (из 10)')
    bar.set(ylim=(0, 10))
    fig1 = bar.get_figure()
    fig1.savefig(buf, format='png')
    return
