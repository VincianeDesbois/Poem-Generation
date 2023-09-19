import os

from flask import Flask, render_template, request, session

from generation_t5 import gen_poem

app = Flask(__name__)
app.secret_key = str(os.urandom(32))


@app.route("/")
def index():
    return render_template("accueil.html")


@app.route("/chose_words/", methods=["POST", "GET"])
def selection_mots():
    if request.method == "POST":
        return render_template("selection_mots.html")
    if request.method == "GET":
        return render_template("selection_mots.html")


@app.route("/chosen_words/", methods=["POST"])
def model():
    if request.method == "POST":
        default_value = "0"
        word1 = request.form.get("word1", default_value).lower()
        word2 = request.form.get("word2", default_value).lower()
        word3 = request.form.get("word3", default_value).lower()
        session["word1"] = word1
        session["word2"] = word2
        session["word3"] = word3
        return render_template(
            "longueur_vers.html", word1=word1, word2=word2, word3=word3
        )


@app.route("/generate_poem/", methods=["POST", "GET"])
def model_gen_poem():
    if request.method == "POST":
        default_value = "NOT ABLE TO GENERATE ANY POEM"
        input_poem = [session["word1"], session["word2"], session["word3"]]
        lenght = request.form.get("vers", default_value)
        session["lenght"] = int(lenght[:1])
        poem = gen_poem(input_poem, session["lenght"])
        poem = poem.replace("\n", "<br>")
        session["poem"] = str(poem)
        return render_template("generate_poem.html", poem=str(poem), words=input_poem)

    if request.method == "GET":
        default_value = "NOT ABLE TO GENERATE ANY POEM"
        input_poem = [session["word1"], session["word2"], session["word3"]]
        poem = gen_poem(input_poem, session["lenght"])
        poem = poem.replace("\n", "<br>")
        session["poem"] = str(poem)
        return render_template("generate_poem.html", poem=str(poem), words=input_poem)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
