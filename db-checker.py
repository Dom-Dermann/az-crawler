import sqlite3

def check_rows():
    connection = sqlite3.connect("crawler.db")
    cursor = connection.cursor()

    sql_command = """
    SELECT * FROM params
    """

    cursor.execute(sql_command)
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    connection.close()

if __name__ == "__main__":
    check_rows()