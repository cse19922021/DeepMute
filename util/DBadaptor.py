import sqlite3


class DBHandler:
    def __init__(self, create_flag) -> None:
        self.create_flag = create_flag
        self.conn = sqlite3.connect('mutation_database.db', check_same_thread=False)
        self.c = self.conn.cursor()
        if self.create_flag:
            create_query = 'CREATE TABLE IF NOT EXISTS mutationTable(mutId Int,start_line String, end_line String, potentialLine Text, mutatedLine Text, methodBody Text, mutationKind Text, Faddress Text, status Int, mstatus Text)'
            self.c.execute(create_query)
        else:
            self.conn = sqlite3.connect('mutation_database.db', check_same_thread=False)
            self.c = self.conn.cursor()
                

    def insert_data(self, mId, start_line, end_line, potentialLine, mutatedLine, methodBody, mutationKind, file_addr, mstatus):
        insert_query = "INSERT INTO mutationTable VALUES (" + "'" + str(mId) + "'" + "," + "'" + str(
            start_line) + "'" + "," + "'" + str(end_line) + "'" + "," + "'"+ potentialLine + "'" + "," + "'" + mutatedLine + "'" + "," + "'" + methodBody + "'" + "," + "'" + mutationKind + "'" + "," + "'" + file_addr + "'" + "," + "'" + str(0) + "'" + "," + "'" + mstatus + "'" + ")"

        try:
            self.c.execute(insert_query)
            self.conn.commit()
        except sqlite3.Error as ee:
            print('SQLite error: %s' % (' '.join(ee.args)))

    def read_data(self):
        read_query = 'SELECT * FROM mutationTable'
        return self.c.execute(read_query)

    def delete_table(self):
        drop_query = 'DROP TABLE mutationTable'
        self.c.execute(drop_query)
    
    def delete_null(self):
        q = 'DELETE from mutationTable where potentialLine is null'
        self.c.execute(q)
        self.conn.commit()

    def update(self, mutId, newStatus):
        self.c.execute(
            '''UPDATE mutationTable SET status = ? WHERE mutId = ?''', (newStatus, mutId))
        self.conn.commit()

    def updateMstatus(self, mutId, newStatus):
        self.c.execute(
            '''UPDATE mutationTable SET mstatus = ? WHERE mutId = ?''', (newStatus, mutId))
        self.conn.commit()

    def updateMutatedLine(self, mutId, mutatedLine):
        self.c.execute(
            '''UPDATE mutationTable SET mutatedLine = ? WHERE mutId = ?''', (mutatedLine, mutId))
        self.conn.commit()

    def filter_table(self):
        mutation_list = []
        cursor_obj = self.read_data()
        for row in cursor_obj:
            mutation_list.append(row)
        return mutation_list


def main():
    db_handler = DBHandler()
    ds_list = db_handler.filter_table()
    for i in range(len(ds_list)):
        print(ds_list[i])


if __name__ == "__main__":
    main()