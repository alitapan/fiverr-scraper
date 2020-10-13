import os
import shutil
import zipfile

os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/events/')
list = os.listdir()


print(str(min(os.listdir())).split(".")[0])

#shutil.copy(min(list), os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/old')


# with zipfile.ZipFile(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/' + str(min(os.listdir())), 'r') as zip_ref:
#     zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')


os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/covid-19_discussions/')
zip_file_path = str(min(os.listdir()))
print(zip_file_path)


class Test:

    def change_dir(self, flg=True):
        os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/data/')
        return

    def __init__(self):
        self.change_dir()
        print(os.listdir())

Test()
