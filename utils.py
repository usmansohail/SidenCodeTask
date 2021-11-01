from urllib.request import Request, urlopen
import requests as req
import mmap


class Stream:

    def __init__(self, url, chunk_size):
        self.url = url
        self.chunk_size = chunk_size
        self.response = req.get(url, stream=True)

    def iterate(self):
        return self.response.iter_content(chunk_size=self.chunk_size)


if __name__ == "__main__":
    # this forms somewhat of a unit test. 
    # TODO: make this into a clean unit test

    stream = Stream(
        "https://raw.githubusercontent.com/usmansohail/SidenCodeTask/main/siden_coding_test_file_sample.txt",
        1024)
    for chunk in stream.iterate():
        if(chunk):
            for word in chunk.decode("utf-8").split("\n"):
                print(word)
