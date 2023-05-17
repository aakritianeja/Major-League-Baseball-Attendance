"""
Pull data from saved html webpages in order to get the divisions each team
was in for each year
"""

from bs4 import BeautifulSoup
import re
import os
import json



files = os.listdir('../data/standings')
divisions = {}

for filename in files:
    # only process .html files
    if filename[-5:] == '.html':
        with open(os.path.join('../data/standings/', filename), 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
        names = soup.find_all('tr')
        pattern = '\d+ \w+ League Standings'
        i = 0
        ctr = 0
        header = None
        stopflag = False
        # find the start of a league
        league = 'AL'
        while not stopflag:
            if re.match(pattern, names[i].text):
                i += 1
                ctr += 1
                
                # first time through initialize variables
                if not header:
                    header = [h.text for h in names[i].find_all('td')]
                    data = [[] for _ in range(len(header) + 1)]
                    header[0] = 'team'
                div = league + '_' + names[i].td.text
                
                # pull data from all divisions in a league
                while names[i + 1].attrs['class'][0] != 'stathead':
                    if names[i + 1].attrs['class'][0] == 'colhead':
                        div = league + '_' + names[i + 1].td.text
                        i += 1
                    else: 
                        for j, d in enumerate(names[i + 1].find_all('td')):
                            data[j].append(d.text)
                        data[j + 1].append(div)
                        i += 1
                if ctr == 2:
                    stopflag = True
                league = 'NL'
            i += 1
        
        
        # clean team names
        data[0] = [n.split('-')[-1].rstrip() for n in data[0]]
        divisions[filename[:-5]] = {t : d for t, d in zip(data[0], data[-1])}

# write to file
json_div = json.dumps(divisions)
with open('../data/division.json', 'w') as f:
    f.write(json_div)