from urllib.request import Request, urlopen
import mmap


class Stream:

    def __init__(self, url):
        self.url = url
        self.f = open('tmpFile.zip', 'wb')
        self.f.write(b'\0')
        self.f.close()
        self.f = open('tmpFile.zip', 'r+b')
        self.mmaped_file_as_string = mmap.mmap(self.f.fileno(), 0,
                                          access=mmap.ACCESS_READ)

        # perform request
        request = Request(url, self.mmaped_file_as_string)
        request.add_header("Content-Type", "application/zip")
        self.response = urlopen(request)

    def close(self):
        self.mmaped_file_as_string.close()
        self.f.close()


    def readResponse(self):
        return self.response.read().decode()




stream = Stream(
    "https://drive.google.com/uc?id=1mmFQVmWJT4entvG5OVOSxcG_uT9XUSAa")
for word in stream.mmaped_file_as_string:
    print(word)

print(stream.readResponse())
