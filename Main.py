import re
import requests
import os
import queue
from Tree import Tree
import urllib.request
from bs4 import BeautifulSoup
from pathlib import Path
import shutil
import threading
import View


class Queue_Object:
    def __init__(self, link, node, path):
        self.link = link
        self.path = path
        self.node = node


def save_web_page(url, file_path, file_name):
    try:
        full_path = file_path + "/" + file_name
        f = open(full_path + '.html', 'w', encoding='utf-8')
        message = """<head></head>
                <body><p>AMK_MNA Web crawler!</p>
                <p>
                """ + requests.get(url).text + """
                </p>
                </body>
                </html>"""
        f.write(message)
        f.close()
    except Exception as e:
        print('error at saving web page,url:' + url + ',' + str(e))


def make_dir(link):
    path = os.getcwd() + "/1"
    fileName = Path(path)
    if fileName.exists():
        shutil.rmtree(path)

    d[path] = link
    os.mkdir(path)
    return path


def show_tree_and_page():
    txt = ''
    for i, j in Tree.links.items():
        l2 = t.get_children_of_Node(node=i)
        if i == 0:
            txt += '<a href=\'' + j + '\'>' + '<b>root of tree is:</b> ' + j + '</a>' + '<br><br>'
            print('root of tree:' + j)
        else:
            txt += '<br>Node:<br>'
            txt += '<a href=\'' + i + '\'>' + i + '</a>' + '<br>'
            print('children of node:' + i)
            txt += 'children:<br>'
            for k in l2:
                print(k)
                txt += '--<a href=\'' + k + '\'>' + k + '</a>' + '<br>'
    View.set_message(txt)
    View.open_page()


def fix_links(link, base_url):
    if len(link) > 3:
        if link[0] + link[1] + link[2] != 'htt':
            link = re.sub(r'^/*', '', link)
            temp = base_url + link
            try:
                r = requests.get(temp)
                if r.status_code == 200:
                    link = temp
                else:
                    link = 'http://' + link
            except:
                link = 'http://' + link
    else:
        link = base_url + link
    return link


def get_match_links(link):
    List = None
    try:
        content = requests.get(link).text
        key = '<a href=[\'\"](.*?)[\'\"]'
        List = list(set(re.findall(key, content)))
        for i in range(len(List)):
            List[i] = fix_links(List[i], link)
    except:
        print('your link was corrupted')
    return List


def dl_jpg(url, file_path, file_name):
    full_path = file_path + "/" + str(file_name) + '.jpg'
    try:
        urllib.request.urlretrieve(url, full_path)
    except Exception as e:
        print('exception at dl_jpg :' + url + ' , ' + str(e))


# return a list of images link of a given link
def getting_images_links(url):
    images = []
    try:
        r = requests.get(url)
        html_content = r.text
        soup = BeautifulSoup(html_content, "html.parser")
        for img in soup.findAll('img'):
            img_link = img.get('src')
            img_link = fix_links(img_link, url)
            images.append(img_link)
        print('url for getting images:' + url)
        print('images:' + str(images))
    except Exception as e:
        print('error in dl of image,url:' + url + ',' + str(e))

    return images


def crawl(link, counter, pre_path, pre_node):
    # terminate condition:
    if counter == given_level - 1:
        return

    print('counter:' + str(counter) + ',' + 'given_level:' + str(given_level))
    counter += 1

    # make a queue for storing links of this page
    q = queue.Queue()

    List = get_match_links(link)

    # expanding of the tree:
    list_of_children = []
    for i in range(len(List)):
        list_of_children.append(List[i])

    Tree.links[link] = list_of_children
    j = 1
    for i in range(len(List)):
        # To avoid repetitive values in dict:
        if List[i] in d.values():
            continue
        node = pre_node + "." + str(j)
        path = pre_path + "/" + node
        Q = Queue_Object(List[i], node, path)
        q.put(Q)

        # make directory
        d[path] = List[i]
        os.mkdir(path)
        # getting images:
        images = getting_images_links(List[i])
        for n in range(len(images)):
            dl_jpg(images[n], path, n)
        save_web_page(Q.link, Q.path, 'hi')
        j += 1

    print("counter is:%i and given_level is:%i and my List: %s" % (counter, given_level, str(List)))
    while q.qsize() != 0:
        Q = q.get()
        thread = threading.Thread(target=crawl, args=(Q.link, counter, Q.path, Q.node,))
        thread.start()
        thread.join()


d = {}  # hash table
given_link = input('please input your link:').strip()
path1 = make_dir(given_link)
given_level = int(input('please enter a level: ').strip())

save_web_page(given_link, path1, 'hello')
images = getting_images_links(given_link)
for n in range(len(images)):
    dl_jpg(images[n], path1, n)
t = Tree()
Tree.links[0] = given_link
crawl(given_link, 0, path1, "1")
show_tree_and_page()
