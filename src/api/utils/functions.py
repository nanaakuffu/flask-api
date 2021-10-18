import os
from random import randint
from string import ascii_letters, digits


class Helpers():

    def randomize(length: int = 16) -> str:
        randomString = ''

        source_string = ascii_letters+digits
        size = len(source_string)-1

        while len(randomString) < length:
            randomString += source_string[randint(0, size)]

        return randomString

    @staticmethod
    def hashString(self, upload_dir: str, folder_name: str, fileName: str = "") -> str:

        if folder_name:
            path = folder_name.rstrip('/')+'/'

        upload_dir = os.path.join(upload_dir, path)

        if not os.path.exists(upload_dir):
            os.mkdir(upload_dir)

        fileString, fileExtension = os.path.splitext(fileName)

        return path+self.randomize(40)+fileExtension
