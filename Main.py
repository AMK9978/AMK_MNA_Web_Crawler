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


def save_web_page(url, file_path, file_name):
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


def dl_jpg(url, file_path, file_name):
    full_path = file_path + "/" + str(file_name) + '.jpg'
    print('full:' + full_path)
    try:
        urllib.request.urlretrieve(url, full_path)
    except:
        pass


# return a list of images link of a given link
def getting_images_links(url):
    # url = input('Enter a link to save its images:')
    r = requests.get(url)
    html_content = r.text

    soup = BeautifulSoup(html_content, "html.parser")

    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    print(images)
    for i in range(len(images)):
        images[i] = 'http:' + images[i]

    return images


class Queue_Object:
    def __init__(self, link, node, path):
        self.link = link
        self.path = path
        self.node = node


def calc(link, counter, pre_path, pre_node):
    try:
        q = queue.Queue()
        if counter == given_level - 1:
            return
        counter += 1
        # try:
        r = requests.get(link)
        content = r.text
        key = '<a href=[\'\"](.*?)[\'\"]'
        List = list(set(re.findall(key, content)))
        j = 1
        for i in range(len(List)):
            # To avoid repetitive values in dict:
            try:
                if List[i] in d.values():
                    continue
            except Exception as e:
                print(str(i))
            # To save accurate links:
            if len(List[i]) > 2:
                # print('HAHA:%s,%s,,,%s' % (List[i][0], List[i][1], List[i][0] + List[i][1]))
                if List[i][0] + List[i][1] != 'ht':
                    List[i] = link + List[i]
            else:
                List[i] = link + List[i]

            Tree.links[List[i]] = link
            node = pre_node + "." + str(j)
            path = pre_path + "/" + node
            Q = Queue_Object(List[i], node, path)
            # make directory
            q.put(Q)
            d[path] = List[i]
            os.mkdir(path)

            images = getting_images_links(List[i])
            for n in range(len(images)):
                dl_jpg(images[n], path, n)
            save_web_page(Q.link, Q.path, 'hi')
            j += 1

            print("my List: %s" % str(List))
            while q.qsize() != 0:
                Q = q.get()
                threading.Thread(target=calc, args=(Q.link, counter, Q.path, Q.node,))

    except Exception as e:
        print(str(e) + "," + link)
    # except Exception as e:
    #     print(str(e) + "," + link)


d = {}  # hash table

path1 = os.getcwd() + "/1"
fileName = Path(path1)
if fileName.exists():
    shutil.rmtree(path1)

counter = 0
given_link = input('please input your link:').strip()
given_level = int(input('please enter a level: ').strip())

d[path1] = given_link
os.mkdir(path1)
save_web_page(given_link, path1, 'hello')
t = Tree()
calc(given_link, 0, path1, "1")
txt = ''
for i in Tree.links:
    l2 = t.get_children_of_Node(node=i)
    txt += '<a href=\'' + i + '\'>' + i + '</a>'+'\n'
    print('children of node:' + i)
    for j in l2:
        print(j)
View.set_message(txt)
View.open_page()
