# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 01:54:30 2015

@author: nausheenfatma
"""
#Tokenisation

import operator
import matplotlib.pyplot as plt
import re

def add_unigram_to_list(token,case,main_word):  #unigrams_dict is of the form {token:[frequency,case satisfied,last word from which token generated]}
    if token not in unigrams_dict :
        unigrams_dict[token]=[1,"case:"+case,main_word]
    else :
        count=unigrams_dict[token][0]+1
        unigrams_dict[token]=[count,"case:"+case,main_word]        
        

def find_unigrams(token):
   # print token
    if len(token)==1:    #for single tokens like , . add token as it is
             add_unigram_to_list(token,"-1",token)

    elif re.match("[-+]*[0-9]+[\w\W]+",token) and not re.match('[-]*[0-9]*[,.][0-9]+',token) : # for separating units like px,km and commas and fulltop from end of numbers  
    #        print "case 0 "
            list0=re.findall(r"[\+\-']+", token)
            #print list0
            for word in list0:
                add_unigram_to_list(word,"0",token)
            list1= re.findall(r"[\d']+", token)
           # print list1
            for word in list1:
                add_unigram_to_list(word,"0",token)
            list2= re.findall(r"[^\d]+", token)
          #  print list2
            for word in list2:
                add_unigram_to_list(word,"0",token)
                
    elif re.match('[-]*[0-9]*[,.][0-9]*[\w\W]*',token):  #for keeping decimals and commas between numbers but separating units,commas,fullstop from end
           
            list0=re.findall(r"[\+\-']+", token)
            #print list0
            list1= re.findall(r"[0-9]*[,.][0-9]*", token) #number 
           # print list1
            prefix_length=0
            number_length=0
            if len(list0)>0:
                prefix_length+=len(list0[0])
            if len(list1)>0:
                number_length+=len(list1[0])
            prefix=token[0:prefix_length]
            number=token[prefix_length:(prefix_length+number_length)] 
           # print len(number)
            unit=token[(prefix_length+number_length):]
            if len(prefix)>0 :
               # print prefix
                add_unigram_to_list(prefix,"1",token)
            if len(number)>0 :
               # print number
                add_unigram_to_list(number,"1",token)
            if len(unit)>0:
               # print unit
                add_unigram_to_list(unit,"1",token)

          
    elif re.match('[$]([0-9]\?[,.])*',token):       #if numbers have currency $
         #   print "case 2 matched"
            add_unigram_to_list('$',"2",token)
            add_unigram_to_list(token[1:],"2",token)
        
    elif re.match('[0-9]{,2}[-/][0-9]{,2}[-/][0-9]{2,4}',token):  #dates like 18-12-1990
        #    print "case 3 matched"
            add_unigram_to_list(token,"3",token)
        
    elif re.match('[0-9]+\W',token):             #special characters have to be separated
        #    print "case 4 matched"
            #pattern =re.compile('\W')
            list1= re.findall(r"[\d']+", token)
            for word in list1:
                add_unigram_to_list(word,"4",token)
            list2= re.findall(r"[\W']+", token)
            for word in list2:
                add_unigram_to_list(word,"4",token)
        
    elif re.match('www.',token):                 #for urls
        #    print "case 5 matched"
            add_unigram_to_list(token,"5",token)
            
    elif re.match('[a-zA-Z._]+@[a-zA-Z]+\.[a-zA-Z]+',token): #for emails
        #    print "case 6 matched"
            add_unigram_to_list(token,"5",token)
            
    elif re.match("([A-Z][.])+",token):          #For words like U.S.A.
         #       print "case 7 matched"  
                add_unigram_to_list(token,"6",token)
                
    elif re.match("([A-Z][a-z][.])+",token):     #For words like Dr. ,Mr. ,Ph.D
        #        print "case 8 matched"
                add_unigram_to_list(token,"7",token)
    elif re.match("[\w][.,]",token):
             add_unigram_to_list(token,"7",token)
             
    #elif re.match("[\w]+'s\\b", token) :         #for words like Joe's
    elif re.match("[\w]+'s", token) :         #for words like Joe's

        list1=token.split("'s")
        if len(list1) >0 :
            add_unigram_to_list(list1[0],"8",token)
            add_unigram_to_list("'s","8",token)
            
        
        
    elif re.match("(\w*\W*)*",token):     #For any other special characters at end example (a)). will be broken into (, a,),) 
        list1= re.findall(r"[\w]+", token)
        for word in list1:
            add_unigram_to_list(word,"9",token)
        list2= re.findall(r"[{}().;,!\[\]*'\"/|\-\+%]+", token)
        for seq in list2:
            list_seq=list(seq)
            for word in list_seq:
                add_unigram_to_list(word,"9",token)
    else :
            add_unigram_to_list(token,"10",token)
            
    
def sort_descending(unigrams):
    return sorted(unigrams.items(), key=operator.itemgetter(1), reverse=True)
    
def plot(x,y):

    
    plt.plot(x, y)
    plt.xlabel('rank')
    plt.ylabel('frequency')
    #show plot
    plt.show()

def find_x_y_for_plotting(ranked_list,unigrams_dict):
    dict_plot={}
    f1=open("output.txt", "w")
    for i in range(len(ranked_list)):
     #  print i
        word=ranked_list[i][0]                #fetching the word string from ranked list
     #   print word
        dict_plot[i+1]=unigrams_dict[word][0] #finding the frequency of word from unigrams_dict
        f1.write(word+"\t\t:\t"+str(unigrams_dict[word][0])+"\n")
    
    f1.close()
    return dict_plot
            
    
if __name__ == "__main__": 
    f1=open("English_sample.txt","r") #file to read
    unigrams_dict={}                  #Dictionary to hold unigrams and its count
    dict_plot={}                      #x=key=rank,y=value=frequency
    i=1
    for line in f1:
        if i%1000==0:
            print i
        i=i+1
        tokens=line.rstrip().split()
        for token in tokens :
            find_unigrams(token)
    ranked_list=sort_descending(unigrams_dict)  #key=word,value=frequency
    dict_plot=find_x_y_for_plotting(ranked_list,unigrams_dict)
    plot(dict_plot.keys()[:50],dict_plot.values()[:50]) #display for only 50 ranks
    plt.show()
                
    

