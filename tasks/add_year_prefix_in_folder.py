import os

class AddYearPrevixInFolderName(object):

    @staticmethod
    def run(year_prefix, root_folder):

        for file in os.scandir(root_folder):
            if file.is_dir():

                if not file.name.startswith(year_prefix):
                    new_name = year_prefix + ' ' + file.name
                    new_path = os.path.join(os.path.dirname(file.path), new_name)
                    print("------------------------------------------------------")
                    print(f"{file.path}")
                    print(f"{new_path}")
                    os.rename(file.path, new_path)

def main():
    year = "1992"
    AddYearPrevixInFolderName.run(year, f"p:\\pics\\{year}")
    AddYearPrevixInFolderName.run(year, f"d:\\picsHres\\{year}")

if __name__ == '__main__':
  main()