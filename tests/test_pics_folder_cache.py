import context; context.set_context()
import pprint
from gphoto.pics_folder import PicsFolder

def main():
    cache = PicsFolder.cache_folder("d:\\picsHres\\2040")
    pp = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)
    pp.pprint(cache)
    PicsFolder.save_cache()
    PicsFolder.load_cache()
    pp.pprint(PicsFolder.cache())

if __name__ == '__main__':
  main()