import re
import requests
import os
import queue


# from anytree import Node, RenderTree


def calc(link, counter, pre_path, pre_node):
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
        if len(List[i]) > 2:
            print('mehrnoush:%s,%s,,,%s' % (List[i][0], List[i][1], List[i][0]+List[i][1]))
            if List[i][0] + List[i][1] != 'ht':
                List[i] = link + List[i]
        else:
            List[i] = link + List[i]
        node = pre_node + "." + str(j)
        path = pre_path + "/" + node
        # t = Node(node, parent=pre_node)
        d[path] = List[i]
        os.mkdir(path)
        calc(List[i], counter, path, node)
        j += 1
    print("my List: %s" %str(List))

    q.put(List)
    print(q.get())



def search(link):
    for key, value in d.items():
        if value == link:
            print("Yes!")
            print(key)
            return

    print("No!")
    return


# def main():
q = queue.Queue()
d = {}  # hash table

counter = 0
given_link = input('please input your line:').strip()
given_level = int(input('please enter a level: ').strip())

# t = Node("C")  # tree
# subT = []
# subT = Node("1", parent="C")
d["C:/1"] = given_link
os.mkdir("C:/1")
calc(given_link, 0, "C:/1", "1")
# for i in d:
#     print(i)
search(given_link)
# for pre, fill, node in RenderTree(t):
#     print("%s%s" % (pre, node.name))

# if __name__ == 'main':
#     main()
