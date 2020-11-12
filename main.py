from flask import Flask, render_template
from ff_projections import positions, analysts, get_comparison, get_full_comparison

app = Flask(__name__)

@app.route('/')
def my_index():
    position_list = [(num, position.upper()) for num, position in enumerate(positions)]
    analyst_list = [(num, analyst) for num, analyst in enumerate(analysts)]

    return render_template("index.html",
        weeks=range(1,8),
        positions=position_list,
        analysts=analyst_list
    )

@app.route('/success')
def success():
    df_html = get_projections()
    return render_template("index.html",
        table= None
    )

if __name__ == '__main__':
    app.run(debug=True)
