"""
Chat GPTでコード生成

質問内容：
以下の条件を満たす100行以内のPythonのコードを教えてもらえないでしょうか？
・指定した範囲にデータが無い日があった場合は自動で処理をスキップする。
・指定した範囲の各日付ごとに日本株全銘柄について各株ごとに、銘柄コード、企業名、始値、当日高値、当日安値、終値、出来高（1000株単位）を取得する。
・取得したデータについて、各日付ごとにテキストファイルに出力する。

回答内容：
以下が指定された条件を満たすPythonコードです。

※注意※

このコードを実行するには、BeautifulSoup4、pandas、requests、osのライブラリが必要です。
株価データを取得するためにYahoo!ファイナンスから情報を取得します。Yahoo!ファイナンスから情報を取得するには、使用される検索条件に応じて、
スクレイピングが禁止されている場合があります。したがって、このコードを実行する前に、Yahoo!ファイナンスの利用規約を確認してください。

上記コードを実行すると、指定された期間内にデータが存在する各日について、日本株の全銘柄について、銘柄コード、企業名、始値、当日高値、当日安値、終値、
出来高を取得し、指定された日付ごとにテキストファイルに出力します。また、指定された期間内にデータが存在しない日があった場合は、自動的にその日の処理を
スキップします。

"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

start_date = '2022-01-01'
end_date = '2022-01-03'

date_range = pd.date_range(start=start_date, end=end_date, freq='D')

for date in date_range:
    date_str = date.strftime('%Y%m%d')
    url = f'https://info.finance.yahoo.co.jp/ranking/?kd=1&tm=d&mk=1&tmn=on&thm=on&dit=on&tc={date_str}&ct=s'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.select('.rankingTable .stocksTable tr')

    if not rows:
        continue

    data = []
    for row in rows[1:]:
        tds = row.select('td')
        code = tds[0].text.strip()
        name = tds[1].text.strip()
        open_price = tds[2].text.strip().replace(',', '')
        high_price = tds[3].text.strip().replace(',', '')
        low_price = tds[4].text.strip().replace(',', '')
        close_price = tds[5].text.strip().replace(',', '')
        volume = tds[6].text.strip().replace(',', '')
        data.append([code, name, open_price, high_price, low_price, close_price, volume])

    df = pd.DataFrame(data, columns=['銘柄コード', '企業名', '始値', '当日高値', '当日安値', '終値', '出来高'])
    df.to_csv(f'{date_str}.txt', sep='\t', index=False)

print('Done.')

