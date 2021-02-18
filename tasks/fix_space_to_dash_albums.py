"""
Replace spaces in the date with dashes like this in src/target subfolders
    2014 05 11 Mother's Day
        to
    2014-05-11 Mother's Day
"""

import os

class SpaceToDashAlbums(object):

    @staticmethod
    def run(year_pattern, root_folder):

        start_pattern = year_pattern + " "
        for file in os.scandir(root_folder):
            if file.is_dir():
                # print(f"name='{file.name}, '{os.path.dirname(file.path)}''")
                if file.name.startswith(start_pattern):
                    subs = file.name.split(' ')
                    dt = subs[0] + '-' + subs[1] + '-' + subs[2]
                    desc = " ".join(subs[3:])
                    new_name = dt + ' ' + desc
                    new_path = os.path.join(os.path.dirname(file.path), new_name)
                    print("------------------------------------------------------")
                    print(f"{file.path}")
                    print(f"{new_path}")
                    os.rename(file.path, new_path)

def main():
    year = "1992"
    SpaceToDashAlbums.run(year, f"p:\\pics\\{year}")
    SpaceToDashAlbums.run(year, f"d:\\picsHres\\{year}")

if __name__ == '__main__':
  main()