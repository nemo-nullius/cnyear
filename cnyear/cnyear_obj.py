import re

from .cn2dig import cn2dig
from .dig2cn import dig2cn
from .cnyeardb_obj import Cnyeardb
# TODO
# 1. y2cny(): what if two cn years refer to the same year? eg. 明崇禎十七年 清順治二年

class Cnyear(object):
    def __init__(self,cnyear):
        self.cnyear = cnyear
        '''
        seven kinds of cnyear:
        cnyear: 清道光十二年/清道光12年/清道光間/民國元年/民國1年/民國間/一九五〇年/1950年
        '''
        self.cnyeardb_handler = Cnyeardb()
        pq0 = self.cnyeardb_handler.mkregp_rgnl()
        pq1 = pq0.replace(r'元一二三四五六七八九十',r'0-9')
        pq2 = pq0.replace(r'([元一二三四五六七八九十]+)年',r'間')
        pm0 = r'民國([元一二三四五六七八九十]+)年'
        pm1 = r'民國([0-9]+)年'
        pm2 = r'民國間'
        pce0 = r'([〇零一二三四五六七八九]+)'
        pce1 = r'([\d+]+)'
        cq0 = re.compile(pq0)
        cq1 = re.compile(pq1)
        cq2 = re.compile(pq2)
        cm0 = re.compile(pm0)
        cm1 = re.compile(pm1)
        cm2 = re.compile(pm2)
        cce0 = re.compile(pce0)
        cce1 = re.compile(pce1)

        self.cnyear_kind = ''
        self.cnyear_m = None
        self.cnyear_realkind = None # will be set in y2cny
        if cq0.search(cnyear):
            self.cnyear_m = cq0.search(cnyear)
            self.cnyear_kind = 'q0'
        elif cq1.search(cnyear):
            self.cnyear_m = cq1.search(cnyear)
            self.cnyear_kind = 'q1'
        elif cq2.search(cnyear):
            self.cnyear_m = cq2.search(cnyear)
            self.cnyear_kind = 'q2'
        elif cm0.search(cnyear):
            self.cnyear_m = cm0.search(cnyear)
            self.cnyear_kind = 'm0'
        elif cm1.search(cnyear):
            self.cnyear_m = cm1.search(cnyear)
            self.cnyear_kind = 'm1'
        elif cm2.search(cnyear):
            self.cnyear_m = cm2.search(cnyear)
            self.cnyear_kind = 'm2'
        elif cce0.search(cnyear):
            self.cnyear_m = cce0.search(cnyear)
            self.cnyear_kind = 'ce0'
        elif cce1.search(cnyear):
            self.cnyear_m = cce1.search(cnyear)
            self.cnyear_kind = 'ce1'

    def get_year_component(self):
        if self.cnyear_kind == 'q0' or self.cnyear_kind == 'q1':
            return (self.cnyear_kind, self.cnyear_m.group(3),self.cnyear_m.group(4),self.cnyear_m.group(5))
        if self.cnyear_kind == 'q2':
            return (self.cnyear_kind, self.cnyear_m.group(3),self.cnyear_m.group(4),'間')
        if self.cnyear_kind == 'm0' or self.cnyear_kind == 'm1':
            return (self.cnyear_kind, '民國',None,self.cnyear_m.group(1))
        if self.cnyear_kind == 'm2':
            return (self.cnyear_kind, '民國',None,'間')
        if self.cnyear_kind == 'ce0' or self.cnyear_kind == 'ce1':
            return (self.cnyear_kind, 'ce',None,self.cnyear_m.group(1))

    def get_year_offset(self, dig=False, conv_1=False):
        '''To get year offset, without '年' behind
        清光緒二十年 二十
        清乾隆元年 元
        清光緒二十年 20
        清乾隆元年 1
        民國間 間
        一九八九年 一九八九'''
        if self.cnyear_kind[-1] != '2': # not '間'
            offset = self.get_year_component()[3]
            if not dig:
                if self.cnyear_kind[:-1] != 'ce':
                    return self.__year_dig2cn(offset+'年', ce=False)[:-1]
                else: # ce
                    return self.__year_dig2cn(offset+'年', ce=True)[:-1]
            else: # dig
                if self.cnyear_kind[:-1] != 'ce':
                    return self.__year_cn2dig(offset+'年', ce=False, conv_1=conv_1)[:-1]
                else: # ce
                    return self.__year_cn2dig(offset+'年', ce=True)[:-1]
        else:
            return '間'




    def cny2y(self):
        '''deprecated, use cny2y_safe instead'''
        if self.cnyear_kind == 'q0':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            #TODO: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            yoffset_ch = self.cnyear_m.group(5)
            if yoffset_ch == '元':
                yoffset = 1
            else:
                yoffset = cn2dig(yoffset_ch)
            return (ya+yoffset-1, None)
        if self.cnyear_kind == 'q1':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            #TODO: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            yoffset = int(self.cnyear_m.group(5))
            return (ya+yoffset-1, None)
        if self.cnyear_kind == 'q2':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            #Todo: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            return (ya,yz)
        if self.cnyear_kind == 'm0':
            yoffset_ch = self.cnyear_m.group(1)
            if yoffset_ch == '元':
                yoffset = 1
            else:
                yoffset = cn2dig(yoffset_ch)
            return (1911+yoffset, None)
        if self.cnyear_kind == 'm1':
            yoffset_ch = self.cnyear_m.group(1)
            yoffset = int(yoffset_ch)
            return (1911+yoffset, None)
        if self.cnyear_kind == 'm2':
            return (1912, 1949)
        if self.cnyear_kind == 'ce0':
            ych = self.cnyear_m.group(1)
            return (int(''.join([str(cn2dig(x)) for x in ych])),None) #一九五九年
        if self.cnyear_kind == 'ce1':
            ych = self.cnyear_m.group(1)
            return (int(ych), None)
        return (None, None)

    def cny2y_safe(self):
        '''
        return (ya,yz,check)
        if check == false: this regnal year is not correct
        else: this regnal year is correct (before yz)
        ya == None: no result get
        yz == None: not a span of time 間
        check == None: a span of time 間, or for CE, or NO RESULT
        '''
        if self.cnyear_kind == 'q0':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            if not lyear: return (None, None, None)
            #TODO: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            yoffset_ch = self.cnyear_m.group(5)
            if yoffset_ch == '元':
                yoffset = 1
            else:
                yoffset = cn2dig(yoffset_ch)
            intyear = ya+yoffset - 1
            if intyear <= yz:
                ycheck = True
            else:
                ycheck = False
            return (intyear, None, ycheck)
        if self.cnyear_kind == 'q1':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            if not lyear: return (None, None, None)
            #TODO: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            yoffset = int(self.cnyear_m.group(5))
            intyear = ya+yoffset - 1
            if intyear <= yz:
                ycheck = True
            else:
                ycheck = False
            return (intyear, None, ycheck)
        if self.cnyear_kind == 'q2':
            d = self.cnyear_m.group(3)
            rgnl = self.cnyear_m.group(4)
            lyear = self.cnyeardb_handler.lkp_rgnl(d, rgnl)
            if not lyear: return (None, None, None)
            #Todo: if many results
            ya = int(lyear[0][12])
            yz = int(lyear[0][13])
            return (ya,yz, None)
        if self.cnyear_kind == 'm0':
            yoffset_ch = self.cnyear_m.group(1)
            if yoffset_ch == '元':
                yoffset = 1
            else:
                yoffset = cn2dig(yoffset_ch)
            intyear = 1911+yoffset
            if intyear <= 1949:
                ycheck = True
            else:
                ycheck = False
            return (intyear, None, ycheck)
        if self.cnyear_kind == 'm1':
            yoffset_ch = self.cnyear_m.group(1)
            yoffset = int(yoffset_ch)
            intyear = 1911+yoffset
            if intyear <= 1949:
                ycheck = True
            else:
                ycheck = False
            return (intyear, None, ycheck)
        if self.cnyear_kind == 'm2':
            return (1912, 1949, None)
        if self.cnyear_kind == 'ce0':
            ych = self.cnyear_m.group(1)
            return (int(''.join([str(cn2dig(x)) for x in ych])),None,None) #一九五九年
        if self.cnyear_kind == 'ce1':
            ych = self.cnyear_m.group(1)
            return (int(ych), None, None)
        return (None, None, None)

    def y2cny(self, dig=False, ldefaultdy=['清','明']):
        ''' convert year to cny 
        # OUTPUT RULE
        if intyear >= 1950: ALL to CE
        if intyear = 1949: if original year is 民國 then 民國, else CE
        if intyear in [1912, 1949): ALL to 民國 （***NOT TO CE***)
        if intyear in (xxx, 1912): 
            if original year is correct, then original one; 
            else the correct one according to ldefaultydy or the last tyear in lyear
        # SOME HINTS
        0. xx 間 no changes
        1. >= 1950 CE
        2. in [1912, 1949) 民國
        3. ==1949 original 民國 then 民國, else CE (i.e. default CE)
        4. ldefaultydy ONLY takes effect when in (xxx, 1912) AND the original regnal year is UNCORRECT 
        '''
        if self.cnyear_kind == 'q2' or self.cnyear_kind == 'm2': #xx間
            self.cnyear_realkind = self.cnyear_kind[:-1]
            return self.cnyear
        intyear,yz,check = self.cny2y_safe()
        if not intyear:
            return None
        if intyear >= 1950: # all to CE 
            self.cnyear_realkind = 'ce'
            if dig: return str(intyear)+'年'
            else: return ''.join(dig2cn(x) for x in str(intyear))+'年'
        elif intyear == 1949: # originally 民國 then 民國, else 1949
            if self.cnyear_kind == 'm0' or self.cnyear_kind == 'm1':
                self.cnyear_realkind = 'm'
                if dig: return '民國38年'
                else: return '民國三十八年'
            else:
                self.cnyear_realkind = 'm'
                if dig: return '1949年'
                else: return '一九四九年'
        elif intyear >= 1912: # all to 民國
            self.cnyear_realkind = 'm'
            y_offset = intyear - 1911
            if y_offset == 1:
                if dig: return '民國元年'
                else: return '民國元年'
            else:
                if dig: return '民國%s年' %y_offset
                else: return '民國%s年' %dig2cn(y_offset)
        else: # all to REGNAL YEAR
            self.cnyear_realkind = 'q'
            if check:
                if dig: return self.__year_cn2dig(self.cnyear, ce=False, conv_1=False)
                else: return self.__year_dig2cn(self.cnyear, ce=False)
            else: # the original regnal year is not correct
                lyear = self.cnyeardb_handler.lkp_year(intyear)
                if lyear:
                    if len(lyear) == 1:
                        ya = int(lyear[0][12])
                        dynasty = lyear[0][5]
                        regnal = lyear[0][10]
                    else: # get the year according to defaultdy
                        ya = None
                        for defaultdy in ldefaultdy:
                            for tyear in lyear:
                                if tyear[5] == defaultdy: #TODO add alias
                                    ya = int(tyear[12])
                                    dynasty = tyear[5]
                                    regnal = tyear[10]
                                    break
                            if ya:
                                break
                        if not ya: # default last one
                            ya = int(lyear[-1][12])
                            dynasty = lyear[-1][5]
                            regnal = lyear[-1][10]
                    y_offset = intyear - ya + 1
                    if y_offset == 1:
                        if dig: cny = '元'
                        else: cny = '元'
                    else:
                        if dig: cny = str(y_offset)
                        else: cny = dig2cn(y_offset)
                    return '%s%s%s年' %(dynasty, regnal, cny)
                else: # lyear==[]
                    return None

    def get_year_realkind(self):
        if not self.cnyear_realkind:
            self.y2cny()
        return self.cnyear_realkind

    def ycn2dig(self, conv_1=False):
        '''convert 清乾隆十二年 清乾隆12年
                  一八九〇年 1890年
                  一八九零年 1890年
                  清乾隆元年 清乾隆元年
        conv_1: whether to convert 元年 to 1年
        '''
        if conv_1:
            if '元年' in self.cnyear:
                return self.cnyear.replace('元年','1年')
        c_cn = re.compile(r'([一二三四五六七八九十〇零]+)年')
        m = c_cn.search(self.cnyear)
        if not m: return self.cnyear 
        s_dig = m.group(1)
        if self.cnyear_kind == 'ce0' or self.cnyear_kind == 'ce1': # CE
            r = ''.join(str(cn2dig(x)) for x in s_dig)
        else:
            r = cn2dig(s_dig)
        return self.cnyear.replace(s_dig+'年', str(r)+'年')

    def ydig2cn(self):
        '''convert 清乾隆12年 清亁隆十二年
                  清乾隆1年 清乾隆元年
                  清乾隆元年 清乾隆元年
                  1898年 一八九八年
                  abcde abcde
        '''
        c_cn = re.compile(r'([0-9]+)年')
        m = c_cn.search(self.cnyear)
        if not m: return self.cnyear
        s_dig = m.group(1)
        dig = int(s_dig)
        if self.cnyear_kind == 'ce0' or self.cnyear_kind == 'ce1': # CE
            r = ''.join(dig2cn(int(x)) for x in s_dig)
        else:
            if dig == 1:
                r = '元'
            else:
                r = dig2cn(dig)
        return self.cnyear.replace(s_dig+'年',r+'年')

    def __year_cn2dig(self, s, ce=False, conv_1=False):
        '''convert 清乾隆十二年 清乾隆12年
                  一八九〇年 1890年
                  一八九零年 1890年
                  清乾隆元年 清乾隆元年
        ce : whether s is CE or not
        conv_1: whether to convert 元年 to 1年
        '''
        if conv_1:
            if '元年' in s:
                return s.replace('元年','1年')
        c_cn = re.compile(r'([一二三四五六七八九十〇零]+)年')
        m = c_cn.search(s)
        if not m: return s
        s_dig = m.group(1)
        if ce:
            r = ''.join(str(cn2dig(x)) for x in s_dig)
        else:
            r = cn2dig(s_dig)
        return s.replace(s_dig+'年', str(r)+'年')

    def __year_dig2cn(self, s, ce=False):
       '''convert 清乾隆12年 清亁隆十二年
                 清乾隆1年 清乾隆元年
                 清乾隆元年 清乾隆元年
                 1898年 一八九八年
                 abcde abcde
       '''
       c_cn = re.compile(r'([0-9]+)年')
       m = c_cn.search(s)
       if not m: return s
       s_dig = m.group(1)
       dig = int(s_dig)
       if ce:
           r = ''.join(dig2cn(int(x)) for x in s_dig)
       else:
           if dig == 1:
               r = '元'
           else:
               r = dig2cn(dig)
       return s.replace(s_dig+'年',r+'年')
