import glob
import os
import taglib

from config import Config


class FileSearch:
    def __init__(self):
        self.formats = Config.SONG_EXTENSIONS

    def search(self, path, *args):
        for fileFormat in self.formats:
            for fileName in glob.iglob((path + "/**/*" + fileFormat), recursive=True):
                media = {
                    "path": os.path.dirname(fileName),
                    "filename": os.path.basename(fileName)
                }
                tags = taglib.File(fileName)
                media["length"] = tags.length
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
