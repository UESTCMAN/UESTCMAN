#coding:utf-8
#author:Anthony Simon
#site: https://uestcman.github.io
#�뽫���ļ�����mkdocs��Ŀ��Ŀ¼
import sys
import ConfigParser
import time
import os
import shutil
import yaml
class CheckStructure():
    def __init__(self):
        global systemPath
        systemPath=os.path.split(os.path.abspath(__file__))[0]
        self.systemPath=systemPath
        self.checkDir()
    @classmethod
    def checkDir(cls):
        fatherDir=systemPath
        Dir=["/docs","/site",'/config','/md']
        for sonDir in Dir:
            cls.creatDir(fatherDir,sonDir)
        '''
        #html����Ľṹ
        fatherDir=systemPath+'/html'
        Dir=["/article",'/series','/pic','/ftp']
        for sonDir in Dir:
            cls.creatDir(fatherDir,sonDir)
        #md����Ľṹ
        fatherDir=systemPath+'/md'
        Dir=['/'+TheTime().year]
        for sonDir in Dir:
            cls.creatDir(fatherDir,sonDir)
        '''
    @classmethod
    def creatDir(cls,fatherDir,sonDir):
        if os.path.exists(fatherDir):
            if os.path.exists(fatherDir+sonDir):
                pass
            else:
                os.makedirs(fatherDir+sonDir)
        else:
            print "����Ŀ¼ʱ��Ŀ¼������!"


class ConfigFile():
    '''
    Ӧ����CheckStructureʵ������ʵ����
    '''
    def __init__(self):
        self.configPath=systemPath+'/config'
        self.configFilePath=self.configPath+'/system.conf'#������Ҫ�����Ż�������ֻ�����ض��ļ����ڴ���system.conf
        self.checkExist()
        config=ConfigParser.ConfigParser()
        config.read(self.configFilePath)
        self.config=config
    def checkExist(self):
        configPath=self.configPath
        if (os.path.exists(self.configFilePath)):
            if (os.path.isfile(self.configFilePath)):
                pass
            else:
                self.creatConfigFile(self.configFilePath)             
        else:
            self.creatConfigFile(self.configFilePath)
    @classmethod
    def creatConfigFile(cls,targetPath):
        content='''
[system]
welcomeMessage=True
[series]
[auto]
build=True
deploy=True

        '''
        choice=raw_input("δ���������ļ�,�Ƿ񴴽��µ������ļ���y/n\n")
        if choice=="Y"or choice=="y":
            with open(targetPath,'w')as f:
                f.write(content)
            print "�������µ������ļ�"
        else:
            exit()
    def getConfig(self,section,key):
        self.config.get(section,key)
        self.updateConfig()
    def setConfig(self,section,key,value):
        self.config.set(section,key,value)
        self.updateConfig()
    def addSection(self,newSection):
        if not self.hasSection(newSection):
            self.config.add_section(newSection)
            self.updateConfig()
    def hasSection(self,section):
        return self.config.has_section(section)
    def hasOption(self,section,option):
        return self.config.has_option(option)
    def TrueOrFalse(self,section,key):
        if self.config.get(section,key) in ["True","true"]:
            return True
        else:
            return False
    def updateConfig(self):
        with open(self.configFilePath,'w')as f:
            self.config.write(f)





class TheTime():
    def __init__(self):
        now=time.localtime()
        self.time=time.time()
        self.year=time.strftime("%Y", now)
        self.month=time.strftime("%m", now)
        self.month_s=time.strftime("%B", now)
        self.day=time.strftime("%d", now)
        self.week=time.strftime("%a",now)
    def year_month_day(self):
        global year_month_day
        year_month_day="%s-%s-%s"%(self.year,self.month,self.day)
        return year_month_day
class Information():
    def welcome(self):
        welcomeInformation='''
        Welcome to use mkdocs-plus!
        '''
        if ConfigFile().TrueOrFalse('system','welcomemessage'):
            print welcomeInformation
    def toHelp(self):
        helpInformation='''
        -h:display this help information

        '''
        print helpInformation
    def ParameterFalse(self):
        FalseInformation='''
        Error:The Parameter you input is an Unknown Command
        usage: [command]
        for more information please input command h
        '''
        print  FalseInformation

class blog():
    def newpage(self):
        self.series="daily"
        precontent='''














notes:
compose on the top of these words plz
please write title on the first line
and do not delete these words
'''
        with open(systemPath+"/md/"+TheTime().year_month_day()+".md",'w')as f:
            f.write(precontent)
        try:
            os.system("vim "+systemPath+"/md/"+TheTime().year_month_day()+".md")
        except:
            print"����vimʧ��"
        f=open(systemPath+"/md/"+TheTime().year_month_day()+".md",'r')
        self.newpageTitle=f.readline().strip().lstrip().rstrip()#��ҪΪ���ң�����������ò�Ҫ�����ַ�
        newseries=f.readline().strip().lstrip().rstrip()#�ڶ���д����������ϵ��
        f.close()
        if newseries!="":
            self.series=newseries
        if self.newpageTitle=="":
            self.newpageTitle=TheTime().year_month_day()
        try:
            shutil.copy(systemPath+"/md/"+TheTime().year_month_day()+".md",systemPath+"/docs/"+self.newpageTitle+".md")#�����ļ�
        except:
            print "�����ļ���docsĿ¼ʧ�ܣ�����������ڱ�������������"
        #self.addConfig()#д�����µ�����
        if ConfigFile().TrueOrFalse('auto','build'):
            self.build()
        if ConfigFile().TrueOrFalse('auto','deploy'):
            self.deploy()
    
    def addConfig(self,thetype):
        self.readYml()
        if thetype=='':
            pass
        print self.ymlContent
        self.writeYml()

    def readYml(self):
        f=open(systemPath+"/mkdocs.yml")
        self.ymlContent=yaml.load(f)
        print self.ymlContent
        f.close()
        self.writeYml()
    
    def writeYml(self):
        f=open(systemPath+"/mkdocs.yml",'w')
        yaml.dump(self.ymlContent,f)
        f.close()
    def server(self):
        try:
            print "ctrl c�˳�������"
            os.system("mkdocs serve")
        except:
            print"�������ѹر�"
    @classmethod
    def build(cls):
        try:
            os.system("mkdocs build")
        except:
            print "����mkdocsʧ��"
    @classmethod
    def deploy(cls):
        try:
            os.system("git add .")
            os.system("git commit -m"+"'"+TheTime().year_month_day()+"'")
            os.system("git push origin master -f")#�Ƚ�Σ�գ�ע�Ᵽ���Լ��Ĳֿ⣡
        except:
            print "git����ʧ��!"


def exeThePa(inputPa):
    if inputPa in ["h","H","Help","-h","-H","-Help","help"]:
        Information().toHelp()
    elif inputPa in ['new','newpage','n','-n']:
        blog().newpage()
    elif inputPa in ['']:
        pass
    elif inputPa in ['exit','e','Exit','-e']:
        exit()
    elif inputPa in ['yaml','yml']:
        blog().readYml()
    elif inputPa in ['s','server','serve']:
        blog().server()
    else:
        Information().ParameterFalse()

def main():
    CheckStructure()
    ConfigFile()
    Information().welcome()
    while(True):
        inputPa=raw_input("what to do next? ") #��ȡ�������
        exeThePa(inputPa)
main()
