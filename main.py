import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options


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






#歌手の名前から歌手のurlがまとまった辞書を返す関数
def artist_searcher(artist_name):

    #ヘッドレスモード
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.uta-net.com/')

    #歌ネットでアーティスト検索
    element = driver.find_element(By.XPATH, 
    "/html/body/div[1]/div/div[1]/div[1]/div[2]/form/div/input")
    artist = artist_name
    element.send_keys(artist)

    #検索ボタンをクリック
    element = driver.find_element(By.XPATH, 
    "/html/body/div[1]/div/div[1]/div[1]/div[2]/form/div/button")
    element.click()
    driver.quit()

    #アーティストの検索結果から番号を取得
    load_url = 'https://www.uta-net.com/search/?target=art&type=in&keyword=' + artist



    #それぞれ歌手の情報の取得
    base_url = 'https://www.uta-net.com/'
    html = load(load_url)
    #曲ごとのurlを格納
    song_url = []
    #歌を格納
    song_name = []

    #曲のurlを取得
    #tdのurlを格納
    for td in get_tags(html, 'td'):
        #a要素の取得
        for a in get_tags(td, 'a'):
            #print(a.get ('href'))
            #href属性にsongを含むか否か
            if 'artist' in a.get ('href'):
                #urlを配列に追加
                song_url.append(base_url + a.get('href'))
            #Song
            for tag in a:
                #id検索を行うため、一度strにキャスト
                tag = str(tag)
                simple_row = parse(tag)
                if ("歌詞" not in simple_row) and (len(simple_row)>0):
                    song_name.append(simple_row) 

    singer_dist = {}
    for i in range(len(song_name)):
        singer_dist[song_name[i]] = song_url[i]

    return singer_dist



#歌手のurlから、曲一覧と曲に対応したurlをまとめた辞書を返す
def song_searcher(artist_url):
    html = load(artist_url)
    #曲ごとのurlを格納
    song_url = []
    #歌を格納
    song_name = []


    #曲のurlを取得
    base_url = 'https://www.uta-net.com/'
    #tdのurlを格納
    for td in get_tags(html, 'td'):
        #a要素の取得
        for a in get_tags(td, 'a'):
            #href属性にsongを含むか否か
            if 'song' in a.get ('href'):
                #urlを配列に追加
                song_url.append(base_url + a.get('href'))


    #曲の情報の取得
    for i, page in enumerate(song_url):
        html = load(page)
        #Song
        for tag in get_tag(html, 'h2'):
            #id検索を行うため、一度strにキャスト
            tag = str(tag)
            simple_row = parse(tag)
            song_name.append(simple_row)   
        


    song_dist = {}
    for i in range(len(song_name)):
        song_dist[song_name[i]] = song_url[i]

    return song_dist


def liric_seacher(song_url):
    #曲の情報の取得
    #print('{}曲目:{}'.format(i + 1, page))
    html = load(song_url)          

    #Lyric
    id_ = str(get_id(html, '#kashi_area'))
    if r'id="kashi_area"' in id_:
        #歌詞部分
        song_info = parse_lyric(id_)
        #1秒待機(サーバの負荷を軽減)
        time.sleep(1)
    
    return song_info
