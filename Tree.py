class Tree:
    links = {}

    def __init__(self):
        pass

    def get_children_of_Node(self, node):
        list = []
        for key, value in Tree.links.items():
            if value == node:
                list.append(key)
        return list