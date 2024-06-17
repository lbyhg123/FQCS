import glo
import glo2
if __name__ =='__main__':
    glo._init()
    glo.set_value(0, 0) #给全局变量cho，赋值game
    glo.add(0, 50)
    print(glo.get_value(0))
    glo2.pair(0) #调用glo2文件的Name类的pair函数，判断全局变量cho是否共享成功

