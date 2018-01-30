from flask import Flask
from flask_exercise.connect_db import udn
app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def HelloWorld():
    h = ""
    for doc in udn.find()[:3]:
        h += u"<a href=#>{}</a><br>".format(doc["title"])
        h += "<font>{}</font>".format(str(doc["date_released"].date()))
        h += "<br><br>"

    return h

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
