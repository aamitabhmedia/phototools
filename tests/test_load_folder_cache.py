import context; context.set_context()
import pprint
import gphoto.folder_cache as folder_cache

def main():
    cache = folder_cache.load("d:\\picsHres\\2040")
    pp = pprint.PrettyPrinter(indent=2, sort_dicts=False)
    pp.pprint(cache)

if __name__ == '__main__':
  main()