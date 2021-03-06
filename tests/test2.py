#-*-coding:utf-8-*-
from .context import cnyear

Cnyeardb = cnyear.Cnyeardb
Cnyear = cnyear.Cnyear


if __name__ == '__main__':
    cnyeardb_handler = Cnyeardb()
    cnyear = Cnyear('清宣統六年')
    print(cnyeardb_handler.lkp_dnst('清',r'\b清\b',d1='後金·清'))
    print(cnyeardb_handler.lkp_rgnl('清','天聰',da=r'\b清\b'))
    print(cnyeardb_handler.lkp_dnst('清',da=r'\b清\b'))
    print(cnyeardb_handler.lkp_dnst('清'))
    print(cnyeardb_handler.mtch_dnst('三國吳'))
    print(cnyeardb_handler.mtch_dnst('南朝宋'))
    print(cnyeardb_handler.mtch_dnst('唐'))
    print(cnyeardb_handler.mtch_dnst('清'))
    print(cnyeardb_handler.mtch_rgnl('清乾隆十二年'))
    print(cnyeardb_handler.mtch_rgnl('清十二年'))
    print(cnyeardb_handler.mtch_rgnl('明建文元年'))
    print(cnyeardb_handler.mtch_rgnl('南明弘光二年'))
    print(cnyeardb_handler.lkp_dnst('明'))
    print(cnyeardb_handler.lkp_year(1922))
    print(cnyeardb_handler.lkp_year(1822))
    print(cnyeardb_handler.lkp_year(1522))
    print(cnyeardb_handler.lkp_year(1644))
    
    print(Cnyear('清宣統六年').y2cny())
    print(Cnyear('明崇禎十八年').y2cny(ldefaultdy=['明','清','南明']))
    print(Cnyear('明崇禎十八年').y2cny(ldefaultdy=['明','南明','清'],dig=True))
    print(Cnyear('明崇禎十八年').y2cny(ldefaultdy=['明'],dig=True))
    print(Cnyear('明崇禎17年').y2cny(ldefaultdy=['明','清']))
    print(Cnyear('明崇禎十七年').y2cny(ldefaultdy=['清','明'],dig=True))
    print(Cnyear('明崇禎間').y2cny(ldefaultdy=['清','明']))
    print(Cnyear('民國間').y2cny(ldefaultdy=['清','明']))
    print(Cnyear('民國三十八年').y2cny(ldefaultdy=['清','明']))
    print(Cnyear('一九四九年').y2cny(ldefaultdy=['清','明'], dig=True))
    
    def test_cnyear_y2cny(s, ldefaultdy=[], dig=False):
        r = Cnyear(s).y2cny(ldefaultdy=ldefaultdy, dig=dig)
        print(s, r)
    
    test_cnyear_y2cny('民國1年',dig=True)
    test_cnyear_y2cny('民國三十九年')
    test_cnyear_y2cny('民國三十八年')
    test_cnyear_y2cny('民國38年')
    test_cnyear_y2cny('1949年')
    test_cnyear_y2cny('1948年',dig=True)
    test_cnyear_y2cny('一九二三年')
    test_cnyear_y2cny('清宣統十八年')
    test_cnyear_y2cny('明崇禎十七年')
    test_cnyear_y2cny('清順治2年',dig=True)
    test_cnyear_y2cny('明崇禎二十八年',ldefaultdy=['明','清','南明'])
    test_cnyear_y2cny('明崇禎二十八年',ldefaultdy=['明','南明','清'])
    test_cnyear_y2cny('明崇禎二十八年',ldefaultdy=['明'])
    test_cnyear_y2cny('清宣統四十一年',ldefaultdy=['明'],dig=True)
    test_cnyear_y2cny('明宣統四十一年',ldefaultdy=['明'])
    test_cnyear_y2cny('民國上年',ldefaultdy=['明'])
    
    print('\n')
    x = Cnyear('明崇禎二十八年')
    print(x.get_year_realkind())
    print(x.y2cny(ldefaultdy=['南明']))
    print(x.y2cny(ldefaultdy=['清']))
    print(x.get_year_realkind())
    print(__name__)


