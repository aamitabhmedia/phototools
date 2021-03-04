import logging
from googleapi.google_service import GoogleService

class AlbumAPI(object):

    # -----------------------------------------------
    def get_album_by_title(service, title):
        """
            The function returns the album object if it already exists.
            Otherwise it returns None
        """
        request_body = {
            'album': {'title': title}
        }
        response = NotImplemented
        try:
            response = service.albums().create(body=request_body).execute()
        except Exception as e:
            raise Exception(f"AlbumsAPI:create_album: Error while calling album create '{title}'")


    # -----------------------------------------------
    def create_album(service, title):

        request_body = {
            'album': {'title': title}
        }
        response = NotImplemented
        try:
            response = service.albums().create(body=request_body).execute()
        except Exception as e:
            raise Exception(f"AlbumsAPI:create_album: Error while calling album create '{title}'")

        if not response:
            raise Exception(f"AlbumsAPI:create_album: No response after created album '{title}'")

        # If not album returned then create failed
        if "id" not in response:
            raise Exception(f"AlbumsAPI:create_album: Missing id after created album '{title}'")

        logging.info(f"AlbumsAPI:create_album: Album '{title}' created with id:'{response['id']}'")

        return response

    # -----------------------------------------------
    def make_album_sharable(service, album_id, share=True):
        request_body = {
            'sharedAlbumOptions': {
                'isCollaborative': True,
                'isCommentable': True
            }
        }

        response = None
        try:
            if share:
                response = service.albums().share(
                    albumId=album_id,
                    body=request_body
                ).execute()
            else:
                response = service.albums().unshare(
                    albumId=album_id,
                    body=request_body
                ).execute()
        except Exception as e:
            raise Exception(f"AlbumsAPI.make_album_sharable: Error while sharing album '{album_id}', e: '{str(e)}'")

        return response