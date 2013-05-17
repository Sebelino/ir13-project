from flask import Flask, render_template, request
import GlobalConfiguration
from Search import Search

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('search.html')

@app.route('/s', methods=['POST'])
def search():
    query = request.form['query']
    s = Search()
    results = s.search(query)

    return render_template('search.html', query=query, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
