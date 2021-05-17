import context; context.set_context()
import fire

from tasks.gphoto_album import GphotoAlbum
from tasks.gphoto_image import GphotoImage

class Root(object):

  def __init__(self):
    self.album = GphotoAlbum()
    self.image = GphotoImage()

  def run(self):
    # self.ingestion.run()
    # self.digestion.run()
    return 'Root complete'

if __name__ == '__main__':
  fire.Fire(Root)