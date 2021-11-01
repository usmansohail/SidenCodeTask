# SidenCodeTask
Implementation of Siden Fullstack Coding Task

## Description:
We have a file (can be a very large file (up to 100 GB)), which contains a lot
of words and each word is on a new line (file sample -
https://drive.google.com/file/d/1mmFQVmWJT4entvG5OVOSxcG_uT9XUSAa/view?usp=sharing)


## Requirements:

1) Implement "PUT" HTTP endpoint which will save/replace file on the disk
2) Implement "GET "HTTP endpoint which will return "processed" file without
word duplicates
3) Implementation must run in 8GB of RAM. Assume that you will not have enough
memory to fit the entirety of the file in memory


## Architecture
I chose to use a simple MySQL database to store all the words of the file and a
streaming mechanism to ensure both the PUT and GET requests do not require too
much memory, regardless of the file size. When I first read the prompt, my
initial thought was to use some sort of map. However, given that the file may
get up-to a 100Gb, and there is no restriction on the words, we could end up
having completely unique words in the original file making the processed file
also 100Gb in size. Although a distributed map would be possible to implement,
I felt that a simple MySQL database would get the job done as it allows batch
queries.

Given that the file uploaded can be up-to 100 Gb, the PUT request does not take
the file itself as a parameter, but rather a url pointing to the file. This way
we can stream the file in smaller chunks. The chunk size I chose for now was
1024 although this can easily be changed with the current implementation. So
the system only needs to hold a maximum of 1024 words in memory at any given
time. The GET request has a similar batch architecture. The query only grabs
up-to 1024 entries into memory at a given time and streams them over http to the
end user. 

## complexity
###  runtime
The runtime complexity for the put is O(n) where n is the number of total words
including duplicates in the file uploaded by the user. Each word is only
processed once. 
### space
The space complexity is O(m) where m is the total number of unique words. Only
unique words are persisted in memory. Due to the batch processing, only a
constant amount of memory is used per each batch. 


## Additional Considerations
* the requirements only asked for PUT and GET, but a POST could have easily
	been implemented that combined files. 
* although I did not test this on an 8Gb machine, this method should work,
	albiet slowly for a file that is 100Gb in size. 
* additional constraints could be set on the MySQL buffers themselves to ensure
	too much memory is never used.
* a NOSQL database could also be used, but given the structure is quite simple,
	and joins of any kind would never be required, a sql database handles the job
* in a production setup, I would have stress tested  the system, but for now I
	only tested  the basics in the test directory
