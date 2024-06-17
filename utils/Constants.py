# alpha = 0.5;
#
# s = 1;
# # onstant for calculating the topic score fo worker/task
#
# k = 1;
# # // propagation factor
#
# IS_DEBUG = false;
#
# lookupLength = 5*60;
#
# showlookupLength = 5*60
def _init(): #初始化
    global  _global_dict
    _global_dict = {}
    _global_dict['alpha'] = 0.5
    _global_dict['s'] = 1
    _global_dict['k'] = 1
    _global_dict['lookupLength'] = 5*60
    _global_dict['showlookupLength'] = 5*60

def set_value(key, value):
    #定义一个全局变量
    _global_dict[key] = value

def get_value(key, defValue=None):
    #获得全局变量，不存在则返回默认值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue