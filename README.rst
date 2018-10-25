===========================
A Brief Introduction
===========================

This a tool for conversion between Chinese regnal year and Comman Era,
and a module can be directly used in python.

*This is just an alpha version, which only supports years from Ming Dynasty till doday, and there may be some mistakes. More data will be added in the future.*

Examples:

============ ============
清乾隆元年   1736年
============ ============
明正德十二年 1517年
============ ============
民國20年     1931年
============ ============
一九八〇年   1980年
============ ============
1621年       明天啓元年
============ ============
1861年       清咸豐十一年
============ ============
1948年       民國37年
============ ============

Installation
===============

::

    pip install cnyear

Usage Samples
=================

.. code:: python

    from cnyear import Cnyear
    
    # get the Common Era for a Chinese regnal year
    year_obj1 = Cnyear('清康熙十二年')
    year_obj1.cny2y() # return a tuple (1673, None, True) which means (first year, last year, validity)
    year_obj1.y2cny(dig=True) # 清康熙12年

    # get a span of time
    year_obj2 = Cnyear('明正統間')
    year_obj2.cny2y() # (1436, 1449, True)

    # correct the wrong regnal year
    year_obj3 = Cnyear('清咸豐十二年')
    year_obj3.cny2y() # (1862, None, False)
    year_obj3.y2cny() # 清同治元年

    # get the Chinese regnal year for a Common Era
    Cnyear('明崇禎十八年').y2cny(ldefaultdy=['清','南明']) # 清順治二年
    Cnyear('明崇禎十八年').y2cny(ldefaultdy=['南明','清']) # 南明弘光元年

    
Other Features
===================

#. Convert an invalid Chinese regnal year into a valid Chinese regnal year.
#. Convert Chinese digit numbers into Arabic digit numbers in a year and vice versa.
#. Get each component in an expression of year.

Future Features
===================

#. To support sexagenary cycle 干支.
#. To support operand like minus and plus between years.

Acknowledgement
===================

All the year data come from *Zhongguo Lishi Jinianbiao* (中國歷史紀年表).
