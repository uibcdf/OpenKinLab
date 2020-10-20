class Microstate():


    def __init__(self, name, node=None):

        self.name=None
        self.node=None
        self.link=None

        self.name=name
        self.node=node

        if node is not None:

            node.microstate=self

    def add_link(self, edge):

        if end.microstate.name in self.link:
            raise ValueError("The microstate is already in this network.")

        self.link[end.microstate.name]=edge

