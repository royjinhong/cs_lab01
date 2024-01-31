################################################################################################
# program :  powerball_main.py
# Author:    Roy Liu
# Date:      30 January 2024
#
#This program extracts from the powerball archive site and scrape the draw info and the winning
#balls and save the extraction to a text file. It then analyse the draws to ascertain how many 
#repeated numbers were in the previous 3 draws and the result saved in a text file. 
#
# 30/01/2024   Initial coding (powerball itself is not monitored at this version)
# 31/01/2024   Added saving the power ball 
#
#################################################################################################

import requests as rq
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import csv
  
savedir = "/home/royliu/tmp/"    
permURL = "http://www.powerball.net/australia/archive/"
yrExtract = "2000"

fileSaved = savedir + yrExtract + ".txt"
anafile = savedir + yrExtract + "_analysis.txt"
curURL = permURL + yrExtract
html = rq.get(curURL)

desired_tags = ss('a', class_="archive-box")
soup = bs(html.content,'html.parser', parse_only=desired_tags)


#loop through the parsed html to extract the draw no and the winning balls
drawnset = {}
ballset = []
analset = []
pbset = []

for x in soup:
    dkey = x.strong.text.replace("Draw ",'')
    
    #extract the winning balls
    winballs = []
    ballset = []
    for y in x.find_all('div', class_="ball"):
        winballs.append(y.text)
    analset.append(winballs)
       
    #extract the power ball
    pball = x.find('div', class_="powerball")
    
    ballset = [winballs, pball.text]
    pbset.append(pball.text)
    
    drawnset[dkey] = ballset

#save the extracted results in a text file
with open(fileSaved, "wt") as f:
    for key in drawnset:
        balls = drawnset[key]
        data = key + "->" + ",".join(balls[0]) + ", pb=" + balls[1] + "\n"
        f.write(data)
        
f.close

#analyse the drawn numbers, ascertaining how many repeated numbers in the previous 3 draws
no_of_draws = len(analset)  # same as power ball set
lastindx = no_of_draws - 1
indx = 0
ref1 = []
ref2 = []
ref3 = []
res1 = []
res2 = []
res = []

for wb in analset:
    rep1 = 0
    rep2 = 0
    rep3 = 0
  
    c = indx + 3 - lastindx
    if c <= 0:
        ref1 = analset[indx + 1]
        ref2 = analset[indx + 2]
        ref3 = analset[indx + 3]
        for ele in wb:
           if ele in ref1:
               rep1 += 1
           if ele in ref2:
               rep2 += 1
           if ele in ref3:
               rep3 += 1
    elif c > 0 and c <= 1:
        ref1 = analset[indx + 1]
        ref2 = analset[indx + 2]
        for ele in wb:
            if ele in ref1:
                rep1 += 1  
            if ele in ref3:
                rep2 += 1 
    elif c > 1 and c <= 2:
        ref1 = analset[indx + 1]
        for ele in wb:
           if ele in ref1:
               rep1 += 1
    else:
        pass
    
    res1.append([rep1,rep2,rep3])         
    indx += 1

# analyse the power ball repetition by the same logic
# reset indx
indx = 0
for pb in pbset:
    rep1 = 0
    rep2 = 0
    rep3 = 0
  
    c = indx + 3 - lastindx  
    if c <= 0:
        if pb == pbset[indx + 1]:
            rep1 += 1
        if pb == pbset[indx + 2]:
            rep2 += 1
        if pb == pbset[indx + 3]:
            rep3 += 1
    elif c > 0 and c <= 1:
        if pb == pbset[indx + 1]:
            rep1 += 1
        if pb == pbset[indx + 2]:
            rep2 += 1
    elif c > 1 and c <= 2:
        if pb == pbset[indx + 1]:
            rep1 += 1
    else:
        pass
    
    res2.append([rep1,rep2,rep3])
    indx += 1

      
    
with open(anafile, "wt") as af:
    for ar in res1:
        adata = str(ar) + "\n"
        af.write(adata)
        
    af.write("\n")
    
    for ar in res2:
        adata = str(ar) + "\n"
        af.write(adata)
        
af.close

#print to console job finished
print("Finished! no of draws = " + str(no_of_draws))
    