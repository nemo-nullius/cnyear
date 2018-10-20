import re
from .cnyeardb_pkg import cnyeardb
from .cn2dig import cn2dig

cnyear_handler = cnyeardb.Cnyeardb()

def ycn2y(stime):
    '''
    stime: 清道光十二年/清道光12年/清道光間/民國元年/民國1年/民國間/一九五〇年
    return: (intA, intB)
    intA: beginning year
    intB: end year for 間 else None
    '''

    #pre-min: 1.清年號十五年 2.清年號15年
    pq0 = cnyear_handler.mkregp_rgnl()
    pq1 = pq0.replace(r'元一二三四五六七八九十',r'0-9')
    pq2 = pq0.replace(r'([元一二三四五六七八九十]+)年',r'間')
    pm0 = r'民國([元一二三四五六七八九十]+)年'
    pm1 = r'民國([0-9]+)年'
    pm2 = r'民國間'
    pp0 = r'(一九[〇一二三四五六七八九]{2,2})'
                #dtime = int(''.join([str(cn2dig(x)) for x in stime_pure])) #一九五九年
    cq0 = re.compile(pq0)
    cq1 = re.compile(pq1)
    cq2 = re.compile(pq2)
    cm0 = re.compile(pm0)
    cm1 = re.compile(pm1)
    cm2 = re.compile(pm2)
    cp0 = re.compile(pp0)

    m = cq0.search(stime)
    if m:
        d = m.group(3)
        rgnl = m.group(4)
        lyear = cnyear_handler.lkp_rgnl(d, rgnl)
        #Todo: if many results
        ya = int(lyear[0][12])
        yz = int(lyear[0][13])
        yoffset_ch = m.group(5)
        if yoffset_ch == '元':
            yoffset = 1
        else:
            yoffset = cn2dig(yoffset_ch)
        return (ya+yoffset-1, None)
    m = cq1.search(stime)
    if m:
        d = m.group(3)
        rgnl = m.group(4)
        lyear = cnyear_handler.lkp_rgnl(d, rgnl)
        #Todo: if many results
        ya = int(lyear[0][12])
        yz = int(lyear[0][13])
        yoffset = int(m.group(5))
        return (ya+yoffset-1, None)
    m = cq2.search(stime)
    if m:
        d = m.group(3)
        rgnl = m.group(4)
        lyear = cnyear_handler.lkp_rgnl(d, rgnl)
        #Todo: if many results
        ya = int(lyear[0][12])
        yz = int(lyear[0][13])
        return (ya,yz)
    m = cm0.search(stime)
    if m:
        yoffset_ch = m.group(1)
        if yoffset_ch == '元':
            yoffset = 1
        else:
            yoffset = cn2dig(yoffset_ch)
        return (1911+yoffset, None)
    m = cm1.search(stime)
    if m:
        yoffset_ch = m.group(1)
        yoffset = int(yoffset_ch)
        return (1911+yoffset, None)
    m = cm2.search(stime)
    if m:
        return (1912, 1949)
    m = cp0.search(stime)
    if m:
        ych = m.group(1)
        return (int(''.join([str(cn2dig(x)) for x in ych])),None) #一九五九年
    return (None, None)


