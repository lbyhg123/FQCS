# 40.635194, -74.196605 156 Staten Island
# 40.726977, -74.016934 231 Manhattan
# result_dir = "../resources/result/"
# files = 'map.txt'
# file = open(result_dir + files, "a", encoding='utf-8')
zone = {1: {'stratZone': 'Bronx', 'endZone': 'Manhattan'},
        1: {'stratZone': 'Bronx','crossZone': ' ' ,'endZone': 'Manhattan'},
        2: {'stratZone': 'Bronx', 'endZone': 'Queens'},
        3: {'stratZone': 'Manhattan', 'endZone': 'Brooklyn'},
        4: {'stratZone': 'Manhattan', 'endZone': 'Queens'},
        5: {'stratZone': 'Manhattan', 'endZone': 'Manhattan'},
        6: {'stratZone': 'Queens', 'endZone': 'Bronx'},
        7: {'stratZone': 'Queens', 'endZone': 'Brooklyn'},
        8: {'stratZone': 'Queens', 'endZone': 'Manhattan'},
        9: {'stratZone': 'Brooklyn', 'endZone': 'Queens'},
        10: {'stratZone': 'Brooklyn', 'endZone': 'Manhattan'},
        11: {'stratZone': 'Brooklyn', 'endZone': 'Staten Island'},
        12: {'stratZone': 'Staten Island', 'endZone': 'Brooklyn'},
        }
zone1 = {

}
map = {'Bronx': {'Manhattan': {0: {0: 'Bronx', 1: 'Manhattan'}},
                 'Queens': {0: {0: 'Bronx', 1: 'Queens'}},
                'Brooklyn': {0: {0: 'Bronx', 1: 'Manhattan', 2: 'Brooklyn'},
                             1: {0: 'Bronx', 1: 'Queens', 2: 'Brooklyn'}},
                  'Staten Island': {0: {0: 'Bronx', 1: 'Manhattan', 2: 'Brooklyn', 3: 'Staten Island'},
                                    1: {0: 'Bronx', 1: 'Queens', 2:'Brooklyn', 3: 'Staten Island'}}}
        , 'Manhattan': {'Brooklyn': {0: {0: 'Manhattan', 1: 'Brooklyn'}},
                        'Queens': {0: {0: 'Manhattan', 1: 'Queens'}},
                        'Bronx': {0: {0: 'Manhattan', 1: 'Bronx'}},
                  'Staten Island': {0: {0: 'Manhattan', 1: 'Brooklyn'}, 2: 'Staten Island'}}
        , 'Queens': {'Manhattan': {0: {0: 'Queens', 1: 'Manhattan'}},
                     'Bronx': {0: {0: 'Queens', 1: 'Bronx'}},
                     'Brooklyn': {0: {0: 'Queens', 1: 'Brooklyn'}},
                  'Staten Island': {0: {0: 'Queens', 1: 'Brooklyn', 2: 'Staten Island'}}}
        , 'Brooklyn': {'Manhattan': {0: {0: 'Brooklyn', 1: 'Manhattan'}},
                       'Queens': {0: {0: 'Brooklyn', 1: 'Queens'}},
                'Bronx': {0: {0: 'Brooklyn', 1: 'Manhattan', 2: 'Bronx'},
                          1: {0: 'Brooklyn', 1: 'Queens', 2: 'Bronx'}},
                  'Staten Island': {0: 'Brooklyn', 1: 'Staten Island'}}
        , 'Staten Island': {'Brooklyn': {0: 'Staten Island', 1: 'Brooklyn'},
                            'Queens': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens'}}
                , 'Manhattan': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens'}},
                  'Bronx': {0: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Manhattan', 3: 'Queens'},
                            1: {0: 'Staten Island', 1: 'Brooklyn', 2: 'Queens', 3: 'Queens'}}}
        }
print(map['Brooklyn']['Bronx'])
# ,
       # 'Manhattan': ,
       #  'Queens':,
       #  'Brooklyn':,
       #  'Staten Island':}
zones = {}
# for i in range(len(line)):
#     zones[line[i]] = {}
#     for j in range(len(line)):
#         zones[line[i]][line[j]] = {}
#         for t in range(len(zone)):
#             if zone[t]['stratZone'] == line[i]:
#
# for i in range(len(zone)):
#     zone1 = {}
#     if zone[i][]
# print(zone)

# file.write(template)