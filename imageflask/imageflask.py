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
    response = 'Query: %s \n' % query
    response += '\n'.join(results)
    return response

if __name__ == '__main__':
    app.run()
