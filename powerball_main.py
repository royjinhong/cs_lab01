import requests as rq
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
import csv
  
savedir = "/home/royliu/tmp/"    
permURL = "http://www.powerball.net/australia/archive/"
yrExtract = "2022"

fileSaved = savedir + yrExtract + ".txt"
anafile = savedir + yrExtract + "_analysis.txt"
curURL = permURL + yrExtract
html = rq.get(curURL)

desired_tags = ss('a', class_="archive-box")
soup = bs(html.content,'html.parser', parse_only=desired_tags)


#loop through the parsed html to extract the draw no and the winning balls
drawnset = {}
analset = []

for x in soup:
    dkey = x.strong.text.replace("Draw ",'')
    
    #extract the winning balls
    winballs = []
    for y in x.find_all('div', class_="ball"):
        winballs.append(y.text)
    analset.append(winballs)
    drawnset[dkey] = winballs

#save the extracted results in a text file
with open(fileSaved, "wt") as f:
    for key in drawnset:
        data = key + "->" + ",".join(drawnset[key]) + "\n"
        f.write(data)
        
f.close

#analyse the drawn numbers, ascertaining how many repeated numbers in the previous 3 draws
no_of_draws = len(analset)
lastindx = no_of_draws - 1
indx = 0
ref1 = []
ref2 = []
ref3 = []
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
               
    res.append([rep1,rep2,rep3])
    indx += 1
    
with open(anafile, "wt") as af:
    for ar in res:
        adata = str(ar) + "\n"
        af.write(adata)
af.close

#print to console job finished
print("Finished! no of draws = " + str(no_of_draws))
    