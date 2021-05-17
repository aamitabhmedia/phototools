import context; context.set_context()
import fire

class GphotoAlbum(object):

  def create(self, folder, share:bool = True):
    """
    Parameters
            ----------
            folder : string
                path to local album folder
            share : bool
                Make album shareable (default == sharable)

            Returns
            -------
            string
                Returns Google album id, if successful
    """
    # """
    # Create an album and return album id
    # Arguments:
    #     title: Title of the album
    #     --share | --noshare: make album shareable (--share is deafault)
    # """
    return f"creating album '{title}', as Shared={share}"

  def get(self, title):
    return f"return album '{title}'"

