import log
import pymysql
import datetime
import json
import const
import utils

log = log.logging.getLogger(__name__)


class Database(object):
    conn = {}
    def __init__(self):
        # log.info(const.DB_PORT)
        # log.info(const.DB_HOST)
        # log.info(const.DB_ACCOUNT)
        # log.info(const.DB_PASSWORD)
        conn = pymysql.Connect(host=const.DB_HOST, port=int(const.DB_PORT), user=const.DB_ACCOUNT, passwd=const.DB_PASSWORD, db='btc',charset='utf8')
        self.conn = conn

    def getMessage(self,data):
        cursor = self.conn.cursor()
        try:
            if data == None:
                cursor.execute("select * from `btc`.`message` where `isdisplay`='1' order by `init_time`;")
            elif data.get("name") != None:
                cursor.execute("select * from `btc`.`message` where name = %s;", (data.get('name')))
            elif data.get("id") != None:
                cursor.execute("select * from `btc`.`message` where id = %s;", (data.get('id')))
            elif data.get("isdisplay") != None:
                cursor.execute("select * from `btc`.`message` where `isdisplay`in ('0','1') order by `init_time`;")
            else:
                cursor.execute("select * from `btc`.`message` where `isdisplay`='1' order by `init_time`;")
            data = []
            for row in cursor.fetchall():
                obj = {}
                for i, value in enumerate(row):
                    log.debug(cursor.description[i][0] + ':'+ str(value))
                    obj[cursor.description[i][0]]= value.strftime("%Y/%m/%d %H:%M:%S") if type(value) is datetime.date else str(value)
                data.append(obj)
            # r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            return data
        except Exception as e:
            log.info( "getMessage error: " + cursor._executed)
            log.info(utils.except_raise(e))
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def addMessage(self,data):
        cursor = self.conn.cursor()
        sql = "insert into btc.message (name, init_time, message) values( %s, now(), %s )"
        val = (data.get('name'), data.get('message'))
        log.info(val)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            return True
        except Exception as e:
            log.info("query '{}' with params {} failed with {}".format(sql, val, e))
            log.info(cursor._executed)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def editMessage(self,data):
        cursor = self.conn.cursor()
        sql = "UPDATE btc.message SET isdisplay = %s where id = %s"
        val = (data.get('isdisplay'), data.get('id'))
        log.info(val)
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            return True
        except Exception as e:
            log.info("query '{}' with params {} failed with {}".format(sql, val, e))
            log.info(cursor._executed)
            self.conn.rollback()
            raise e
        finally:
            cursor.close()
            self.conn.close()

    def delMessage(self,data):
        cursor = self.conn.cursor()
        sql = "DELETE FROM btc.message WHERE id = %s"
        val = (data.get('id'))
        try:
            cursor.execute(sql, val)
            self.conn.commit()
            log.info(cursor.rowcount)
            return True
        except Exception as e:
            log.info( "delMessage error: " + cursor._executed)
            raise e
        finally:
            cursor.close()
            self.conn.close()