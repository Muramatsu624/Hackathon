import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from evaluate import *

#webサイトを取得し、テキスト形式で出力
def load(url):
    res = requests.get(url)
    #HTTPリクエストが失敗したステータスコードを返した場合、HTTPErrorを送出
    res.raise_for_status()
    #レスポンスボディをテキスト形式で入手
    return res.text

#htmlタグの取得
def get_tag(html, find_tag):
    soup = BeautifulSoup(str(html), 'html.parser')
    tag = soup.find(find_tag)
    return tag

#htmlタグの取得
def get_tags(html, find_tag):
    soup = BeautifulSoup(str(html), 'html.parser')
    tag = soup.find_all(find_tag)
    return tag

#htmlのid取得
def get_id(html, find_id):
    soup = BeautifulSoup(str(html), 'html.parser')
    html_id = soup.select(find_id)
    return html_id

#プログラムで扱えるデータ構造に変換
def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    #htmlタグの削除
    simple_row = soup.getText()
    simple_row = simple_row.replace('　', '')    
    return simple_row

def parse_lyric(html):
    soup = BeautifulSoup(html, 'html.parser')
    #htmlタグの削除
    simple_row = soup.get_text(separator=" ").strip()
    simple_row = simple_row.replace('　', ' ')

    return simple_row

#それぞれ歌の情報の取得
def get_info(url):
    base_url = 'https://www.uta-net.com/'
    html = load(url)
    #曲ごとのurlを格納
    song_url = []
    #歌を格納
    song_info = []
    songs_info=[]

    #曲のurlを取得
    #tdのurlを格納
    for td in get_tags(html, 'td'):
        #a要素の取得
        for a in get_tags(td, 'a'):
            #href属性にsongを含むか否か
            if 'song' in a.get ('href'):
                #urlを配列に追加
                song_url.append(base_url + a.get('href'))

    #曲の情報の取得
    two_song = []
    for i, page in enumerate(song_url):
        print('{}曲目:{}'.format(i + 1, page))
        html = load(page)
        song_info = []

        #Song
        for tag in get_tag(html, 'h2'):
            #id検索を行うため、一度strにキャスト
            tag = str(tag)
            simple_row = parse(tag)
            song_info.append(simple_row)                

        #Artist
        for tag in get_tags(html, 'h3'):
            tag = str(tag)
            if r'itemprop="byArtist name"' in tag:
                simple_row = parse(tag)
                song_info.append(simple_row)

        #Lyricist
        for tag in get_tags(html, 'a'):
            tag = str(tag)
            if r'itemprop="lyricist"' in tag:
                simple_row = parse(tag)
                song_info.append(simple_row)

        #Composer
        for tag in get_tags(html, 'a'):
            tag = str(tag)
            if r'itemprop="composer"' in tag:
                simple_row = parse(tag)
                song_info.append(simple_row)

        #Lyric
        for id_ in get_id(html, '#kashi_area'):
            id_ = str(id_)
            if r'id="kashi_area"' in id_:
                simple_row = parse_lyric(id_)
                #これが歌詞部分
                print(simple_row)
                if(len(two_song) < 2):
                    two_song.append(simple_row)
                    print(len(two_song))
                # # 全て文字化けしてtxt-fileに出力される
                txt_file = "test.txt"
                with open (txt_file, 'a') as f:
                    f.write(str(i+1) + "曲目")
                    f.write(simple_row)
                song_info.append(simple_row)
                songs_info.append(song_info)

                #1秒待機(サーバの負荷を軽減)
                time.sleep(1)
                break
        
    # 得点出力テスト
    theme = "悲しい"
    evaluate(two_song[0], two_song[1], theme)

    return songs_info

def create_df(file_name, url):
    # データフレームを作成
    #df = pd.DataFrame('Song_Title', 'Artist', 'Lyricist', 'Composer', 'Lyric')
    df = pd.DataFrame(get_info(url))
    df = df.rename(columns={0:'Song_Title', 1:'Artist', 2:'Lyricist', 3:'Composer', 4:'Lyric'})
    # print(df['Lyric'].iat[13])
    # # # 全て文字化けしてtxt-fileに出力される
    # txt_file = "test2.txt"
    # with open (txt_file, 'a') as f:
    #     f.write(df['Lyric'].iat[13])
    # CSVファイル出力
    # csv = df.to_csv("csv/{}.csv".format(file_name))
    # return csv


file_name = 'sample'
url = 'https://www.uta-net.com/artist/26099/'
#url = 'https://www.uta-net.com/user/ranking/daily.html'
#url = 'https://www.uta-net.com/user/ranking/monthly.html'
create_df(file_name, url)
