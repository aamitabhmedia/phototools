import context; context.set_context()
import gphoto.folder_cache as folder_cache

def main():
    cache = folder_cache.load("/d/picsHres")
    print(cache)

if __name__ == '__main__':
  main()