################################################################################################
# program :  powerball_stats.py
# Author:    Roy Liu
# Date:      02 February 2024
#
# This program extracts from the powerball archive site the official statistics available from
# all the available draws so far 
#
# 02/02/2024   Initial coding 
#
#################################################################################################

import requests as rq
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
  
savedir = "/home/royliu/tmp/"   
srcURL = "https://www.powerball.net/australia/statistics"
savedFile = savedir + "powerball_draws_stats.txt"

html = rq.get(srcURL)
desired_tags = ss('div', id="_d")
soup = bs(html.content,'html.parser', parse_only=desired_tags)

# extract from soup all the desired info
no_of_draws = 0
mbStats = {}
pbStats = {}
pairStats = []

no_of_draws = int(soup.find('span', class_="draw-count").text.replace(",",''))
    
# main balls statistics
for mainballs in soup.find('div', { "data-ball":"ball"}).find_all('div',class_="freq-result js-stats-item"):
    try:
        ballnum = mainballs['data-num']
        ballfreq = mainballs['data-freq']
        mbStats[ballnum] = ballfreq
    except:
        pass
    

# powerball statistics
for powerballs in soup.find('div', { "data-ball":"powerball"}).find_all('div',class_="freq-result js-stats-item"):
    try:
        ballnum = powerballs['data-num']
        ballfreq = powerballs['data-freq']
        pbStats[ballnum] = ballfreq
    except:
        pass
    
# paired balls statistics
for pairballs in soup.find_all('div', {"class":"freq-result stat-box"}):
    numballs = []
    ballfreq = 0
    try:
        for x in pairballs:
            x_val = x.text.strip()
            if not x_val == '':
                if x_val.isdigit():
                    numballs.append(x_val)
                elif "Frequency" in x_val:
                    ballfreq = int(x_val.replace("Frequency ",''))
                    pairStats.append([numballs, ballfreq])
            else:
                pass
    except:
        pass


# write the statistics out in a file   
with open(savedFile, "wt") as f:
    f.write("No of draws examined in this statistics: -> " + str(no_of_draws) + "\n")
    f.write("Main balls Statistics\n")
    f.write("=====================\n")
    
    for key in mbStats:
       f.write(key + "-> " + mbStats[key] + "\n")        
       
    f.write("\n")
      
    f.write("Power Balls Statistics\n")
    f.write("======================\n")
    
    for key in pbStats:
        f.write(key + "-> " + pbStats[key] + "\n")
     
    f.write("\nPaired Balls Statistics\n")  
    f.write("=========================\n")
    
    for ele in pairStats:
        numset = ''
        no_ele = len(ele[0])
        for n in range(no_ele):
           if not n == no_ele - 1:
               numset = numset + ele[0][n]+ ","
           else:
               numset = numset + ele[0][n]
        
        f.write(numset + " -> " + str(ele[1]) + "\n")
        

f.close

# print finished message to the console
print("Statistics extraction completed!")

