__author__ = 'wanguan2000'
#coding=utf-8
import os.path
import os
import sys
import re

class StringMeth:
    def getPathName(self, path):
        return os.path.splitext(os.path.basename(path))[0]

    def changeExtension(self, filename, extension):
        return os.path.join(os.path.splitext(filename))[0] + extension

    def changeName(self, filename, suffix):
        name = os.path.split(filename)[1]
        pattern2 = re.compile(r'_.*')
        return os.path.join(os.path.split(filename)[0], pattern2.sub(suffix, name))


class Const(object):
    def __init__(self, data):
        self.__dict__.update(data)

    def __setattr__(self, name, value):
        raise Exception, "Error Can't rebind const"

    def __getattr__(self, name):
        return self.__dict__.get(name)


class Init_Pipeline():
    def doInit(self, myconfig):
        #must input your config file!!!!!#############
        sys.path.insert(0, os.path.split(myconfig)[0])
        modfile = os.path.splitext(os.path.basename(myconfig))[0]
        mod = __import__(modfile)
        mydict = dict([(x, getattr(mod, x)) for x in dir(mod) if not x.startswith('__')])
        #add tmp folder
        mydict['Temp_Folder'] = os.path.join(mydict['Output_Folder'], 'Temp')
        const = Const(mydict)


        return  const


'''
mydict={'a':1}
const = Const(mydict)
print const.a

path = '/home/wanguan2000/pg/myNGS/inputfile_NGS/s1/adsahd_asd_fastq.txt'
m1 = StringMeth()

print path.split('/')[-1].split('.')[0]
print m1.getPathName(path)
print m1.changeExtension(path,'.exe')
print m1.changeName(path,'_chang.txt')
print os.path.join(os.path.splitext(path))[0]




extension = 'bam'
filename = 'database_NGS/hg19fastadatabase/ucsc.hg19.fasta'
print re.compile(r'[.].*?$').sub(extension, filename)
print filename.split('.')[-1]
print '.'.join(filename.split('.')[:-1])+'.'+extension



__author__ = 'wanguan2000'

class Const(object):
    def __init__(self, data):
        self.__dict__.update(data)

    def __setattr__(self, name, value):
        raise Exception, "Error"

    def __getattr__(self, name):
        return self.__dict__.get(name)

if __name__ == '__main__':
    a = {'a':1, 'b':2}
    const = Const(a)
    print const.a

    class B(object):
        def __init__(self, const):
            self.const = const

        def p(self):
            print self.const.a

    b = B(const)
    b.p()


'''
