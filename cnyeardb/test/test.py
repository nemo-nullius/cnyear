from ..cnyeardb_obj import Cnyeardb
cnyeardb_handler = Cnyeardb()
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
