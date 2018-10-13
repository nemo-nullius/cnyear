import re
import sys
import sqlite3

def debug(foo):
    print(foo)

class Cnyeardb(object):
    def __init__(self, dbpath="./cnyeardb.db"):
        self.sqlbase = '''SELECT 
            tb_regnal_postq.id,
            tb_dynasty_c1_postq.name,
            tb_dynasty_c1_postq.alias,
            tb_dynasty_c2_postq.name,
            tb_dynasty_c2_postq.alias,
            tb_dynasty_postq.name,
            tb_dynasty_postq.alias,
            tb_emperor_postq.name,
            tb_emperor_postq.temple_name,
            tb_emperor_postq.alias,
            tb_regnal_postq.regnal,
            tb_regnal_postq.alias,
            tb_regnal_postq.ya,
            tb_regnal_postq.yz
            FROM tb_regnal_postq
            LEFT JOIN tb_dynasty_postq ON tb_regnal_postq.dynasty_id = tb_dynasty_postq.id
            LEFT JOIN tb_emperor_postq ON tb_regnal_postq.emperor_id = tb_emperor_postq.id
            LEFT JOIN tb_dynasty_c1_postq ON tb_dynasty_postq.c1_id = tb_dynasty_c1_postq.id
            LEFT JOIN tb_dynasty_c2_postq ON tb_dynasty_postq.c2_id = tb_dynasty_c2_postq.id
            '''
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None
        try:
            self.conn = sqlite3.connect(dbpath)
            self.c = self.conn.cursor()
            self.conn.create_function("REGEXP",2,regexp)
        except Error as e:
            print(e)
            sys.exit(-1)

    def mksqlcmd_dnst(self,d,da='',d1='',d1a='',d2='',d2a=''):
        if not d: return None
        sqld = ''
        sqld1 = ''
        sqld2 = ''
        if d or da:
            if d:
                sqld = "tb_dynasty_postq.name='%s'" %d
            if da:
                sqld += " OR " if d else ""
                sqld += "tb_dynasty_postq.alias REGEXP '%s'" %da
        if sqld: sqld = "(%s)" %sqld
        if d1 or d1a:
            if d1:
                sqld1 = "tb_dynasty_c1_postq.name='%s'" %d1
            if d1a:
                sqld1 += " OR " if d1 else ""
                sqld1 += "tb_dynasty_c1_postq.alias REGEXP '%s'" %d1a
        if sqld1: sqld1 = "(%s)" %sqld1
        if d2 or d2a:
            if d2:
                sqld2 = "tb_dynasty_c2_postq.name='%s'" %d2
            if d2a:
                sqld2 += " OR " if d2 else ""
                sqld2 += "tb_dynasty_c2_postq.alias REGEXP '%s'" %d2a
        if sqld2: sqld2 = "(%s)" %sqld2
        # sqld must not be none
        sqlcmd = sqld
        if sqld1: sqlcmd = "%s AND %s" %(sqlcmd,sqld1)
        if sqld2: sqlcmd = "%s AND %s" %(sqlcmd,sqld2)
        debug(sqlcmd)
        return sqlcmd

    def mksqlcmd_rgnl(self, d, rgnl, rgnla='', da='', d1='', d1a='', d2='', d2a=''):
        if not rgnl: return None
        sqlcmd_dnst = self.mksqlcmd_dnst(d=d,da=da,d1=d1,d1a=d1a,d2=d2,d2a=d2a)
        s = "tb_regnal_postq.regnal='%s'" %rgnl
        s += " OR tb_dynasty_c2_postq.alias REGEXP '%s'" %rgnla if rgnla else ""
        s = "(%s)" %s
        sqlcmd = sqlcmd_dnst + ' AND ' + s
        return sqlcmd

    def lkp_rgnl(self, d, rgnl, rgnla='', da='', d1='', d1a='', d2='', d2a=''):
        sqlcmd = self.mksqlcmd_rgnl(d=d,rgnl=rgnl,rgnla=rgnla,da=da,d1=d1,d1a=d1a,d2=d2,d2a=d2a)
        sqlcmd = self.sqlbase + "WHERE " + sqlcmd
        self.c.execute(sqlcmd)
        return self.c.fetchall()

    def lkp_dnst(self, d, da='', d1='', d1a='', d2='', d2a=''):
        sqlcmd = self.mksqlcmd_dnst(d=d,da=da,d1=d1,d1a=d1a,d2=d2,d2a=d2a)
        sqlcmd = self.sqlbase + "WHERE " + sqlcmd
        self.c.execute(sqlcmd)
        return self.c.fetchall()

if __name__ == '__main__':
    cnyeardb_handler = Cnyeardb()
    print(cnyeardb_handler.lkp_dnst('清',r'\b清\b',d1='後金·清'))
    print(cnyeardb_handler.lkp_rgnl('清','天聰',da=r'\b清\b'))


