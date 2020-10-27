from flask import Flask, render_template
from ff_projections import analysts, get_comparison, get_full_comparison

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

def cli_one_analyst():
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
    if df_c is None:
        print("Rankings don't exist for week %s" % week_no)
    else:
        print(df_c)

def cli_full_comparison():
    week_no = int(input("Which week? "))
    while week_no not in range(1, 18):
        print("Week %s is not valid (integer between 1 and 17)" % week_no)
        week_no = int(input("Which week? "))
    df_tuple = get_full_comparison(week_no)
    if df_tuple is None:
        print("Rankings don't exist for week %s" % week_no)
    else:
        present_comparison_tables(df_tuple)

def present_comparison_tables(dfs):
    projection_df = dfs[0]
    deviation_df = dfs[1]
    std_dev = dfs[2]
    print('                            -----------------------PROJECTIONS----------------------')
    print(projection_df)
    print('                                    ------------DIFFERENCES (ACTUAL - PROJECTED)------------')
    print(deviation_df)
    print('                       ----------------------------STD DEVIATIONS-------------------------')
    print(std_dev)

if __name__ == '__main__':
    cli_full_comparison()
    # app.run(debug=True)
