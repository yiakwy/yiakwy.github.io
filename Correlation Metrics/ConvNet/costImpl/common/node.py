__author__ = 'wangyi'

class Node(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

        self.father = None
        self.children = list()
        self.level_pos = None

    def __str__(self):
        return str(self.data)

    def add_child(self, child):
        self.children.append(child)
        return self

    def add_children(self, children):
        self.children = self.children.extend(children)
        return self

    def set_children(self, children):
        self.children = children
        return self

    def set_father(self, father):
        self.father = father
        father.childer.add_child(self)
        return self

    def set_level_pos(self, pos):
        self.level_pos = pos

    def get_children(self, i=None):
        if i is None:
            return self.children
        else:
            return self.children[i]

    def get_father(self):
        return self.father