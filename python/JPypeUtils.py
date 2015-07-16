"""
    Copyright (C) 2013-2015 Simon Hickinbotham, Hywl Williams, Susan Stepney
    
    This file is part of PyPhagea.

    PyPhagea is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyPhagea is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Phagea.  If not, see <http://www.gnu.org/licenses/>.

"""




def setupJPype():

    from jpype import startJVM    

    #Specify the path to the phagea java classes:
    classpath = "-Djava.class.path=/home/sjh/git/phagea/src/"

    #Specify the path to the jvm: 
    jvmpath = "/usr/local/java/jdk1.8.0_25/jre/lib/amd64/server/libjvm.so"#"/usr/lib/jvm/default-java/jre/lib/i386/client/libjvm.so"
    #classpath = "-Djava.class.path='.'" 
    #"-ea -Djava.class.path=C:\\Documents and Settings\\Sydney\\Desktop\\jpypeTest\\"
    startJVM(jvmpath,"-ea",classpath)


def stopJPype():
    from jpype import shutdownJVM    
    shutdownJVM()
