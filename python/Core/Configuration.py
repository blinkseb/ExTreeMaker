__author__ = 'sbrochet'

from collections import namedtuple

class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

Collection = namedtuple('Collection', 'name type input_tag')

class Configuration:

    """
    The class name of the analyzer you want to run. Must be specified
    """
    analyzer = None

    """
    The name of the output file produced by the framework. Can be overridden when launching runFramework.py
    """
    output_file = 'output_mc.root'

    """
    The name of the output tree
    """
    tree_name = 'tree'

    """
    List of producers you want to run before your analyzer. Products produced by these producers will be stored
    inside the output file tree.

    The framework expect each value of the list to be an instance of :class:`Bunch` with at least the fields
    ``clazz`` and ``alias`` set.
    """
    producers = []

    """
    List of collections your analyzer depends on.

    The framework expect each value of this list to be an instance of :class:`Collection`
    """
    collections = []

    analyzer_configuration = {}
