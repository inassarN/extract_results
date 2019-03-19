# -*- coding: utf-8 -*-
"""
#Created on Thu Sep 06 12:27:37 2018#
#
#@author: beylander
#!/usr/bin/env python
"""

import os
import sys
import numpy as np
import csv

def find_most_recent_file(dir_files):
    high_time = None
    for i, dir1 in enumerate(dir_files):
        # highest last modified time
        if os.path.getmtime(dir1)>high_time:
            star_dir = dir1
            high_time = os.path.getmtime(dir1)
    return star_dir

def find_file_wString(dir1,string):
    temp_files=[]
    passed = False
    # grab files
    for subdir, dirs, files in os.walk(dir1):
        temp_files.append(files) 
        break
    temp_files = temp_files[0]
    # look for string in list
    ndir = []
    d='blank'
    for d in temp_files:
        if string in d:
            passed = True
            ndir.append("%s/%s"%(dir1,d))
    # if there are no files in the folder:
    if d=='blank':
        return 0
    # there are 2 identical in HFSS so I pick the first one
    if d == temp_files[len(temp_files)-1]:
        if passed == False:
            print('cant find %s file'%string)
            return 0
        else:
            cor_file = find_most_recent_file(ndir)
            return cor_file
def find_dir_wString(dir1,string):
    temp_dir=[]
    for subdir, dirs, files in os.walk(dir1):
        temp_dir.append(dirs) 
        break
    temp_dir = temp_dir[0]
    for d in temp_dir:
        if string in d:
            ndir = "%s/%s"%(dir1,d)
            return ndir
    print('cant find %s directory'%string)
    return 0

def find_expCache(dir1):
    
    ndir = find_dir_wString(dir1,'aedtresults')
    if ndir == 0:
        return 0
    ndir = find_dir_wString(ndir,'results')
    if ndir == 0:
        return 0
    nfile = find_file_wString(ndir,'ExprCache')
    if ndir == 0:
        return 0
    return nfile

def find_pass_count(content):
    loc1 = content[-1].rfind("Pass")
    pass_cnt = content[-1][loc1+6]
    return int(pass_cnt)

def get_values(content,pass_cnt):
    newa = []
    for val in content:
        if val.find("Pass='%s'"%pass_cnt)>0:
            newa.append(val[15:23])
    return newa
def grab_freq(dirs):
    fr = []
    rel_dir = []
    for val in dirs:     
        if val.find(".")>=0:
            fr_temp = val
            fr.append(float(fr_temp))
            rel_dir.append(val)
    return np.array(fr), rel_dir
    
#==============================================================================
# MAIN
#==============================================================================

rdir = r"/home/nimbix/data/8in_00"
#rdir = r"K:\Secure51\hfss\Project\KU_ASM\RF_STUDIES\TripleBandStudy\Ibrahim\NoSS\CF\30DegWedge\2p58\NoWAIM_AdjustedDK2"

file_in_dir = os.listdir(rdir)
all_dir = []
for subdir, dirs, files in os.walk(rdir):
    all_dir.append(dirs) 
    break
dirs = all_dir[0]
print("Number of Simulated Folders: %d"%(len(dirs)))

freqs,dirs = grab_freq(dirs)
num_dirs = len(dirs)
num_result_vars = 7
num_result_vars = num_result_vars + 3
vals = np.zeros((num_dirs,num_result_vars))
vals = np.array(vals,dtype=object)
for ind, d in enumerate( dirs):
    ndir = "%s/%s"%(rdir,d)
    fdir = find_expCache(ndir)
    if fdir==0:
        continue
    print fdir
    with open(fdir) as f:
        content = f.readlines()
    content = [x.strip() for x in content] #remove whitespace characters like `\n` at the end of each line
    pass_cnt = find_pass_count(content) 
#    if pass_cnt==5:
#        pass_cnt=4
#    pass_cnt=3
#    data = np.genfromtxt(fdir, dtype=None , delimiter="\t")
    temp_vals = get_values(content,pass_cnt)
    temp_vals = [pass_cnt]+temp_vals
    nvals = len(temp_vals)
    vals[ind,1:nvals+1] = temp_vals
    vals[ind,0] = freqs[ind]
    vals[ind,-1] = d

file_title = 'output_results'
outfile = open('%s/%s.csv'%(rdir,file_title),'wb')
with outfile as fout:
    writer = csv.writer(fout)
    titles = (['Freq (GHz)','Pass #','D (dBi)','Rad Eff ','Prad','Paccept','Ptop','Pmegtron','Pbot','file'])
    writer.writerow(titles)
    writer.writerows(vals)
print vals
