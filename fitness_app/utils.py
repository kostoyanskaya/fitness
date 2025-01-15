import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def search_in_templates(query):
    results = []
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".html") and filename != "base.html" and filename != "home.html":
            with open(
                os.path.join(TEMPLATES_DIR, filename), 'r', encoding='utf-8'
            ) as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append(filename)
    return results
