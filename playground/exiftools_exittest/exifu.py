import atexit

@atexit.register
def goodbye():
  print(f"Goodbye: '{Exifu._exiftool}'")

class Exifu(object):

  _exiftool = None

  def get_exiftool():
    if Exifu._exiftool is None:
      Exifu._exiftool = "Initialized value"
    return Exifu._exiftool


def main():
  val = Exifu.get_exiftool()
  print(val)

if __name__ == '__main__':
  main()