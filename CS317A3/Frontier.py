# CMPT 317.201809: A Python implementation of Frontier interfaces for uninformed search.
#
# Simple implementations of the Frontier interface.
#   Frontier: a base class
#   FrontierFIFO: implements FIFO, for use by BFS
#   FrontierLIFO: implements LIFO, for use by DFS
#

class Frontier(object):
    """
    A base class for Frontiers.  A Frontier is a list.
    """

    def __init__(self):
        self._nodes = []

    def __len__(self):
        return len(self._nodes)

    def is_empty(self):
        return len(self._nodes) == 0


class FrontierFIFO(Frontier):
    """ This is a typical FIFO queue.
    """

    def __init__(self):
        Frontier.__init__(self)

    def add(self, aNode):
        """add the new state on the end"""
        self._nodes.append(aNode)

    def remove(self):
        """remove the first state"""
        val = self._nodes.pop(0)
        return val


class FrontierLIFO(Frontier):
    """This version is a LIFO Stack"""

    def __init__(self):
        Frontier.__init__(self)

    def add(self, aNode):
        """Add the new state on the end"""
        self._nodes.append(aNode)

    def remove(self):
        """remove the state from the end"""
        val = self._nodes.pop()
        return val


class FrontierLIFO_DL(FrontierLIFO):
    """ This is a LIFO queue, but nodes that exceed a limit are discarded.
    """

    def __init__(self, dlimit):
        FrontierLIFO.__init__(self)
        self.__dlimit = dlimit
        self._cutoff = False

    def add(self, aNode):
        """add the new state on the end"""
        if aNode.depth <= self.__dlimit:
            self._nodes.append(aNode)
        elif not self._cutoff:
            self._cutoff = True
