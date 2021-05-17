import context; context.set_context()
import fire

class GphotoAlbum(object):

  def create(self, title, share:bool = True):
    return f"creating album '{title}', as Shared={share}"

  def get(self, title):
    return f"return album '{title}'"

