from flask import Flask, request, Response
from flask_mysqldb import MySQL
from utils import Stream
from dotenv import load_dotenv
import os

class FlaskApp:

    def __init__(self, host, user, password, database, chunk_size):
        # create the app
        self.app = Flask(__name__)

        # set up the database configurations
        self.app.config['MYSQL_HOST'] = host
        self.app.config['MYSQL_USER'] = user
        self.app.config['MYSQL_PASSWORD'] = password
        self.app.config['MYSQL_DB'] = database
        self.mysql = MySQL(app)

        # store a chunk size for the streams
        self.chunk_size = chunk_size


    @app.route('/put-file/<string:url>', methods=['PUT'])
    def put_file(self):
        try:
            # create an input stream with a chunk size of chunk size to
            # memory usage minimize
            input_stream = Stream(url, self.chunk_size)
            sql_cursor = self.mysql.connection.cursor()
            for chunk in input_stream:
                if(chunk):
                    for word in chunk.decode("utf-8").split("\n"):
                        sql_cursor.execute(
                            "INSERT IGNORE INTO words(word) VALUES (%s)",
                            (word))
                self.mysql.connection.commit()
            sql_cursor.close()
            return "success"
        except Exception as e:
            return e

    @app.route('/get-file', methods=['GET'])
    def get_file(self):
        result = "Error, invalid request"
        return Response(get_words())

    def get_words(self):
        cur_idx = 0
        try:
            while True:
                sql_cursor = self.mysql.connection.cursor()
                sql_cursor.execute(f"SELECT word FROM words LIMIT {cur_idx},"
                                   f"{self.chunk_size}")
                row = [word for word in sql_cursor.fetchall()]
                if len(row) == 0:
                    break
                cur_idx += self.chunk_size
                yield row
        except Exception as e:
            return


if __name__ == "__main__":
    load_dotenv()
    db_host = os.getenv('HOST')
    db_user = os.getenv('USER')
    db_password = os.getenv('PASSWORD')
    db_name = os.getenv('NAME')
    chunk_size = os.getenv('CHUNK_SIZE')
    currentApp = FlaskApp(db_host, db_user, db_password, name, chunk_size)
    currentApp.app.run()
