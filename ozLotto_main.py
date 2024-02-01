#######################################################################################################
# program :  oztLotto_main.py
# Author:    Roy Liu
# Date:      01 February 2024
#
#This program extracts from the oz lotto archive site and scrape the draw info and the winning
#balls and save the extraction to a text file. It then analyse the draws to ascertain how many 
#repeated numbers were in the previous 5 draws and the result saved in a text file. 
#
# 01/02/2024   Initial coding 
#
######################################################################################################

import requests as rq
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss


permURL = "https://australia.national-lottery.com"
savedir = "/home/royliu/tmp/"    

fileSaved = savedir + "oz_lotto" + ".txt"
anafile = savedir + "oz_lotto" + "_analysis.txt"

drawncount = 0

# first extract from controlling page the years available in archive

initialURL = permURL + "/oz-lotto/past-results"
html = rq.get(initialURL)

desired_tags = ss('span', class_="ddRel")
soup = bs(html.content,'html.parser', parse_only=desired_tags)

# loop through this soup and extract available years in the archive
archives = []

for ele in soup.find_all('a', href=True):
    archives.append(ele['href'])

# loop through this list and get each page and extract all the required info
drawnset = {}
analset = []

for yrURL in archives:
   
    curURL = permURL + yrURL
    html = rq.get(curURL)

    desired_tags = ss('tr', attrs=not(['rel']))
    soup = bs(html.content,'html.parser', parse_only=desired_tags)
    
    for x in soup:
        drawnumExtracted = False
        dkey = " "
        
        for z in x.find_all('a', title=True, href=True):
            part1 = ' '.join(z['title'].split(' ')[7:])
            part2 = part1.split(' ')[1]
            unwanted = part1.replace(part2, part2+",")
            if not drawnumExtracted:
               dkey = z.text.replace(unwanted,'').replace("Draw ",'')
               drawnumExtracted = True
    
        #extract all the winning balls including supplementary
        winballs = []
        
        for y in x.find_all('li'):
            winballs.append(y.text)
       
        if dkey.isdigit():
            drawnset[dkey] = winballs
            analset.append(winballs)
            drawncount += 1
    
#save the extracted results in a text file
with open(fileSaved, "wt") as f:
    for key in drawnset:
        balls = drawnset[key]
        data = key + "->" + ",".join(balls) + "\n"
        f.write(data)
        
f.close


# Analyse the numbers for repetition
no_of_draws = len(analset)  # same as power ball set
lastindx = no_of_draws - 1
indx = 0
ref1 = []
ref2 = []
ref3 = []
ref4 = []
res = []

for wb in analset:
    rep1 = 0
    rep2 = 0
    rep3 = 0
    rep4 = 0
  
    c = indx + 4 - lastindx
    if c <= 0:
        ref1 = analset[indx + 1]
        ref2 = analset[indx + 2]
        ref3 = analset[indx + 3]
        ref4 = analset[indx + 4]
        for ele in wb:
           if ele in ref1:
               rep1 += 1
           if ele in ref2:
               rep2 += 1
           if ele in ref3:
               rep3 += 1
           if ele in ref4:
               rep4 += 1
    elif c > 0 and c <= 1:
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
    elif c > 1 and c <= 2:
        ref1 = analset[indx + 1]
        ref2 = analset[indx + 2]
        for ele in wb:
           if ele in ref1:
               rep1 += 1
           if ele in ref2:
               rep2 += 1
    elif c > 2 and c <= 3:
        ref1 = analset[indx + 1]
        for ele in ref1:
            if ele in ref1:
                rep1 += 1
    else:
        pass
    
    res.append([rep1,rep2,rep3,rep4])         
    indx += 1

      
    
with open(anafile, "wt") as af:
    for ar in res:
        adata = str(ar) + "\n"
        af.write(adata)  
        
af.close

if not no_of_draws == drawncount:
    print("out of sync detected")
    
#print to console job finished
print("Finished! no of draws = " + str(drawncount))
 