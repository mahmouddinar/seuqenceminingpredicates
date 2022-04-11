# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 11:56:57 2013

@author: mdinar
"""

from __future__ import division

# scenario 2: clingo input comes from a file, say "foo.lp"
# open a pipe to clingo process
# we only open stdout: "clingo foo.lp 2>&1 | <python>"

# alternative1: parent_of chained but all entities have the same type parent_of
# path_out="C:\Users\mdinar\Documents\Research\Creative IT\Empirical material\Can crusher\MAE 342\P-maps\parent_of chained\\"

# alternative2: parent_of chained and each entity type has 
#  its own parent_of relation e.g. parent_of_fnction
path_out="C:\Users\mdinar\Documents\Research\Creative IT\Empirical material\Can crusher\MAE 342\P-maps\parent and entity\\"

path_write="C:\Users\mdinar\Documents\Research\Creative IT\Empirical material\Can crusher\MAE 342\\"
# generating the range that contains P-maps of students in MAE 342 (can crusher problem)
p_maps=range(9,97)
p_maps.remove(19)
p_maps.remove(23)
p_maps.remove(24)
p_maps.remove(25)
p_maps.remove(26)
p_maps.remove(28)
p_maps.remove(31)
p_maps.remove(34)
p_maps.remove(35)
p_maps.remove(36)
p_maps.remove(38)
p_maps.remove(44)
p_maps.remove(45)
p_maps.remove(48)
p_maps.remove(49)
p_maps.remove(57)
p_maps.remove(60)
p_maps.remove(63)
p_maps.remove(70)
p_maps.remove(71)
p_maps.remove(74)
p_maps.remove(78)
p_maps.remove(79)
p_maps.remove(81)
p_maps.remove(83)
p_maps.remove(84)
p_maps.remove(94)


# testing the code for a shorter list of sequences (a few p-maps)
# delete, or mark off the next line after testing!
p_maps=range(9,13)

import subprocess
from operator import itemgetter


sortedNamesAllRecords=[]

for i in p_maps:
    # open the pipe to clingo process; output from *.lp p-map
    p=subprocess.Popen(["C:\Program Files\clingo-3.0.5-win64\clingo","0","-l", path_out+str(i)+".lp"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    unsortedArray=[]
    sortedNamesArray=[]

    # run clingo including P-map facts, and parent_of chaining rule
    for line in p.stdout.readlines():
        if line.find("(")>1:
            name=line.partition("(")[0].split()[1]
            time=line.split(",")[-1].split(")")[0]
            unsortedArray.append([name,time])
    
    # sorting P-map predicates in ascending order (based on time created)
    for element in xrange(0,len(unsortedArray)-2):
        for record in xrange(0,len(unsortedArray)-2):
            if int(unsortedArray[record][1])>=int(unsortedArray[record+1][1]):
                temp=unsortedArray[record]
                unsortedArray[record]=unsortedArray[record+1]
                unsortedArray[record+1]=temp
    
    # write to list of lists - list of all P-maps with each sublist as one P-map
    sortedNamesArray=map(itemgetter(0),unsortedArray)    
    sortedNamesAllRecords.append(sortedNamesArray)

#print 'This is all the pmaps sorted'
#print sortedNamesAllRecords

report_file=open(path_write+"General sequence mining report.txt",'w')
# report_file.write('Mining sequences started, please wait!')

# a function for searching a sequence in a list
# use to see if a subsequence exists in a sequence
# e.g. ['a','b'] in ['c','d','a','b','c']
def contains(sub, seq):
    for i in xrange(len(seq)-len(sub)+1):
        for j in xrange(len(sub)):
            if seq[i+j] != sub[j]:
                break
        else:
            return True
    return False

# a function for searching sublists in a list of lists (subsequences in sequences)
# use to determine if subsequence have already been searched
# e.g. ['a','b'] in [['c','b','d'],['a','b']]
def contains_list(sublist,superlist):
    for i in superlist:
        if i==sublist:
            return True
            break
    else:
        return False


# a function for searching list of subsequences in a list of divided sequences
# use to determine if a subsequence exists in divided sequences
# e.g. ['a','c','e'] in [['a','b'],['c','d'],['c','b'],['a','e']]
def follows(subseq,seq):
	exhaustion_counter=len(subseq)
	last_saved_position=0
	for item in subseq:
		for j in xrange(last_saved_position,len(seq)):
			if contains(item,seq[j]):
				exhaustion_counter-=1
				last_saved_position=j+1
				break
	if exhaustion_counter==0:
		return True
	else:
		return False

# define minimum support and range of maximum support (for uncommon but non-zero subs)            
minsupp=0.5
maxsuppLow=0.05
maxsuppUp=0.1
windowsize=10

divided_pmaps=[]

unpruned_highsupp_subs=[]
#highsupport_subsequences=[]
unpruned_lowsupp_subs=[]

subSequences=[] # declaring the list that contains all searched subsequences
#subSeqsSupport=[] # declaring the list of searched subsequences and their support

pmapCount=len(sortedNamesAllRecords) # the number of all collected pmaps

# a function for dividing each pmap lst into sublists of length size sz
lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]

# dividing all pmaps into window-sized sub-lists
#  the result is a list of list of lists: [all pmaps][each pmap][window list]
for pmap in sortedNamesAllRecords:
    divided_pmaps.append(lol(pmap,windowsize))

#for pmap in divided_pmaps:



## next line is for debugging. Delete when done!
##debugcounter1=0
##debugcounter2=0
##debugcounter3=0
#
## Loop 1: looking into each P-map
#for pmap in sortedNamesAllRecords:
#    
#    # Loop 2: strating from a sub-sequence of length 2 up to the length of the P-map
#    
#    # next line is for debugging. Delete when done!    
#    # print 'Selecting sub-sequences from P-map ',pmap
#    # debugcounter3+=1
#    
#    for subseqlength in xrange(2,len(pmap)+1):
#        
#        # Loop 3: for each starting position in the P-map
#        # the last subsequence starts at length of pmap minus lenth of subsequence 
#        for position in xrange(len(pmap)-subseqlength+1):
#            subsequence=pmap[position:position+subseqlength]
#            
#            # check if the subseq has already been searched; if so go to next sub
#            if contains_list(subsequence,subSequences):
#                # debugcounter2+=1
#                break
#            else:
#                
#                # Loop 4: searching the subsequence in all pmaps to calculate support
#                subseq_frequency=0 # for each search of subseqs reset the counter
#                support=0
#                
#                # next line is for debugging. Delete when done!
#                # debugcounter1+=1
#                
#                for pmap_records in sortedNamesAllRecords:
#                    if contains(subsequence,pmap_records):
#                        subseq_frequency+=1
#                        # next line is for debugging. Delete when done!
#                        # print pmap_records,'contains',subsequence
#                        
#                support=round(subseq_frequency/pmapCount,2) # calculate support for subseq
#                
#                # add high support subseq to the list of unpruned subs
#                if support>minsupp:
#                    unpruned_highsupp_subs.append(subsequence+[support])
#                    
##                    highsupport_subsequences.append(subsequence)
#                if maxsuppLow<support<maxsuppUp:
#                    unpruned_lowsupp_subs.append(subsequence+[support])
#                subSequences.append(subsequence)
##                subSeqsSupport.append(subsequence+[support])
#
## sort unpruned high support subs based on subs length
#for element in xrange(0,len(unpruned_highsupp_subs)-2):
#    for record in xrange(0,len(unpruned_highsupp_subs)-1):
#        if len(unpruned_highsupp_subs[record])>=len(unpruned_highsupp_subs[record+1]):
#            temp=unpruned_highsupp_subs[record]
#            unpruned_highsupp_subs[record]=unpruned_highsupp_subs[record+1]
#            unpruned_highsupp_subs[record+1]=temp
#
#
## sort unpruned low support subs based on subs length
#for element in xrange(0,len(unpruned_lowsupp_subs)-2):
#    for record in xrange(0,len(unpruned_lowsupp_subs)-1):
#        if len(unpruned_lowsupp_subs[record])>=len(unpruned_lowsupp_subs[record+1]):
#            temp=unpruned_lowsupp_subs[record]
#            unpruned_lowsupp_subs[record]=unpruned_lowsupp_subs[record+1]
#            unpruned_lowsupp_subs[record+1]=temp
#
## sort all subs based on subs support
##for element in xrange(0,len(subSeqsSupport)-2):
##            for record in xrange(0,len(subSeqsSupport)-1):
##                if subSeqsSupport[record][-1]<=subSeqsSupport[record+1][-1]:
##                    temp=subSeqsSupport[record]
##                    subSeqsSupport[record]=subSeqsSupport[record+1]
##                    subSeqsSupport[record+1]=temp
#
## sort high support subs based on subs support
##for element in xrange(0,len(unpruned_highsupp_subs)-2):
##            for record in xrange(0,len(unpruned_highsupp_subs)-1):
##                if unpruned_highsupp_subs[record][-1]<=unpruned_highsupp_subs[record+1][-1]:
##                    temp=unpruned_highsupp_subs[record]
##                    unpruned_highsupp_subs[record]=unpruned_highsupp_subs[record+1]
##                    unpruned_highsupp_subs[record+1]=temp
#
#
## pruning! remove subsequences from list of high support subs 
##  if they are a part of another high support subsequence
#pruned_highsupport_subsequences=[]
#for i in xrange(0,len(unpruned_highsupp_subs)-1):
#    for j in xrange(i+1,len(unpruned_highsupp_subs)):
#        if contains(unpruned_highsupp_subs[i][0:-1],unpruned_highsupp_subs[j][0:-1]):
#            break
#    else:
#        pruned_highsupport_subsequences.append(unpruned_highsupp_subs[i])
#            
##pruned_highsupport_subsequences.append(highsupport_subsequences[-1])
#
##print 'All subsequences with corresponding frequencies'
##print subSeqsSupport
#
#report_file.write('List of pruned high support subseqs with minsupp=')
#report_file.write(str(minsupp)+"\n")
#report_file.writelines(["%s\n" % item  for item in pruned_highsupport_subsequences])
#report_file.write('\nList of high support subseqs before prunning\n')
#report_file.writelines(["%s\n" % item  for item in unpruned_highsupp_subs])
#report_file.write("\n")
#report_file.write('\nList of low support subseqs with support range ['+str(maxsuppLow)+'-'+str(maxsuppUp)+"]\n")
#report_file.writelines(["%s\n" % item  for item in unpruned_lowsupp_subs])
##report_file.write('\nList of all sub-sequences with support in ascending order\n')
##report_file.writelines(["%s\n" % item  for item in subSeqsSupport])
#report_file.close()
#
##print 'List of high support subseqs with minsupp=',minsupp
##print highsupport_subsequences
##print 'List of high support subseqs before prunning'
##print unpruned_highsupp_subs
##print 'List of low support subseqs with support range [',maxsuppLow,'-',maxsuppUp,']'
##print unpruned_lowsupp_subs