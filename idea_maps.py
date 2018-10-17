# -*- coding: utf-8 -*-
"""
This code is used to find idea maps from triplet responses
and calculate novelty.

It uses MATLAB code from https://lvdmaaten.github.io/ste/Stochastic_Triplet_Embedding.html
to find embedding

@author: faez

"""

from shutil import copyfile
import sys
from subprocess import call
import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

def centeroidnp(arr):
    """
    centroid of X
    
    """
    
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    
    return sum_x/length, sum_y/length
    
def disfrompoint(X):
    """
    Find novelty ranking based on distance from centroid
    
    """
    
    cen=centeroidnp(X)
    cen=np.array(cen).reshape((1,2))
    d=cdist(cen,X)

    return (np.argsort(d)[0])[::-1]

def triplet_satisfied(X, matr):
    """
    This function finds number of triplets satisfied by any given X coordinates
    X is nx2 matrix denoting 2-D position of n points
    matr is mx3 matrix with m triplets.
    
    """
    newtriplet=np.copy(matr)
    
    csat=0.0
    numtriplets=len(matr)
    for i in range(numtriplets):
       d1=X[matr[i,1]]-X[matr[i,0]]
       d2=X[matr[i,2]]-X[matr[i,0]]
       
       if((np.linalg.norm(d1))>(np.linalg.norm(d2))):
           csat=csat+1
           newtriplet[i,2]=matr[i,1]
           newtriplet[i,1]=matr[i,2]
    #csat is number of triplets not satisfied.
    #new triplet is triplet responses which satisfy the map     
    print "Percentage of triplets not satisfied", csat/numtriplets       
    return csat,newtriplet


def plot_sketch(X,thumbfile,sfx,f1,f2):
    #plot sketches overlaid at positions given by X
    
    fig = plt.figure(figsize=(f1,f2), dpi=80)
    

    plt.hold('True')

    
    a,b = np.min(X,axis=0)
    c,d = np.max(X,axis=0)
    
    X1=np.copy(X)
    X1[:,0]=(X1[:,0]-a)/(c-a)
    X1[:,1]=(X1[:,1]-b)/(c-a)

    
    prefx='s'
    
    for i in range(len(X)):
    
        im = Image.open(thumbfile+'/%d.jpg'%i)
        
        size = 85, 130
        im.thumbnail(size)

        
        im = ImageOps.expand(im,border=2,fill='black')
        img = im.convert("RGBA")
        
        datas = img.getdata()
        
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)

        
        xcoord=1+X1[i,0]*(fig.bbox.xmax)*0.85
        ycoord=1+X1[i,1]*(fig.bbox.ymax)*0.85
        
        
        fig.figimage(img, xcoord, ycoord, zorder=2)
        plt.axis('off')
        
    fig.savefig('output/{}_{}.png'.format(prefx,sfx), dpi=100)
        

def findnovel():
    
    """
    reads x coordinates, finds distance matrix and item novelty
    
    """

    X=np.loadtxt('output/xx.txt') 
    Z=squareform(pdist(X, 'euclidean'))    
    
    nov=np.sum(Z, axis=0)
    nov_sort=np.argsort(nov)
    
    print 'Most novel items using sum of embedding distances', nov_sort[-10:][::-1]

    #print "Metric novelty scores are", nov
    
    print "Most novel items using novelty calculated as distance from centroid", disfrompoint(X)
    
    return X, Z, nov_sort[-10:][::-1], nov

def runmatlab(filname):
    
    """
    Run main.m MATLAB code to find embedding from triplet responses
    
    """
    

    copyfile(filname, 'output/triplet_response.txt')
    
    try:
        sinp="matlab -nodisplay -nosplash -nodesktop -r \"run('main(4)');exit;\""

        retcode = call(sinp, shell=True)

        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e

def find_embedding(filname):
    
    
    """
    Run matlab to find embedding. MATLAB should be installed on the system.    
    The resulting coordinates are written in xx.txt file.
    Using the coordinates, novelty is calculated.
    """
    runmatlab(filname)
    
    
    
    #Find novelty of items
    X, Z, nov_sort, nov=findnovel()
    
    return X, nov_sort
    


if __name__=="__main__":
    
    """
    Code to find embedding and calculate novelty from the paper
    
    "Interpreting Idea Maps: Pairwise comparisons reveal what makes ideas novel"
    
    To use your own dataset, upload the new sketches in the sketches folder and 
    upload triplet responses in "input.txt" 
    
    """
    
    #File containing triplet responses
    #Rater id 10 in Experiment 2--- Fig. 7b should be reproduced
    filname='input.txt'
    
    #Folder containing sketches
    thumbfile='sketches'
    
    #Find embedding coordinates and novelty score
    #X is the 2-D coordinates of each item
    #nov_sort is the novelty ranking with 0 being most novel
    
    X, nov_sort=find_embedding(filname) 
        
    #Plot idea map on a 2-D map.
    plot_sketch(X,thumbfile,0,9,6)
    
    print "Percentage of triplets not satisfied by embedding", np.loadtxt('output/er.txt')[0]
    
    print "Number of transitive violations", np.shape(np.loadtxt('output/wrongmatr.txt'))[0]
    
    

