import taglib
import yaml
import glob
import os
import taglib

class FileSearch():
    def __init__(self, configFile="./config.yml"):
        self.configFile = open(configFile)
        self.configYml = yaml.load(self.configFile)
        self.formats=self.configYml["Formats"]

    def search(self, path, *args):
        for fileFormat in self.formats:
            for fileName in glob.iglob((path + "/**/*" + fileFormat), recursive=True):
                media = {}
                media["path"] = os.path.dirname(fileName)
                media["filename"] = os.path.basename(fileName)
                tags = taglib.File(fileName)
                media["lenght"] = tags.length
                media["meta"] = tags.tags
                for key in args:
                    if key not in media["meta"]:
                        media["meta"][key] = None
                yield media

if __name__ == "__main__":
    fileSearch = FileSearch()
    search = fileSearch.search("../../test_data/", "artist", "michi")
    for f in search:
        print(f)
