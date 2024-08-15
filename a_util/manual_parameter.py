# heatingTemp = { 
#     0 : {"0": 15,   "r-2": 15,   "r" : 16,  "13" : 18,  "s-1": 18,  "s": 15,  "s+2" : 15,  "23": 15},
#     3 : {"0": 15,   "r-2": 15,   "r" : 16,  "13" : 18,  "s-1": 18,  "s": 15,  "s+2" : 15,  "23": 15},
#     7 : {"0": 15,   "r-2": 15,   "r" : 16,  "13" : 18,  "s-1": 18,  "s": 15,  "s+2" : 15,  "23": 15},
#     14 : {"0": 15,   "r-2": 15,   "r" : 16,  "13" : 18,  "s-1": 18,  "s": 15,  "s+2" : 15,  "23": 15},
#     21 : {"0": 15,   "r-2": 15,   "r" : 16,  "13" : 18,  "s-1": 18,  "s": 15,  "s+2" : 15,  "23": 15}
# }


t1 = 21
t2 = 9
t3 = 15.78
t4 = 10

# t1 = 21
# t2 = 9
# t3 = 16.35
# t4 = 10

# t1 = 21
# t2 = 9
# t3 = 16.75
# t4 = 10

# t1 = 19
# t2 = 10
# t3 = 17
# t4 = 10

temp1 = [t1,t1,t2,t2,t2,t2,t1,t1]
temp2 = [t3,t3,t4,t4,t4,t4,t3,t3]

heatingTemp = { 
    0 : {"0": 18, "r": 18, "r+1": 24, "s-1": 24, "s": 18, "23": 18},
    70 : {"0": 17, "r": 17, "r+1": 21, "s-1": 21, "s": 17, "23": 17},
}

ventOffset = {
    0 : {"0": 1, "r": 1, "r+1": 1, "s-1": 1, "s": 1, "23": 1},
    70 : {"0": 1, "r": 1, "r+1": 1, "s-1": 1, "s": 1, "23": 1},
}

# heatingTemp = { 
#     0 : {"0": temp1[0], "r-2": temp1[1], "r": temp1[2], "r+2": temp1[3], "12": temp1[4], "s-2": temp1[5], "s": temp1[6], "s+2": temp1[7]},
#     70 : {"0": temp2[0], "r-2": temp2[1], "r": temp2[2], "r+2": temp2[3], "12": temp2[4], "s-2": temp2[5], "s": temp2[6], "s+2": temp2[7]}   
# }

# temp = 18
# temp2 = 11
# temp3 = 18
# temp4 = 11

# temp = 15
# temp2 = 11
# temp3 = 19
# temp4 = 12

# temp = 17
# temp2 = 11
# temp3 = 16
# temp4 = 11

# heatingTemp = { 
#     0 : {"0": temp,   "r-2": temp2,   "r" : temp2,  "11" : temp2,  "s-1": temp2,  "s": temp2,  "s+2" : temp,  "23": temp},
#     7 : {"0": temp,   "r-2": temp2,   "r" : temp2,  "11" : temp2,  "s-1": temp2,  "s": temp2,  "s+2" : temp,  "23": temp},
#     14 : {"0": temp,   "r-2": temp2,   "r" : temp2,  "11" : temp2,  "s-1": temp2,  "s": temp2,  "s+2" : temp,  "23": temp},
#     21 : {"0": temp,   "r-2": temp2,   "r" : temp2,  "11" : temp2,  "s-1": temp2,  "s": temp2,  "s+2" : temp,  "23": temp},
#     63 : {"0": temp3,   "r-2": temp3,   "r" : temp4,  "11" : temp4,  "s-1": temp4,  "s": temp4,  "s+2" : temp3,  "23": temp3},
#     73 : {"0": temp3,   "r-2": temp3,   "r" : temp4,  "11" : temp4,  "s-1": temp4,  "s": temp4,  "s+2" : temp3,  "23": temp3}
# }

hours_light = {
    0 : 0,
    45 : 16
}

max_iglob = {
    0 : 10,
    24 : 10,
    44 : 10    
}

# vent_set = 10
# vent_set2 = 10
# vent_set3 = 10
# ventOffset = {
#     0 : {'0': vent_set, 'r-2': vent_set, 'r+2': vent_set, '13': vent_set, 's-2': vent_set, 's+2': vent_set, '23': vent_set},
#     21 : {'0': vent_set, 'r-2': vent_set, 'r+2': vent_set, '13': vent_set, 's-2': vent_set, 's+2': vent_set, '23': vent_set},
#     43 : {'0': vent_set2, 'r-2': vent_set2, 'r+2': vent_set2, '13': vent_set2, 's-2': vent_set, 's+2': vent_set2, '23': vent_set2},
#     63 : {'0': vent_set3, 'r-2': vent_set3, 'r+2': vent_set3, '13': vent_set3, 's-2': vent_set3, 's+2': vent_set3, '23': vent_set3}
# }




