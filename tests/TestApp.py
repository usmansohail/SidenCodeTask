import pytest
import requests

base_url = "http://127.0.0.1:5000/"


def assert_correct_counts(correct_count):
    current_count = 0
    get_url = f"{base_url}/get-file"
    s = requests.Session()
    response = s.get(get_url,
                     headers={"content-type":"multipart/x-mixed-replace; boundary=&"},
                     stream=True)
    assert response.status_code == 200
    for line in response.iter_lines():
        if len(line) != 0:
            current_count += 1
    assert current_count == correct_count

'''
Test empty file:
    This file is empty. Test that it in fact adds no words.
'''
def test_empty_file():
    put_url = f"{base_url}/put-file/"
    data_url = \
        "https://raw.githubusercontent.com/usmansohail/SidenCodeTask/main/tests/example_files/empty_file.txt"
    response = requests.put(put_url, data={"url":data_url})
    assert response.status_code == 200
    assert_correct_counts(0)

'''
Ten unique words:
    This test case adds a file with ten unique words, but 23 total lines. This
    test will ensure that words are successfully inserted and also duplicates
    are handled correctly.
'''
def test_ten_unique_words():
    put_url = f"{base_url}/put-file/"
    data_url = \
        "https://raw.githubusercontent.com/usmansohail/SidenCodeTask/main/tests/example_files/ten_unique_words.txt"
    response = requests.put(put_url, data={"url":data_url})
    assert response.status_code == 200
    assert_correct_counts(10)

    # cleanup by putting the empty file again
    test_empty_file()
'''
Special characters:
    This test case adds a file with ten unique special characters, but 23 total
    lines. This test will ensure that words are successfully inserted even
    though they are all special characters.
'''
def test_special_characters():
    put_url = f"{base_url}/put-file/"
    data_url = \
        "https://raw.githubusercontent.com/usmansohail/SidenCodeTask/main/tests/example_files/special_chars.txt"
    response = requests.put(put_url, data={"url":data_url})
    assert response.status_code == 200
    assert_correct_counts(10)

    # cleanup by putting the empty file again
    test_empty_file()

def test_put_provided_file():
    put_url = f"{base_url}/put-file/"
    data_url = \
        "https://raw.githubusercontent.com/usmansohail/SidenCodeTask/main/tests/example_files/siden_coding_test_file_sample.txt"
    response = requests.put(put_url, data={"url":data_url})
    assert response.status_code == 200
    assert_correct_counts(3023)

    # cleanup by putting the empty file again
    test_empty_file()
