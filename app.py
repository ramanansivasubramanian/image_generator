from flask import Flask, render_template, request
import requests
import itertools
import logging

logging.basicConfig(filename='record.log', level=logging.DEBUG)
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home(name=None):
    return render_template("home.html", name=name)

@app.route("/anagrams", methods=['GET', 'POST'])
def anagrams():
    if request.method == "POST":
        app.logger.info("Generating Anagrams")
        anagramText = request.form["searchText"]
        if anagramText:
            anagrams = ["".join(perm) for perm in itertools.permutations(anagramText)]
            app.logger.info("Anagrams generated successfully.")
            app.logger.debug(f"{anagrams}")
            return render_template("home.html", anagrams = anagrams)
        else:
            app.logger.error("Input string is empty.")
            return render_template("home.html", error = "Please provide a valid input. We've detected an empty string.")
    app.logger.error("Coudn't generate anagram. Request method is GET. Use Post.")
    return render_template("home.html", error = "Request method is GET. Use Post")


@app.route("/image", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        app.logger.info("Generating images.")
        searchText = request.form["searchText"]
        app.logger.info(f"Search text is: {searchText}")
        r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': searchText,
                'grid_size': 4
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )
        output = r.json()
        output['search_text'] = searchText

        if "err" in output:
            app.logger.error(f"Issues with generating image. Error: {output['err']}")
        else:
            app.logger.info("Image generated successfully!")
        return render_template("home.html", search = output)
    app.logger.error("Coudn't generate anagram. Request method is GET. Use Post.")
    return render_template("home.html", error = "request method is GET. Use Post")