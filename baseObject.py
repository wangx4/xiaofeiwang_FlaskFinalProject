import pymysql, json

import config


class baseObject:
    def setupObject(self, tn):
        self.tn = tn
        self.fnl = []
        self.pk = ''
        self.conn = self.connect()
        self.errorList = []
        self.getFields()

    def connect(self):
        return pymysql.connect(host=config.DB['host'],
                               port=config.DB['port'],
                               user=config.DB['user'],
                               passwd=config.DB['passwd'],
                               db=config.DB['db'],
                               autocommit=True)

    def getFields(self):
        sql = 'DESCRIBE `' + self.tn + '`;'
        # self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql)
        self.fnl = []
        for row in cur:
            print(row)
            self.fnl.append(row['Field'])
            if row['Key'] == 'PRI':
                self.pk = row['Field']

    def getById(self, id):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + self.pk + '` = %s;'
        tokens = (id)
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        print(sql)
        print(tokens)
        self.log(sql, tokens)
        cur.execute(sql, tokens)
        #elf.data = []
        xs = []
        for row in cur:
            #self.data.append(row)
            xs.append(row)
        return xs

    def getAll(self, order=None):
        sql = 'SELECT * FROM `' + self.tn + '` '
        if order != None:
            sql += ' ORDER BY `' + order + '`'
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        self.log(sql)
        cur.execute(sql)
        #self.data = []
        xs = []
        for row in cur:
            #self.data.append(row)
            xs.append(row)
        return xs

    def deleteById(self, id):
        sql = 'DELETE FROM `' + self.tn + '` WHERE `' + self.pk + '` = %s;'
        tokens = (id)
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        self.log(sql, tokens)
        cur.execute(sql, tokens)

    def getByField(self, field, value):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + field + '` = %s;'
        tokens = (value)
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        self.log(sql, tokens)
        cur.execute(sql, tokens)
        #self.data = []
        xs = []
        for row in cur:
            #self.data.append(row)
            xs.append(row)
        return xs

    def getLikeField(self, field, value):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `' + field + '` LIKE %s;'
        tokens = ('%' + value + '%')
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        cur.execute(sql, tokens)
        #self.data = []
        xs = []
        for row in cur:
            #self.data.append(row)
            xs.append(row)
        return xs

    def log(self, sql, tokens=[]):
        f = open('logs/sql_log.txt', 'a')
        import datetime
        now = datetime.datetime.now()
        debug_str = str(now) + ' - ' + sql + json.dumps(tokens) + '\n'
        f.write(debug_str)
        f.close()