"""
    Copyright (C) 2013-2015 Simon Hickinbotham, Hywl Williams, Susan Stepney
    
    This file is part of pyphagea.

    pyphagea is free software: you can redistribute it and/or modify
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
 
import matplotlib.pyplot as plt



##########################################################
# TESTING NETWORKX
#import networkx as nx
#import matplotlib.cm as cmx
#import matplotlib.colors as colors



#import numpy as np
#from numpy.core.numeric import zeros


"""
Run a simulation and plot it, given only the config and the image name
"""

def plotsim(cf,outfn):
    
    from jpype import JClass as JClass
    plc = JClass("com.phagea.phageaLandscape")
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


    #test this now before we run the bloody thing
    mean_cell_population = pe.getMeanCellPop(1000)
    print "Mean Cell Population is "
    print mean_cell_population   


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

    #newname = cfgfile.replace('.cfg', '.pdf')
    #plt.savefig(newname,format='pdf')    
    

    #close the plot to stop gtk issuing "Warning: Source ID 6 was not found when attempting to remove it"
    plt.close()

    #print some statistics
    mean_cell_population = pe.getMeanCellPop(1000)
    print "Mean Cell Population is "
    print mean_cell_population   
    
    return





