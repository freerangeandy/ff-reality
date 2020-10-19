from flask import Flask, render_template
from ff_projections import get_projections

app = Flask(__name__)

@app.route('/')
def my_index():
    return render_template("index.html",
        token="Hello flask + react"
    )

@app.route('/test')
def testing():
    df_html = get_projections()
    return render_template("index.html",
        token= df_html
    )


app.run(debug=True)
