from flask import Flask
from flask import render_template
import sqlite3 as db

app = Flask(__name__)


url_job = ["python", "java", "C", "web", "html", "UI", "javascript"]
job_head_list = ['job_href', 'job_name', 'company_href', 'company_name',
                 'providesalary_text', 'workarea_text', 'updatedate',
                 'companytype_text', 'jobwelf', 'attribute_text',
                 'companysize_text', 'companyind_text']
db_path = "51_job.db"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/index.html')
def index():
    # return render_template("index.html")
    return home()


@app.route('/data.html')
def data():
    data_dict = {}
    for name in url_job:
        data_list = []
        conn = db.connect(db_path)
        cur = conn.cursor()
        sql = "select * from %s" % name
        information = cur.execute(sql)

        for item in information:
            data_list.append(item)

    data_dict[name] = data_list

    return render_template("data.html", data_dict=data_dict)


@app.route('/analysis.html')
def why():
    return render_template("analysis.html")


@app.route('/word_cloud.html')
def about():
    return render_template("word_cloud.html")


if __name__ == '__main__':
    app.run()
