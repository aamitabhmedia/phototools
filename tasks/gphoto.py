import fire


class AlbumModule(object):

  def create(self, title, share:bool = True):
    return f"creating album '{title}', as Shared={share}"

  def get(self, title):
    return f"return album '{title}'"

class ImageModule(object):

  def upload(self, filename, album_id=None):
    return f"Uploading file '{filename}', albu_id='{album_id}'"

  def status(self):
    return 'Image Status is GOOD'

class Root(object):

  def __init__(self):
    self.album = AlbumModule()
    self.image = ImageModule()

  def run(self):
    # self.ingestion.run()
    # self.digestion.run()
    return 'Root complete'

if __name__ == '__main__':
  fire.Fire(Root)