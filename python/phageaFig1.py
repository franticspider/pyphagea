"""
    Copyright (C) 2013-2015 Simon Hickinbotham, Hywl Williams, Susan Stepney
    
    This file is part of Phagea.

    Phagea is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Phagea is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Phagea.  If not, see <http://www.gnu.org/licenses/>.

"""


"""
#need to 
#      export JAVA_HOME=/usr/lib/jvm/default-java 
#before running
#import jpype
"""
#

from jpype import *# JPackage, startJVM, shutdownJVM

#TODO: change this path...
#classpath = "-Djava.class.path=/home/sjh/Desktop/sjh/phagea/workspace/PhagEA/bin/" 
#classpath = "-Djava.class.path=/home/sjh/workspace/PhagEApype/jar/" 

#Specify the path to the phagea java classes:
classpath = "-Djava.class.path=/home/sjh/git/phagea/src/"

#Specify the path to the jvm: 
jvmpath = "/usr/local/java/jdk1.8.0_25/jre/lib/amd64/server/libjvm.so"#"/usr/lib/jvm/default-java/jre/lib/i386/client/libjvm.so"
#classpath = "-Djava.class.path='.'" 
#"-ea -Djava.class.path=C:\\Documents and Settings\\Sydney\\Desktop\\jpypeTest\\"
startJVM(jvmpath,"-ea",classpath)

# test: access the basic java functions
java.lang.System.out.println("JPype has connected to the JVM successfully (I think)")

 
import matplotlib.pyplot as plt



##########################################################
# TESTING NETWORKX
import networkx as nx
import matplotlib.cm as cmx
import matplotlib.colors as colors



import numpy as np

from numpy.core.numeric import zeros
""" there's a sqrt error in plot - this can trap it:   """
#np.seterr(invalid='raise')


##########################################################

#TODO: Not sure if I need this:
#import sys

testPkg = JPackage("com").phagea
Test = testPkg.TestPype
Test.speak("hi")
t = Test()
print t.getString()

print '=============================='
print '====STARTING PHAGEA PROPER===='
print ''


""" Create class variables that we'll get the objects from """
cfc = JClass("com.phagea.phageaConfig")
plc = JClass("com.phagea.phageaLandscape")



"""
Let's define a function that runs a simulation and plots it, given only the config and the image name
"""

def plotsim(cf,outfn):
    
    #load the landscape
    pl = plc(cf)
    
    ndims = pl.getNdims();
    if ndims == 1:
        #this used to work, but no longer!
        #mylandscape = JArray(JFloat,1)(pl.get1DLandscape())
        #nowadays, we can do it like this:
        landscape = pl.get1DLandscape()
        #pl.get1DLandscape()
    else: 
        if ndims == 2:
            landscape = pl.get2DLandscape()
        else:
            print 'Ndims = ',ndims, ' ...no landscape created yet (in python)'
    
    #cf.setInitFit(pl.getNdims(),pl.getMaxValue(),pl.getMinValue())
    
    pec = JClass("com.phagea.phageaEngine")
    pe = pec(cf,pl)
    
    pe.print_stats(0)
    pe.runAlgorithm()
    
    #DO THE PLOTTING NOW:
    plt.figure()
    
    #Data for the subtitle:
    w = cf.getrOmega()
    Rgamma = cf.getrGamma()
    Repsilon = cf.getrEpsilon()
    Theta = cf.getTheta()
    
    if ndims == 1:
        print "Preparing 1D plot"
    
        pst = 'W= %f'%cf.getrOmega()+' Rgamma= %f'%cf.getrGamma()+' Repsilon= %f'%cf.getrEpsilon()+' Theta= %f'%cf.getTheta()
        plt.suptitle(pst)
    
        print 'Plotting Cell Histogram'
        plt.subplot(231)
        CellHist =  pe.getCellHist()
        plt.imshow(CellHist, origin = 'lower' ,aspect='auto', label='cell')
        
        print 'Plotting Phage Histogram'
        plt.subplot(232)
        PhageHist = pe.getPhageHist()
        plt.imshow(PhageHist, origin = 'lower' ,aspect='auto', label='phage')
        
        print 'Plotting Landscape'
        plt.subplot(233)
        FitMap = pl.get1DLandscape()
        nbin = cf.getNbin()
        xx = zeros(nbin)
        print 'nbin= ',nbin,' FitMap size = ',len(FitMap)
        for i in range (0,nbin):
            xx[i] = i
        plt.plot(FitMap,xx,label = "fitness")
        
        print 'Plotting Cell Popdy'
        plt.subplot(234)
        cellpopdy = pe.getCellPopdy()
        plt.plot(cellpopdy)
        
        print 'Plotting Phage Popdy'
        plt.subplot(235)
        phagepopdy = pe.getPhagePopdy()
        plt.plot(phagepopdy)
        
        print 'Plotting Resource Dynamics'
        plt.subplot(236)
        rdy = pe.getRDy()
        plt.plot(rdy)
    
    elif ndims == 2:
        print "Preparing 2D plot"
        pst = 'w='+'{:.1e}'.format(w)+' Rgamma='+"{:.1e}".format(Rgamma)+'\n Repsilon='+"{:.1e}".format(Repsilon)+' theta='+"{:.1e}".format(Theta)
        plt.suptitle(pst)
    
    
        print 'Plotting Cell Histogram'
        plt.subplot(231)
        CellHist =  pe.getCellHist()
        plt.imshow(CellHist, origin = 'lower' ,aspect='auto', label='cell')
        
        print 'Plotting Phage Histogram'
        plt.subplot(232)
        PhageHist = pe.getPhageHist()
        plt.imshow(PhageHist, origin = 'lower' ,aspect='auto', label='phage')
        
        print 'Plotting Landscape'
        plt.subplot(233)
        plt.imshow(landscape, origin = 'lower' ,aspect='auto', label='landscape')
        
        print 'Plotting Cell Popdy'
        plt.subplot(234)
        cellpopdy = pe.getCellPopdy()
        plt.plot(cellpopdy)
        
        print 'Plotting Phage Popdy'
        plt.subplot(235)
        phagepopdy = pe.getPhagePopdy()
        plt.plot(phagepopdy)
        
        print 'Plotting Resource Dynamics'
        plt.subplot(236)
        rdy = pe.getRDy()
        plt.plot(rdy)
    
    else:
        print "TODO: Prepare N-Dimensional plot"
        
    
    
    #newname = cfgfile.replace('.cfg', '.png')
    plt.savefig(outfn)    
    plt.close()
    #newname = cfgfile.replace('.cfg', '.pdf')
    #plt.savefig(newname,format='pdf')    
    
    
    print'FINISHED'
    print'==============================='
    
    return










print '=================================='
print '==== STARTING NEW PHAGEA 2D EXPTS ===='

#Load the config
cfgfile = sys.argv[1]
cf = cfc(cfgfile)

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(False)
cf.setRescaling(False)
cf.setReplenish(False)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRFFF.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(False)
cf.setRescaling(False)
cf.setReplenish(True)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRFFT.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(False)
cf.setRescaling(True)
cf.setReplenish(False)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRFTF.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(False)
cf.setRescaling(True)
cf.setReplenish(True)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRFTT.png")

cf.setRandInit(True)
cf.setRescaling(False)
cf.setReplenish(False)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRTFF.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(True)
cf.setRescaling(False)
cf.setReplenish(True)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRTFT.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(True)
cf.setRescaling(True)
cf.setReplenish(False)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRTTF.png")

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
cf.setRandInit(True)
cf.setRescaling(True)
cf.setReplenish(True)
plotsim(cf,"/home/sjh/Desktop/Dropbox/Hywl/2015/runs/outfilenRTTT.png")


shutdownJVM()

