import pprint

_pprint_object = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)
def pprint(obj):
    """
    Pretty Prints the object in json format using the following
    pprint options:

        pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)

    """
    _pprint_object.pprint(obj)