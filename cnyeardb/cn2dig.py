# Convert chinese numbers to arabic numbers
# copied from http://www.iplaypy.com/code/base/b2600.html
# and modified into a py3 version
# Not chinese number: return None
import re

CN_NUM = {
    u'〇': 0,
    u'一': 1,
    u'二': 2,
    u'三': 3,
    u'四': 4,
    u'五': 5,
    u'六': 6,
    u'七': 7,
    u'八': 8,
    u'九': 9,

    u'零': 0,
    u'壹': 1,
    u'贰': 2,
    u'叁': 3,
    u'肆': 4,
    u'伍': 5,
    u'陆': 6,
    u'柒': 7,
    u'捌': 8,
    u'玖': 9,

    u'貮': 2,
    u'两': 2,
}
CN_UNIT = {
    u'十': 10,
    u'拾': 10,
    u'百': 100,
    u'佰': 100,
    u'千': 1000,
    u'仟': 1000,
    u'万': 10000,
    u'萬': 10000,
    u'亿': 100000000,
    u'億': 100000000,
    u'兆': 1000000000000,
}


def cn2dig(cn):
    lcn = list(cn)
    unit = 0  # 当前的单位
    ldig = []  # 临时数组

    while lcn:
        cndig = lcn.pop()

        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000:
                ldig.append('w')  # 标示万位
                unit = 1
            elif unit == 100000000:
                ldig.append('y')  # 标示亿位
                unit = 1
            elif unit == 1000000000000:  # 标示兆位
                ldig.append('z')
                unit = 1

            continue

        else:
            dig = CN_NUM.get(cndig)

            if unit:
                dig = dig * unit
                unit = 0

            ldig.append(dig)

    if unit == 10:  # 处理10-19的数字
        ldig.append(10)

    ret = 0
    tmp = 0

    while ldig:
        x = ldig.pop()

        if x == 'w':
            tmp *= 10000
            ret += tmp
            tmp = 0

        elif x == 'y':
            tmp *= 100000000
            ret += tmp
            tmp = 0

        elif x == 'z':
            tmp *= 1000000000000
            ret += tmp
            tmp = 0

        else:
            if tmp==None or x==None:# not a chinese number
                return None
            tmp += x

    ret += tmp
    return ret

    # ldig.reverse()
    # print ldig
    # print CN_NUM[u'七']
    """
    def cn2dig_all(s):
        '''convert all cn to dig in a string'''
        c_cn = re.compile('([零一二三四五六七八九十百千万亿兆]+)')
        j = c_cn.finditer(s)
        lpos = [] # to save all the positions to be converted later
        ldig = [] # to save all the converted digits
        for m in j:
            c_cn = 
    """
def year_cn2dig(s, conv_1=False):
    '''convert 清乾隆十二年 清乾隆12年
              一八九〇年 1890年
              一八九零年 1890年
              清乾隆元年 清乾隆元年
    conv_1: whether to convert 元年 to 1年
    '''
    if conv_1:
        if '元年' in s:
            return s.replace('元年','1年')
    c_cn = re.compile(r'([一二三四五六七八九十〇零]+)年')
    m = c_cn.search(s)
    if not m: return s
    s_dig = m.group(1)
    if len(s_dig) == 4: # CE
        r = ''.join(str(cn2dig(x)) for x in s_dig)
    else:
        r = cn2dig(s_dig)
    return s.replace(s_dig+'年', str(r)+'年')
    
if __name__ == '__main__':

    test_dig = [u'九',
                u'十一',
                u'一百二十三',
                u'一千二百零三',
                u'一万一千一百零一',
                u'十万零三千六百零九',
                u'一百二十三万四千五百六十七',
                u'一千一百二十三万四千五百六十七',
                u'一亿一千一百二十三万四千五百六十七',
                u'一百零二亿五千零一万零一千零三十八',
                u'一千一百一十一亿一千一百二十三万四千五百六十七',
                u'一兆一千一百一十一亿一千一百二十三万四千五百六十七',
                u'空'
                ]

    for cn in test_dig:
        print (cn2dig(cn))
    print(year_cn2dig('一八九零年'))
    print(year_cn2dig('一八九〇年'))
    print(year_cn2dig('乾隆元年',True))
    print(year_cn2dig('乾隆元年'))
    print(year_cn2dig('乾隆十二年'))
    print(year_cn2dig('乾隆六十年'))
    print(year_cn2dig('民國二十八年'))
    print(year_cn2dig('清咸豐間'))
    print(cn2dig('清'))
