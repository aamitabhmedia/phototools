import context; context.set_context()
import util
import tasks

dups = tasks.duplicate_pics_folder_images("p:\\pics")
util.pprint(dups)