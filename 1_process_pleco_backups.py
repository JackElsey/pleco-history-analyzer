import xml.etree.ElementTree as et
import pandas as pd
import glob
import numpy as np
import time

# time threshold (days)
t_thres = 5

# read each Pleco backup file into a dataframe
# di = dictionary identifier
# ei = entry identifier (the same word in different dictionaries will have different ei)
# t = unix time of word lookup
df = pd.DataFrame(columns=['di','ei','t'])
frames = list()
backups = glob.glob('backups/*.xml')
for backup in backups:
    root = et.parse(backup).getroot()
    for node in root[0]:
        if node.tag=='entries' and node.attrib['source']=='reader':
            di_list = list()
            ei_list = list()
            t_list = list()
            for child in node:
                di_list.append(int(child.attrib['di']))
                ei_list.append(int(child.attrib['ei']))
                t_list.append(int(child.attrib['t']))
            frames.append(pd.DataFrame(list(zip(di_list,ei_list,t_list)), columns=['di','ei','t']))
            
# concatenate all dataframes together then remove duplicate entries
raw_df = pd.concat(frames, ignore_index=True)
df = pd.DataFrame.drop_duplicates(raw_df)

# remove all entries with unique ei (i.e. rare words that were only looked up once)
dup = df.ei.duplicated(keep=False)
df = df[dup]

# determine what subset of the ei's were for lookups that occurred greater than t_thres apart
spans = list()
ei_to_import = list()
for uniq_ei in df.ei.unique():
    times = df[df.ei.isin([uniq_ei,])].t.values
    span = (times.max()-times.min())/8.64E4
    if span>t_thres:
        spans.append(span)
        ei_to_import.append(uniq_ei)
        
# create empty xml object based on Pleco history backup xml structure
cur_time = str(round(time.time()))
plecodump = et.Element('plecodump', attrib={'formatversion':'1'})
plecohistory = et.SubElement(plecodump, 'plecohistory', attrib={'time':str(cur_time), 'version':'1'})
entries = et.SubElement(plecohistory, 'entries', attrib={'source':'reader', 'version':'1'})

# add ei (as well as corresponding di and one t value) into xml object
for ei in ei_to_import:
    di = df[df.ei.isin([ei,])].iloc[0,0]
    t = df[df.ei.isin([ei,])].iloc[0,2]
    entry_attrib = {'dc':'0', 'di':str(di), 'ei':str(ei), 't':str(t)}
    entry = et.SubElement(entries, 'entry', attrib=entry_attrib)
    
# save xml file for import into Pleco
tree = et.ElementTree(plecodump)
tree.write(open('pleco_import.xml', 'w'), encoding='unicode')