import sys
sys.path.append("/home/database/TFDesignWeb/Services")
import os
# from GGModule.SupportGG import SupportGG
from GGModule.SupportGG import SupportGG
import pymysql
import os
# from ControllerModule import ParseGenBankFileGetName,WriteGBKFileWithoutC
from snapgene_reader import snapgene_file_to_seqrecord
from Bio.SeqIO import parse,write
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from AssemblyFunction import Caculate
from Entity.Part import GetPartByName
from Entity.Backbone import Backbone,GetBackbone
from Entity import LBD,DBD
from six.moves import urllib


DOWNLOAD_FILEADDRESS = "/home/database/WebPlot/UPLOAD_FOLDER/SequenceFile"
class WebAssembly:
    def __init__(self,LBD,DBD,L,api_url,session):
        self.LBD = GetPartByName(api_url,LBD,session)
        self.DBD = GetPartByName(api_url,DBD,session)
        # self.Level2Backbone = "CY571"
        self.Level2Backbone = GetBackbone(api_url,"CY571")
        # self.Level3Backbone = "CY1809"
        self.Level3Backbone = GetBackbone(api_url,"CY1809")
        self.L = L
        # self.promoter = "pxyluas"
        # self.Terminator = "TER25"
        # self.AD = "AD"
        self.AD = GetPartByName(api_url,"AD",session)


    def CaculatePT(self):
        cal = Caculate.Caculate(self.DA.GetCursor(),self.L)
        result = cal.CaculateFunction()
        self.promoter = result[0]
        self.terminator = result[1]
        print(self.promoter.Name)
        print(self.terminator.Name)        
    def downloadfile(filepath):
        filename = filepath.split('/')[-1]
        savepath = os.path.join(DOWNLOAD_FILEADDRESS,filename)
        urllib.request.urlretrieve(filepath,savepath)
        return savepath


    def AssemblyFuntion(self):
        self.CaculatePT()
        PartList = [self.promoter,self.LBD,self.DBD,self.AD,self.terminator]
        print(self.promoter.Name)
        FileAddressList = []
        FileNameList = []
        FileWithoutAddress = []
        FileWithoutAddressindex = []
        try:
            for part in PartList:
                PartAddress = part.GetFileAddress(self.DA.GetCursor())
                if(PartAddress != None):
                    filesavepath = self.downloadfile(PartAddress)
                    FileAddressList.append(filesavepath)
                    FileFormat = ""
                    if(os.path.splitext(filesavepath)[-1][1:] == "fasta"):
                        FileFormat = "fasta"
                    elif(os.path.splitext(filesavepath)[-1][1:] == "gb" or os.path.splitext(PartAddress)[-1][1:] == "gbk" or os.path.splitext(PartAddress)[-1][1:] == "ape" or os.path.splitext(PartAddress)[-1][1:] == "str"):
                        FileFormat = "genbank"
                    elif(os.path.splitext(filesavepath)[-1][1:] == "dna"):
                        FileFormat = "snapgene"
                    Name = self.ParseGenBankFileGetName(filesavepath,FileFormat)
                    FileNameList.append(Name)
                else:
                    FileWithoutAddress.append(part)
                    FileWithoutAddressindex.append(0)
            # BackboneAddress = str(ManageSql.getFileAddress(1,"root",self.Level2Backbone,self.connection, self.cur))
            BackboneAddress = self.Level2Backbone.GetFileAddress(self.DA.GetCursor())
            if(BackboneAddress != None):
                filesavepath = self.downloadfile(BackboneAddress)
                FileAddressList.append(filesavepath)
                AddressSuffix = os.path.splitext(filesavepath)[-1][1:]
                FileFormat = ""
                if(AddressSuffix == "fasta"):
                    FileFormat = "fasta"
                elif(AddressSuffix == "gb" or AddressSuffix == "gbk" or AddressSuffix == "ape" or AddressSuffix== "str"):
                    FileFormat = "genbank"
                elif(AddressSuffix == "dna"):
                    FileFormat = "snapgene"
                Name = self.ParseGenBankFileGetName(filesavepath,FileFormat)
                FileNameList.append(Name)
            else:
                FileWithoutAddress.append(self.Level2Backbone)
                FileWithoutAddressindex.append(1)
            i = 0
            for part in FileWithoutAddress:
                savefileaddress = self.WriteGBKFileWithoutC(part,FileWithoutAddressindex[i],self.DA.GetCursor())
                FileAddressList.append(savefileaddress)
                FileNameList.append(part.Name)
                i = i+1
            print(FileNameList)
            print(FileAddressList)
            GG = SupportGG(FileAddressList, FileNameList)
            GG.assemblyPart("Level2")
            GG.show()
            FileAddressList = []
            FileNameList = []
            FileWithoutAddress = []
            FileWithoutAddressindex = []
            Level2FileAddress = r"/home/database/output/Level2.gb"
            FileAddressList.append(Level2FileAddress)
            Name = self.ParseGenBankFileGetName(Level2FileAddress,"genbank")
            FileNameList.append(Name)
            # BackboneAddress = str(ManageSql.getFileAddress(1,"root",self.Level3Backbone,self.connection, self.cur))
            BackboneAddress = self.Level3Backbone.GetFileAddress(self.DA.GetCursor())
            if(BackboneAddress != None):
                savefileaddress = self.downloadfile(BackboneAddress)
                FileAddressList.append(savefileaddress)
                AddressSuffix = os.path.splitext(savefileaddress)[-1][1:]
                FileFormat = ""
                if(AddressSuffix == "fasta"):
                    FileFormat = "fasta"
                elif(AddressSuffix == "gb" or AddressSuffix == "gbk" or AddressSuffix == "ape" or AddressSuffix== "str"):
                    FileFormat = "genbank"
                elif(AddressSuffix == "dna"):
                    FileFormat = "snapgene"
                Name = self.ParseGenBankFileGetName(savefileaddress,FileFormat)
                FileNameList.append(Name)
            else:
                FileWithoutAddress.append(self.Level3Backbone)
                FileWithoutAddressindex.append(1)
            i = 0
            for part in FileWithoutAddress:
                savefileaddress = self.WriteGBKFileWithoutC(part,FileWithoutAddressindex[i],self.DA.GetCursor())
                import sys
                # FileAddress = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))),part.Name+".gbk")
                self.ParseGenBankFileGetName(savefileaddress,"genbank")
                FileAddressList.append(savefileaddress)
                FileNameList.append(part.Name)
                i = i+1
            GG = SupportGG(FileAddressList, FileNameList)
            GG.assemblyPart("Level3")
            GG.show()
        except pymysql.err.OperationalError as e:
            print(e)


    def ParseGenBankFileGetName(self,file,format):
        if(format == "snapgene"):
            record = snapgene_file_to_seqrecord(file)
            Name = record.name
            return Name
        else:
            records = parse(file, format)
            # if(len(records) > 1):
            #     return "Error"
            # else:
            for record in records:
                return record.name
    

    def WriteGBKFileWithoutC(self,Component, index,cur):
        CurrentSeq = ""
        if(index == 0):
            CurrentSeq = Component.Level0Sequence
        elif(index == 1):
            CurrentSeq = Component.Sequence
        elif(index == 2):
            CurrentSeq = Component.Sequence
        FileName = DOWNLOAD_FILEADDRESS + Component.Name + ".gbk"
        SeqObject = Seq(CurrentSeq)
        record = SeqRecord(SeqObject, id=Component.Name,name = Component.Name, description="for WebAssembly")
        record.annotations = {"molecule_type": "DNA", "topology": "circular"}
        write(record, FileName, "genbank")
        return FileName


# if __name__ == "__main__":
#     FileName = DOWNLOAD_FILEADDRESS + "temp" + ".gbk"
#     SeqObject = Seq("AAAATTTTCCCCGGGGGCAAATTCCCGGGATCGCTAGC")
#     record = SeqRecord(SeqObject, id="temp",name = "temp", description="temp generate")
#     record.annotations = {"molecule_type": "DNA", "topology": "circular"}
#     write(record, FileName, "genbank")
