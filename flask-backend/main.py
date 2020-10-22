from flask import Flask, render_template
from ff_projections import analysts, get_comparison

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

def cli_function():
    week_no = int(input("Which week? "))
    while week_no not in range(1, 18):
        print("Week %s is not valid (integer between 1 and 17)" % week_no)
        week_no = int(input("Which week? "))
    print("Which analyst?")
    analyst_list = ', '.join(["%s: %s" % (num, analysts) for num, analysts in enumerate(analysts, start=1)])
    analyst_index = int(input("(" + analyst_list + "): "))
    while analyst_index not in range(1, 7):
        print("%s is not valid (integer between 1 and 6)" % analyst_index)
        analyst_list = ', '.join(["%s: %s" % (num, analysts) for num, analysts in enumerate(analysts, start=1)])
        analyst_index = int(input("(" + analyst_list + "): "))
    df_c = get_comparison(week_no, analyst=analysts[analyst_index-1])
    print(df_c)

if __name__ == '__main__':
    app.run(debug=True)
