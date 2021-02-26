import context; context.set_context()

import gphoto
import util
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
from gphoto.google_album_images import GoogleAlbumImages

gphoto.init()

def do_work():
    albums_cache = GoogleAlbums.load_albums()
    images_cache = GoogleImages.load_images()
    album_images_cache = GoogleAlbumImages.load_album_images()

    album_ids = albums_cache['ids']
    album_titles = albums_cache['titles']

    image_ids = images_cache['ids']
    image_filenames = images_cache['filenames']

    album_images_dict = album_images_cache['album_images']
    image_albums_dict = album_images_cache['image_albums']

    result = {}

    for image_id, image_albums in image_albums_dict.items():
        image = image_ids[image_id]
        if len(image_albums) > 1:
            consider_image = False
            start_pattern = None
            for album_id in image_albums.keys():
                album = album_ids[album_id]
                if 'title' in album:
                    title = album['title']
                    if start_pattern is None:
                        start_pattern = title[0:8]
                    else:
                        if start_pattern != title[0:8]:
                            consider_image = True
                            break
                        else:
                            pass
                else:
                    consider_image = True
                    break

            if consider_image:
                print(image['productUrl'])
                for album_id in image_albums.keys():
                    album = album_ids[album_id]
                    title = "NONE"
                    if 'title' in album:
                        title = album['title']
                    print(f"  '{title}':  {album['productUrl']}")


# show_shared = True
# album_ids = albums_cache['ids']
# for key, album in album_ids.items():
# 	shared = album['shared']
# 	title = "NONE"
# 	if 'title' in album:
# 		title = album['title']
# 	if shared == show_shared:
# 		print(f"'{title}', '{album['id']}'")

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    do_work()

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()