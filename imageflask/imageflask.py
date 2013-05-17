from flask import Flask, render_template, request
import GlobalConfiguration
from Search import Search
import random

app = Flask(__name__)

clippyjs_agents = ['Bonzi', 'Clippy', 'F1', 'Genie', 'Genius', 'Links', 'Merlin', 'Peedy', 'Rocky', 'Rover']


def random_clippyjs_agent():
    return clippyjs_agents[random.randint(0, len(clippyjs_agents)-1)]

@app.route('/')
def home():
    return render_template('search.html', clippyjs_agent=random_clippyjs_agent())

@app.route('/s', methods=['POST'])
def search():
    query = request.form['query']
    s = Search()
    results = s.search(query)

    return render_template('search.html', query=query, results=results, clippyjs_agent=random_clippyjs_agent())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
