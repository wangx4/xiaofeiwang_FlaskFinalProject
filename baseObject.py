import pymysql, json

import config


class baseObject:
    def setupObject(self, tn):
        self.tn = tn
        self.fnl = []
        self.required_fields = []  # info needed when insert
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
            if row['Null'] == 'NO' and row[
                    'Extra'] != 'auto_increment' and row['Default'] == None:
                self.required_fields.append(row['Field'])

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
        #print(tokens)
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

    def insert(self, data):
        """insert table with data"""
        if not all(required_field in data
                   for required_field in self.required_fields):
            print(f"data must contains {self.required_fields}")
            return
        tokens = []
        for field in self.required_fields:
            tokens.append(data[field])

        vals = ['%s'] * len(self.required_fields)
        vals = ','.join(vals)
        cols = map(lambda fieldname: '`' + fieldname + '`',
                   self.required_fields)
        cols = ','.join(cols)

        sql = 'INSERT INTO `' + self.tn + '` (' + cols + ') VALUES (' + vals + ');'
        #self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        self.log(sql, tokens)
        cur.execute(sql, tokens)
        #self.data[n][self.pk] = cur.lastrowid
        return cur.lastrowid

    def update(self, data):
        if self.pk not in data:
            print("pk is required")
            return
        new_vals = dict()
        for field in self.required_fields:
            if field in data:
                new_vals[field] = data[field]
        if len(new_vals) == 0:
            print("no new vals to update")
            return
        setstring = ''
        tokens = []
        for fieldname, val in new_vals.items():
            setstring += ' `' + fieldname + '` = %s,'
            tokens.append(val)
        setstring = setstring[:-1]
        tokens.append(data[self.pk])

        sql = 'UPDATE `' + self.tn + '` SET ' + setstring + ' WHERE `' + self.pk + '` = %s;'

        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        print(sql)
        print(tokens)
        self.log(sql, tokens)
        cur.execute(sql, tokens)

    def log(self, sql, tokens=None):
        if tokens == None:
            tokens = []
        f = open('logs/sql_log.txt', 'a')
        import datetime
        now = datetime.datetime.now()
        debug_str = str(now) + ' - ' + sql + json.dumps(tokens) + '\n'
        f.write(debug_str)
        f.close()