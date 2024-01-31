################################################################################################
# program :  powerball_pick.py
# Author:    Roy Liu
# Date:      31 January 2024
#
#This program use the seeding methods to eliminate unlikely numbers from the pool of 35 numbers
#after reading a file of past 3 drawn numbers. The analysis program powerball_main.py suggested
#that there were few overlaps so by eliminating them and select from the remaining pool may 
#increase the chance of winning
#
# 31/01/2024   Initial coding
#
#################################################################################################

import csv
import random
from random import randrange

seedFile = "/home/royliu/Documents/pb_seeds.txt"
ball_pool = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]

# read the seed file into a list
with open(seedFile, newline='\n') as f:
    reader = csv.reader(f)
    data = list(reader)
    
# delete from the ball_pool numbers included in the seed file
for line in data:
    for num in line:
        if int(num) in ball_pool:
            ball_pool.remove(int(num))
            
poolsize = len(ball_pool)
pick = []

# pick 7 balls from the refined ball pool randomly
completed = False
cnt = 0

while not completed:
    pos = random.randint(0,poolsize - 1)
    selected = ball_pool[pos]
    if selected not in pick:
        pick.append(selected)
        cnt += 1
    else:
        pass
    if cnt == 7:
        completed = True
  
# print out selected to the console        
print(sorted(pick))