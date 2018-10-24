'''
--------------------- 
作者：mattkang 
来源：CSDN 
原文：https://blog.csdn.net/handsomekang/article/details/52563487?utm_source=copy 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''
import re

def convert(n):
    '''accept int (not float) and convert it to chinese digit numbers (str)'''
    #units = ['', '万', '亿']
    #nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    #decimal_label = ['角', '分']
    #small_int_label = ['', '拾', '佰', '仟']
    #
    units = ['', '万', '亿']
    nums = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
    #decimal_label = ['角', '分']
    small_int_label = ['', '十', '百', '千']
    #
    #int_part, decimal_part = str(int(n)), str(n - int(n))[2:]  # 分离整数和小数部分
    #
    int_part = str(int(n)) # only accept int, no float
    #

    res = []
    #if decimal_part:
    #    res.append(''.join([nums[int(x)] + y for x, y in zip(decimal_part, decimal_label) if x != '0']))

    if int_part == '0':
        return '〇'
    if int_part != '0':
        #res.append('圆')
        while int_part:
            small_int_part, int_part = int_part[-4:], int_part[:-4]
            tmp = ''.join([nums[int(x)] + (y if x != '0' else '') for x, y in list(zip(small_int_part[::-1], small_int_label))[::-1]])
            tmp = tmp.rstrip('零').replace('零零零', '零').replace('零零', '零')
            unit = units.pop(0)
            if tmp:
                tmp += unit
                res.append(tmp)
    #return ''.join(res[::-1])
    #
    # Concerning 一十五 -> 十五
    r = ''.join(res[::-1])
    if r[:2] == '一十':
        r = r[1:]
    return r
    #
dig2cn = convert

def year_dig2cn(s):
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
   if len(s_dig) == 4: # CE
       r = ''.join(dig2cn(int(x)) for x in s_dig)
   else:
       if dig == 1:
           r = '元'
       else:
           r = dig2cn(dig)
   return s.replace(s_dig+'年',r+'年')


if __name__ == '__main__':
    print(convert(1000))
    print(dig2cn(10))
    print(dig2cn(15))
    print(dig2cn(23))
    for i in range(0, 100):
        print(dig2cn(i))
    print(year_dig2cn('清乾隆元年'))
    print(year_dig2cn('清乾隆1年'))
    print(year_dig2cn('清乾隆2年'))
    print(year_dig2cn('民國2年'))
    print(year_dig2cn('民國間'))
    print(year_dig2cn('1898年'))
    print(year_dig2cn('1890年'))


