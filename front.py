from flask import Flask, request, render_template
from main import artist_searcher, song_searcher, liric_seacher
import codecs
from evaluate import evaluate
from theme_out import make_theme
import math

app = Flask(__name__)


@app.route("/")
def bbs():
    theme = make_theme()
    file = codecs.open("theme.txt", "w", "utf-8")
    file.write(theme)
    file.close()
    return render_template("bbs.html", theme = theme)

@app.route("/arti", methods=["POST"])
def arti():
    artist = request.form["artist_name"]
    #song = request.form["song_name"]
    #message = "アーティスト名：" + artist + "\n 曲名："+song

    #name = changer(name)

    singers = artist_searcher(artist)

    """
    file = codecs.open("articles.txt", "a", "utf-8")
    file.write(singer_urls + "," +  + "\n")
    file.close()
    """

    return render_template("bbs_artist.html", singers = singers)

@app.route("/songname", methods=["POST"])
def songname():
    artist_url = request.form["last_artist_name"]
    songs = song_searcher(artist_url)

    return render_template("bbs_song.html", songs = songs)


@app.route("/liric", methods=["POST"])
def liric():
    song_url = request.form["last_song_name"]
    Liric = liric_seacher(song_url)
    Liric = Liric[2:-2]

    #追記------------------------------------------------
    file = codecs.open("player1.txt", "w", "utf-8")
    file.write(Liric)
    file.close()
    #---------------------------------------------------
    

    return render_template("bbs_final.html", Liric = Liric)




@app.route("/2")
def bbs2():
    file = codecs.open("theme.txt", "r", "utf-8")
    theme = file.readline()
    file.close()
    return render_template("bbs2.html", theme = theme)

@app.route("/arti2", methods=["POST"])
def arti2():
    artist = request.form["artist_name"]

    singers = artist_searcher(artist)


    return render_template("bbs_artist2.html", singers = singers)

@app.route("/songname2", methods=["POST"])
def songname2():
    artist_url = request.form["last_artist_name"]
    songs = song_searcher(artist_url)

    return render_template("bbs_song2.html", songs = songs)


@app.route("/liric2", methods=["POST"])
def liric2():
    song_url = request.form["last_song_name"]
    Liric = liric_seacher(song_url)
    Liric = Liric[2:-2]

    #追記------------------------------------------------
    file = codecs.open("player2.txt", "w", "utf-8")
    file.write(Liric)
    file.close()
    #---------------------------------------------------
    

    return render_template("bbs_final2.html", Liric = Liric)

@app.route("/judge", methods=["GET"])
def judge():
    file = codecs.open("player1.txt", "r", "utf-8")
    Liric1 = str(file.readline())
    file.close()

    file = codecs.open("player2.txt", "r", "utf-8")
    Liric2 = file.readline()
    file.close()

    file = codecs.open("theme.txt", "r", "utf-8")
    theme = file.readline()
    file.close()

    #print(Liric1)
    #print(Liric2)

    point1, point2 = evaluate(Liric1, Liric2, theme)
    #point1, point2 =[50, 100]

    return render_template("bbs_judge.html", point1 = math.ceil(point1), point2 = math.ceil(point2))


if __name__ == '__main__':
    app.debug = True  #デバッグモードTrueにすると変更が即反映される
    app.run()