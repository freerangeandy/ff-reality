from flask import Flask, render_template, request
from ff_projections import positions, analysts, get_comparison, get_full_comparison

position_list = [(num, position.upper()) for num, position in enumerate(positions)]
analyst_list = [(num, analyst) for num, analyst in enumerate(analysts)]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
        weeks=range(1,8),
        positions=position_list,
        analysts=analyst_list
    )

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        week_no = int(request.form['weeks-select'])
        position_idx = int(request.form['positions-select'])
        analyst_idx = int(request.form['analysts-select'])


        return render_template("index.html",
            weeks=range(1,8),
            positions=position_list,
            analysts=analyst_list,
            error=f"Week: {week_no}, Position: {position_list[position_idx][1]}, Analyst: {analyst_list[analyst_idx][1]}"
        )

if __name__ == '__main__':
    app.run(debug=True)
