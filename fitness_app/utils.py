import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def search_in_templates(query):
    results = []
    for filename in os.listdir(TEMPLATES_DIR):
        if (filename.endswith(".html") and
                filename not in {"base.html", "home.html"}):
            file_path = os.path.join(TEMPLATES_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if query.lower() in content.lower():
                    results.append(filename)
    return results
