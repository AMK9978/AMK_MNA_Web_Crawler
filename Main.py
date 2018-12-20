import re
import requests
import os
import queue
from bs4 import BeautifulSoup
import urllib.request


class Queue_Object:
    def __init__(self, link, node, path):
        self.link = link
        self.path = path
        self.node = node


# download an image of a given link and put it in a given path
def dl_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


# return a list of images link of a given link
def getting_images_links(url):
    # url = input('Enter a link to save its images:')
    r = requests.get(url)
    html_content = r.text

    soup = BeautifulSoup(html_content, "html.parser")

    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    return images


def calc(link, counter, pre_path, pre_node):
    try:
        images_link = []
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
            node = pre_node + "." + str(j)
            path = pre_path + "/" + node
            Q = Queue_Object(List[i], node, path)
            # make directory
            q.put(Q)
            d[path] = List[i]
            os.mkdir(path)
            j += 1
        print("my List: %s" % str(List))
        while q.qsize() != 0:
            Q = q.get()
            calc(Q.link, counter, Q.path, Q.node)
    except Exception as e:
        print(str(e) + "," + link)


d = {}  # hash table

counter = 0
given_link = input('please input your line:').strip()
given_level = int(input('please enter a level: ').strip())

d["C:/1"] = given_link
os.mkdir("C:/1")
calc(given_link, 0, "C:/1", "1")

