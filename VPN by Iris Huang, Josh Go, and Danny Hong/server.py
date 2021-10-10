from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import mysql.connector
from mysql.connector import MySQLConnection, Error
import json


class GP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        params = parse_qs(self.path[2:])
        user = params["user"][0]
        try:
            # TODO To run the program, please change the user and password value
            conn = mysql.connector.connect(host="localhost", user='****', password='******')
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS user_messages")
            cursor.execute("USE user_messages")
            tableCheck = "CREATE TABLE IF NOT EXISTS " + user + " (sender TEXT, value TEXT, time TEXT)"
            cursor.execute(tableCheck)
            select_query = "SELECT * FROM " + user
            cursor.execute(select_query)
            data = cursor.fetchall()
            row_headers = [x[0] for x in cursor.description]
            messages = []
            for row in data:
                messages.append(dict(zip(row_headers, row)))
            result = {
                "response": {
                    "user": user,
                    "messages": messages
                }}
        except Error as error:
            print(error)
        finally:
            cursor.close()
            conn.close()
        self.wfile.write(json.dumps(result).encode('utf_8'))

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers.get('Content-Length'))
        form = json.loads(self.rfile.read(content_len).decode('utf-8'))
        receiver = form["receiver"]
        insert_query = ("INSERT INTO " + receiver +
                        " (sender, value, time) "
                        "VALUES (%(sender)s, %(value)s, %(time)s)")
        try:
            # TODO To run the program, please change the user and password value
            db = mysql.connector.connect(host="localhost", user='*****', password='******')
            cursor2 = db.cursor()
            cursor2.execute("CREATE DATABASE IF NOT EXISTS user_messages")
            cursor2.execute("USE user_messages")
            checker = "CREATE TABLE IF NOT EXISTS %s (sender TEXT, value TEXT, time TEXT)" %(receiver)
            cursor2.execute(checker)
            cursor2.execute(insert_query, form)
            db.commit()
        except Error as error:
            print(error)
        finally:
            cursor2.close()
            db.close()
        self.wfile.write("<html><body><h1>POST Request Received!</h1></body></html>")


def main(server_class=HTTPServer, handler_class=GP, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server running at localhost:80...'
    httpd.serve_forever()

if __name__ == '__main__':
    main()
