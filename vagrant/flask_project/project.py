from bson.objectid import ObjectId
from flask import Flask, render_template
from flask_project.connect_db import udn
app = Flask(__name__)


@app.route('/')
@app.route('/news')
def list_all_news():
    news = udn.find({})
    return render_template('list.html', news=news)


@app.route("/news/<string:news_id>/")
def show_contest(news_id):
    news = udn.find_one({"_id": ObjectId(news_id)})
    return news["content"]

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


# if __name__ == "__main__":
#     print(type(ObjectId("123456789999")))