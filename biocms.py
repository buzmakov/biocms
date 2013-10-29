import codecs
from flask import Flask, render_template, send_file
import markdown
import os
import glob

app = Flask(__name__)


@app.route('/')
def index():
    return pages('index.html')


@app.route('/<path:path>')
def pages(path):
    user_html = get_html_by_path(path)
    
    if not user_html is None:
        toc = get_toc(path) 
        return render_template('index.html', main_menu=list(build_main_menu()),
                               user_html=user_html, toc=toc)
    else:
        file_name = os.path.join('data', path)
        return send_file(file_name, as_attachment=True)


def filter_url(url):
    turl = url.split('.')
    try:
        t = int(turl[0])
        if turl[1][0] == ' ':
            turl[1] = turl[1][1:]
        return '.'.join(turl[1:])
    except ValueError:
        return turl


def build_main_menu():
    for root, dirs, files in os.walk('data'):
        if root == 'data':
            first_level = sorted(dirs)
            break

    for fl in first_level:
        first_lvl_name = get_abs_path( fl)
        for r, d, f in os.walk(first_lvl_name):
            if r == first_lvl_name:
                de = [dd.decode('utf-8') for dd in sorted(d)]
                sub_dirs = [{'label': filter_url(dd), 'url': u'/'.join([fl.decode('utf-8'), dd])} for dd in de]
                yield {'header': {'label': filter_url(fl.decode('utf-8')), 'url': fl.decode('utf-8')},
                       'sub_menus': sub_dirs}


def get_html_by_path(web_path):
    if web_path.endswith(r'.html'):
        index_file = get_abs_path(web_path[:-len(r'.html')]) + '.md'
        if os.path.exists(index_file):
            input_file = codecs.open(index_file, mode="r", encoding="utf-8")
            text = input_file.read()
            input_file.close()
            html = markdown.markdown(text)
            return html
        elif os.path.exists(get_abs_path(web_path)):
            input_file = codecs.open(get_abs_path(web_path), mode="r", encoding="utf-8")
            html = index_file.read()
            input_file.close()
            return html
        return index_file + u' not found'
    else:
        return None


def get_toc(web_path):
    dir_name = os.path.dirname(get_abs_path(web_path))
    if not 'toc.md' in os.listdir(os.path.join(dir_name)):
        html = get_html_by_path(web_path)
        tocstr = html.split('\n')[0]
        if tocstr.startswith(r'<!--toc:'):
            res = {'type': 'auto'}
            level = int(tocstr[8])
            levels = ','.join(['h' + str(i + 1) for i in range(level)])
            res['levels'] = levels
            return res
        else:
            return {'type': 'none'}
    else:
        toc = get_html_by_path(os.path.join(get_web_path(dir_name), 'toc.html'))
        toc = toc.splitlines()[1:-1]
        toc = '\n'.join(toc)
        return {'type': 'manual', 'html': toc}

def get_abs_path(web_path):
    return os.path.join('data', web_path)

def get_web_path(abs_path):
    return abs_path[len('data/'):]

if __name__ == '__main__':
    app.run(debug=True)
    #   for m in build_main_menu():
    #       print m['header']
    #       for s in sorted(m['sub_menus']):
    #           print '\t'+s