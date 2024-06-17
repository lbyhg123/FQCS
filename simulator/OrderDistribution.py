def _init(): #初始化
    global  _global_dict
    _global_dict = {}
    _global_dict['moreDriver'] = 0
    _global_dict['moreOrder'] = 0

def set_value(key, value):
    #定义一个全局变量
    _global_dict[key] = value

def get_value(key, defValue=None):
    #获得全局变量，不存在则返回默认值
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

def add_value(key, value):
    _global_dict[key] = _global_dict[key] + value