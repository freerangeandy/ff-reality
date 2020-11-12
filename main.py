from flask import Flask, render_template
from ff_projections import positions, analysts, get_comparison, get_full_comparison

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

if __name__ == '__main__':
    app.run(debug=True)
