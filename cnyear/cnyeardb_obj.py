import re
import os
import sys
import sqlite3
from . import CNYEARDB_PATH

class Cnyeardb(object):
    def __init__(self, dbpath=CNYEARDB_PATH,debug=False):
        if debug:
            self.debugger = self.debugger_t
        else:
            self.debugger = self.debugger_f
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
        self.regp_dnst = self.mkregp_dnst()
        self.regp_rgnl = self.mkregp_rgnl()
        self.recpl_dnst = re.compile(self.regp_dnst)
        self.recpl_rgnl = re.compile(self.regp_rgnl)

    def debugger_t(self, foo):
        print(foo)
    def debugger_f(self, foo):
        pass

    def setdebug(self):
        self.debugger = self.debugger_t
    def unsetdebug(self):
        self.debugger = self.debugger_f

    def lkp_year(self, year):
        sqlcmd = self.sqlbase + 'WHERE (tb_regnal_postq.ya <= %s) AND (tb_regnal_postq.yz >= %s)' %(year, year)
        self.c.execute(sqlcmd)
        return self.c.fetchall()

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
        self.debugger(sqlcmd)
        return sqlcmd

    def mksqlcmd_rgnl(self, d, rgnl, rgnla='', da='', d1='', d1a='', d2='', d2a=''):
        if not rgnl: return None
        sqlcmd_dnst = self.mksqlcmd_dnst(d=d,da=da,d1=d1,d1a=d1a,d2=d2,d2a=d2a)
        s = "tb_regnal_postq.regnal='%s'" %rgnl
        s += " OR tb_dynasty_c2_postq.alias REGEXP '%s'" %rgnla if rgnla else ""
        s = "(%s)" %s
        sqlcmd = sqlcmd_dnst + ' AND ' + s
        self.debugger(sqlcmd)
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

    def mkregp_dnst(self):
        try:
            if self.regp_dnst: return self.regp_dnst # AttributeError then do the following
        except:
            pass
        self.c.execute('''SELECT name, alias FROM tb_dynasty_postq''')
        sqlrd = self.c.fetchall()
        self.c.execute('''SELECT name, alias FROM tb_dynasty_c1_postq''')
        sqlrd1 = self.c.fetchall()
        self.c.execute('''SELECT name, alias FROM tb_dynasty_c2_postq''')
        sqlrd2 = self.c.fetchall()
        exprd = []
        exprd1 = []
        exprd2 = []
        for t in sqlrd:
            exprd.append(t[0])
            exprd += t[1].split(' ') if t[1] else []
        for t in sqlrd1:
            exprd1.append(t[0])
            exprd1 += t[1].split(' ') if t[1] else []
        for t in sqlrd2:
            exprd2.append(t[0])
            exprd2 += t[1].split(' ') if t[1] else []
        expr = '(%s)?(%s)?(%s)' %('|'.join(exprd1),'|'.join(exprd2),'|'.join(exprd))
        self.debugger(expr)
        return expr

    def mtch_dnst(self, s):
        m = self.recpl_dnst.search(s)
        if not m: return None
        return [m.group(1),m.group(2),m.group(3)]

    def mkregp_rgnl(self):
        try:
            if self.regp_rgnl: return self.regp_rgnl # AttributeError then do the following
        except:
            pass
        self.c.execute('''SELECT name, alias FROM tb_dynasty_postq''')
        sqlrd = self.c.fetchall()
        self.c.execute('''SELECT name, alias FROM tb_dynasty_c1_postq''')
        sqlrd1 = self.c.fetchall()
        self.c.execute('''SELECT name, alias FROM tb_dynasty_c2_postq''')
        sqlrd2 = self.c.fetchall()
        self.c.execute('''SELECT regnal, alias FROM tb_regnal_postq''')
        sqlrr = self.c.fetchall()
        exprd = []
        exprd1 = []
        exprd2 = []
        exprr = []
        for t in sqlrd:
            exprd.append(t[0])
            exprd += t[1].split(' ') if t[1] else []
        for t in sqlrd1:
            exprd1.append(t[0])
            exprd1 += t[1].split(' ') if t[1] else []
        for t in sqlrd2:
            exprd2.append(t[0])
            exprd2 += t[1].split(' ') if t[1] else []
        for t in sqlrr:
            if t[0]:
                exprr.append(t[0])
            exprr += t[1].split(' ') if t[1] else []
        expr = '(%s)?(%s)?(%s)(%s)' %('|'.join(exprd1),'|'.join(exprd2),'|'.join(exprd),'|'.join(exprr))
        expr += '([元一二三四五六七八九十]+)年'
        self.debugger(expr)
        return expr

    def mtch_rgnl(self, s):
        m = self.recpl_rgnl.search(s)
        if not m: return None
        return [m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)]

