from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home(name=None):
    return render_template("home.html", name=name)

@app.route("/image", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        print("I'm here")
        print(request.form["searchText"])
        print(request.form.get('searchText'))
        searchText = request.form["searchText"]
        print(searchText)
        print(type(searchText))
    
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
        print(output)
        if "err" in output:
            print(f"Issues with generating image. Error: {output['err']}")
        else:
            print("image generated successfully!")
    
        return render_template("home.html", output = output)
    return render_template("home.html", error = "request method is GET. Use Post")