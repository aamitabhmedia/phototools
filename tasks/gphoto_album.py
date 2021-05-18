import context; context.set_context()
import fire

class GphotoAlbum(object):
  """Module to handle Google album specific commands"""

  def create(self, folder, share:bool = True):
    """Create album given 'local folder path', '--share' (default) to make it shareable"""

    return f"creating album '{folder}', as Shared={share}"

  def get(self, title=None, id=None):
    """Return 'album' object given the 'title' or 'id'"""
    
    return f"return album for 'title={title}' or 'id={id}'"

