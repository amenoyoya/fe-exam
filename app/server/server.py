from __init__ import Application
from markdown import markdown
import os

app = Application.create(__name__)
import auth_api

# GET /api/markdown/<filename> => <filename>のMarkdownをHTMLに変換して返す
@Application.api('/markdown/<string:filename>', methods=['GET'])
def md(filename):
    path = f'./markdown/{filename}.md'
    if not os.path.isfile(path):
        return 'file not found'
    with open(path) as f:
        return markdown(f.read(), extensions=[
            'toc', 'attr_list', 'tables', 'fenced_code'
        ])

if __name__ == '__main__':
    Application.run(debug=True)
