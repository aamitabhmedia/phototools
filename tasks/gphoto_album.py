import context; context.set_context()
import fire

class GphotoAlbum(object):
  """Module to handle Google album specific commands"""

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
    return f"creating album '{folder}', as Shared={share}"

  def get(self, title):
    return f"return album '{title}'"

