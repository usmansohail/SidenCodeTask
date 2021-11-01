from flask import Flask, request, Response
import pymysql
from utils import Stream

# create the app
app = Flask(__name__)

# set up the database configurations
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_database = 'words'
chunk_size = 1024

# store a chunk size for the streams
chunk_size = chunk_size

# store the unprocessed file url
file_url = None

def get_db_connection():
    return pymysql.connect(host=db_host,
                          user=db_user,
                          password=db_password,
                          database=db_database,
                          cursorclass=pymysql.cursors.DictCursor)


@app.route('/put-file/', methods=['PUT'])
def put_file():
    global file_url
    url = request.form['url']
    if url != file_url:
        file_url = url
        try:
            # create an input stream with a chunk size of chunk size to
            # minimize memory usage
            input_stream = Stream(url, chunk_size)
            sql_connection = get_db_connection()
            sql_cursor = sql_connection.cursor()

            # drop all the previous entries as the file has changed
            sql_cursor.execute("DELETE FROM word")
            sql_connection.commit()

            # insert every word from the new file
            for chunk in input_stream.iterate():
                if(chunk):
                    for word in chunk.decode("utf-8").split("\n"):
                        if len(word) == 0:
                            continue
                        sql_cursor.execute(
                            "INSERT IGNORE INTO word(word) VALUES (%s)",
                            (word))
                sql_connection.commit()
            sql_cursor.close()
            return "success"
        except Exception as e:
            return str(e)

@app.route('/get-file', methods=['GET'])
def get_file():
    return Response(get_words(), mimetype="multipart/x-mixed-replace; boundary=&")

def get_words():
    cur_idx = 0
    sql_connection = get_db_connection()
    try:
        while True:
            sql_cursor = sql_connection.cursor()
            sql_cursor.execute(f"SELECT * FROM word LIMIT {cur_idx},"
                               f"{chunk_size}")
            words = sql_cursor.fetchall()
            for word in words:
                f_string = f"{word['word']}"
                yield (b'\r\n' + f_string.encode())
            if len(words) == 0:
                break
            cur_idx += chunk_size
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
