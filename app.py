from flask import Flask, request, render_template_string
from duckduckgo_search import DDGS

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Code Generator Web Search</title>
    <style>
        body { background-color: #111; color: #eee; font-family: sans-serif; padding: 2rem; }
        input, button { padding: 0.6rem; width: 100%; margin-top: 1rem; background: #222; color: #eee; border: 1px solid #555; }
        button { background-color: #00ffaa; color: black; font-weight: bold; cursor: pointer; }
        .result { margin-top: 1.5rem; padding: 1rem; background-color: #222; border-left: 4px solid #00ffaa; }
        a { color: #00ffaa; text-decoration: none; }
    </style>
</head>
<body>
    <h1>🔍 Code Generator Web Search</h1>
    <form method="POST">
        <label for="query">Enter your prompt:</label>
        <input type="text" name="query" value="{{ query or '' }}" placeholder="e.g. code generator using Python" required />
        <button type="submit">Search</button>
    </form>

    {% if results %}
        <h2>Top Results:</h2>
        {% for result in results %}
            <div class="result">
                <a href="{{ result['href'] }}" target="_blank"><strong>{{ result['title'] }}</strong></a>
                <p>{{ result['body'] }}</p>
            </div>
        {% endfor %}
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=5)
            results = list(search_results)

    return render_template_string(HTML_TEMPLATE, query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
