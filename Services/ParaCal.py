#使用sameLBD，diffLBD对参数进行拟合
#然后存储在TFDatabase.xlsx   

#先跑Diff，再跑Same  
#将Diff的K1，k2，k3作为静态变量
#static
import sameLBD
import TFDesignWeb.Services.DiffLBD as DiffLBD
import pandas as pd
from Entity import DBD,LBD
from os import listdir
# def EXCELAppend(Type,value):
    # file_path = '/T18/weiboyan/WebPlot/TFDatabase.xlsx'
    # df = pd.read_excel(file_path,sheet_name=Type,engine="openpyxl")
    # workbook = openpyxl.load_workbook(file_path)
    # ws = workbook[Type]
    # valueslist = list(value.values())
    # print(valueslist)
    # DFValue = pd.DataFrame([value])
    # ws.append(valueslist)
    # # print(row)
    # workbook.save(file_path)
    # workbook.close()
    # row = df.shape[0]
    # writer = pd.ExcelWriter(file_path,engine="openpyxl")
    # DFValue = pd.DataFrame([value])
    # DFValue.to_excel(writer,sheet_name=Type,startrow=row+1,header=False,index=False)
    # # workbook.save(file_path)
    # writer.close()
    # # workbook.close()  
    # print(df)
def GetKd(cur,DBDName):
    return DBD.GetDBDKd(cur,DBDName)

def AnalysisExcel(conn,cur):
    # FileAddress = './UPLOAD_FOLDER/Data.csv'
    folderAddress = r'./UPLOAD_FOLDER/Data'
    files = listdir(folderAddress)
    dataframe = pd.DataFrame()
    for file in files:
        FileAddress = folderAddress + "/"+file
        dataframe.append(pd.read_csv)
        # dataframepd.read_csv(FileAddress)
    All_Data = pd.DataFrame(columns=['LBD','inducer','I0','Imax','RPU'])
    row = dataframe.shape[0]
    # print(All_Data)
    SperAllData = []
    LBDDataGroups = dataframe.groupby(["LBDName"])
    FixLBDName = list(LBDDataGroups.groups.keys())[0]
    #提取所有LBDName列为FixLBDName的项
    DBDData = dataframe[dataframe['LBDName'] == FixLBDName]
    sameDBDData = DBDData.groupby(["DBDName"])
    DBDNameList = list(sameDBDData.groups.keys())
    for DBDName in sameDBDData.groups:
        # print(DBDName)
        IndexList = sameDBDData.groups[DBDName].to_list()
        PreData = pd.DataFrame(columns=['LBD','inducer','I0','Imax','RPU'])
        for eachIndex in IndexList:
            temp = dataframe.iloc[eachIndex,[2,3,5,6,4]]
            All_Data.loc[len(All_Data.index)] = temp
            PreData.loc[len(PreData.index)] = temp
            # PreData = pd.concat([PreData,dataframe.iloc[eachIndex,[2,3,6,4]]])
            # PreData = pd.concat([PreData,pd.DataFrame(dataframe.iloc[eachIndex,:]['LBD','inducer','I0','RPU'])],ignore_index=True)
            # PreData = pd.concat([PreData,dataframe.iloc[eachIndex,['LBD','inducer','I0','RPU']]],ignore_index=True)
        SperAllData.append(PreData)
    FixDBDName = DBDNameList[0]
    LBDData = dataframe[dataframe['DBDName'] == FixDBDName]
    sameLBDList = LBDData.groupby(["LBDName"])
    #kd从数据库中取
    kd = float(GetKd(cur,FixDBDName))
    LBDNameList = list(sameLBDList.groups.keys())
    SperLBDData = []
    for LBDName in sameLBDList.groups:
        IndexList = sameLBDList.groups[LBDName].to_list()
        PreData = pd.DataFrame(columns=['LBD','inducer','RPU','I0','kd'])
        for eachIndex in IndexList:
            temp = dataframe.iloc[eachIndex,[2,3,4,5]]
            temp['kd'] = kd
            PreData.loc[len(PreData.index)] = temp
        SperLBDData.append(PreData)
    CalPara(All_Data,DBDNameList,SperAllData,LBDNameList,SperLBDData,conn,cur)
    
def CalPara(All_Data,DBDNameList,SperAllData,LBDNameList,SperLBDData,conn,cur):
    Name = "test"
    model = sameLBD.MyModel ()
    #得到所有DBD的kd值
    #返回数据结构为[Name]:value
    Result = {}
    Result = sameLBD.cal(model,All_Data,DBDNameList,SperAllData)
    #存入计算结果
    for eachkey in Result:
        dbd = DBD.DBD(eachkey["name"],"","","","","","","",eachkey["I0"],eachkey["kd"])
        #TODO: 传Mysql的参数
        dbd.save(conn,cur)
    # print("kd:  {}".format(Result.kd.data))
    # print("k1:  {}".format(Result.k1.data))
    # print("k2:  {}".format(Result.k2.data))
    # print("k3:  {}".format(Result.k3.data))
    index = 0
    for eachLBDName in LBDNameList:
        Result = DiffLBD.cal(eachLBDName,SperLBDData[index])
        # k1 = Result[0]
        # k2 = Result[1]
        # k3 = Result[2]
        # Dict = {"name":Name,"k1":k1,"k2":k2,"k3":k3,"I":1}
        # EXCELAppend("LBDDimer",Dict)
        lbddimer = LBD.LBDDimer(eachLBDName,"","","","","","","",Result[0],Result[1],Result[2],1)
        lbddimer.save(conn,cur)
        index+=1
    return True
if __name__ == '__main__':
    AnalysisExcel()