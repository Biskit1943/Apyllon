import glob
import os
import taglib

from config import Config


class FileSearch():
    """
    Class for searching for specific file formats in the filesystem.
    """
    def __init__(self):
        """
        Attributes:
            formats (dict): Dictonary of the fileendings to search for, specified in the
                            config.py in the root folder.
        """
        self.formats = Config.SONG_EXTENSIONS

    def search(self, path, *args):
        """
        Search recursive throught a folder, extract path, filename, lenght and 
        meta informations.
        Generates a dict for each mathing file including above information. 
        This Method is a Python Generator

        Args:
            path (string): The path to the folder to be searched
            *args (string): Fields to append to meta information dict.
                   If correspnding information was not included in the file, 
                   the missing keys will be added with a None value.

        Yields (dict):
            One dict for every mathing File with the following keys:
                path: absolute path to the File
                filename: name of the file
                lenght: playtime of audio or video file
                meta: all information that could been red from taglib,
                      plus all fields given by *args set to None.

        """
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
