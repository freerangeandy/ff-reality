from flask import Flask, render_template, request
from ff_projections import positions, analysts, get_comparison, get_full_comparison

position_list = [(num, position.upper()) for num, position in enumerate(positions)]
analyst_list = [(num, analyst) for num, analyst in enumerate(analysts)]
weeks_list = range(1, 17)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
        weeks=weeks_list,
        positions=position_list,
        analysts=analyst_list
    )

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        week_no = int(request.form['weeks-select'])
        position_idx = int(request.form['positions-select'])
        analyst_idx = int(request.form['analysts-select'])
        if analyst_idx < 99: # 'All' not selected
            comparison_df = get_comparison(week_no, positions[position_idx], analyst=analysts[analyst_idx])
            return render_template("index.html",
                weeks=weeks_list,
                positions=position_list,
                analysts=analyst_list,
                comparison_html=comparison_df.to_html(),
                message=f"Week: {week_no}, Position: {position_list[position_idx][1]}, Analyst: {analyst_list[analyst_idx][1]}"
            )
        else: # 'All' selected
            print(f"Week: {week_no}, Position: {position_list[position_idx][1]}")
            df_tuple = get_full_comparison(week_no, positions[position_idx])
            return render_template("index.html",
                weeks=weeks_list,
                positions=position_list,
                analysts=analyst_list,
                projections_html=df_tuple[0].to_html(),
                differences_html=df_tuple[1].to_html(),
                std_dev_html=df_tuple[2].to_html(),
                message=f"Week: {week_no}, Position: {position_list[position_idx][1]}"
            )

if __name__ == '__main__':
    app.run(debug=True)
