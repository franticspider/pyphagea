


import sys  
from jpype import JClass
import JPypeUtils as ut
import PyPhagea as pyph


ut.setupJPype()


""" Create class variables that we'll get the objects from """
cfc = JClass("com.phagea.phageaConfig")



print '=================================='
print '==== STARTING NEW PHAGEA 2D EXPTS ===='

#Load the config
cfgfile = sys.argv[1]
cf = cfc(cfgfile)

#CREATE THE DIFFERENT CONFIGURATIONS WE ARE INVESTIGATING
pyph.plotsim(cf,"outfilenRFFF.png")


ut.stopJPype()
