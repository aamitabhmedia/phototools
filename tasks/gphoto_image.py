import context; context.set_context()

import fire

class GphotoImage(object):
  """
  Google Image Command Module
  """

  def upload(self, filename, album_id=None):
    """
    Upload an image, and it will return image id
    """
    return f"Uploading file '{filename}', album_id='{album_id}'"

  def status(self):
    return 'Image Status is GOOD'