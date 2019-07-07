__author__ = 'wangyi'

class Node(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

        self.father = None
        self.children = list()
        self.level_pos = None

    def __str__(self):
        return "%s: \n%s\n" % (self.name, str(self.data))

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
        if child.father is not self:
            child.set_father(self)
        return self

    def add_children(self, children):
        filtered_children = filter(lambda ch: True if ch not in self.children else False, children)
        self.children = self.children.extend(filtered_children)
        return self

    def set_children(self, children):
        self.children = children
        return self

    def set_father(self, father):
        self.father = father
        father.add_child(self)
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