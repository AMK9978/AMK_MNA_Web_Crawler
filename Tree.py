class Tree:
    links = {}

    def __init__(self):
        pass

    def get_children_of_Node(self, node):
        list = []
        if node in Tree.links.keys():
            list = Tree.links[node]
        return list