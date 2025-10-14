#使用sameLBD，diffLBD对参数进行拟合
#然后存储在TFDatabase.xlsx   

#先跑Diff，再跑Same  
#将Diff的K1，k2，k3作为静态变量
#static
import sameLBD
import Services.DiffLBD as DiffLBD
import pandas as pd
from Entity import DBD,LBD
from os import listdir
import DiffLBDCurveFit
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
def GetKd(api_url,DBDName,session):
    return DBD.GetDBDKd(api_url,DBDName,session)


# UploadFileList,algorithm,I0,Imax,app.config['api_url']
def AnalysisExcel(UploadFileList, algorithm, I0, Imax, api_url,session):
    # # FileAddress = './UPLOAD_FOLDER/Data.csv'
    # folderAddress = r'WebPlot/UPLOAD_FOLDER/Data'
    # files = listdir(folderAddress)
    print(UploadFileList)
    if(len(UploadFileList) == 0):
        return
    dataframe = pd.DataFrame()
    for file in UploadFileList:
        # dataframe.append(pd.read_csv)
        dataframe = pd.concat([dataframe,pd.read_csv(file)])
        # dataframepd.read_csv(FileAddress)
    All_Data = pd.DataFrame(columns=['LBD','inducer','RPU'])
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
        PreData = pd.DataFrame(columns=['LBD','inducer','RPU'])
        for eachIndex in IndexList:
            temp = pd.Series()
            temp = dataframe.iloc[eachIndex,[2,3,4]]
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
    # kd = float(GetKd(cur,FixDBDName))
    LBDNameList = list(sameLBDList.groups.keys())
    # SperLBDData = []
    # for LBDName in sameLBDList.groups:
    #     IndexList = sameLBDList.groups[LBDName].to_list()
    #     PreData = pd.DataFrame(columns=['LBD','inducer','RPU','I0','kd'])
    #     for eachIndex in IndexList:
    #         temp = dataframe.iloc[eachIndex,[2,3,4,5]]
    #         # temp = float(GetKd())
    #         PreData.loc[len(PreData.index)] = temp
    #     SperLBDData.append(PreData)
    # CalPara(All_Data,DBDNameList,SperAllData,LBDNameList,SperLBDData,conn,cur)
    result = CalPara(algorithm,I0,Imax,All_Data,DBDNameList,SperAllData,LBDNameList,sameLBDList,dataframe,FixDBDName,api_url,session)
    return result

def CalPara(algorithm,I0,Imax,All_Data,DBDNameList,SperAllData,LBDNameList,sameLBDList,dataframe,FixDBDName,api_url,session):
    Name = "test"
    model = sameLBD.MyModel()
    resultListLBD = []
    resultListDBD = []
    resultList = [resultListDBD,resultListLBD]
    #得到所有DBD的kd值
    #返回数据结构为[Name]:value
    Result = {}
    Result = sameLBD.cal(model,All_Data,DBDNameList,SperAllData,I0,Imax)
    #存入计算结果
    for eachkey in Result:
        dbd = DBD.DBD(eachkey["name"],"","","","","","","",eachkey["I0"],eachkey["kd"])
        #TODO: 传Mysql的参数
        dbd.save(api_url,session)
        eachresult = {}
        eachresult["name"] = eachkey["name"]
        eachresult["I0"] = eachkey["I0"]
        eachresult["kd"] = eachkey["kd"]
        resultListDBD.append(eachresult)
    # print("kd:  {}".format(Result.kd.data))
    # print("k1:  {}".format(Result.k1.data))
    # print("k2:  {}".format(Result.k2.data))
    # print("k3:  {}".format(Result.k3.data))


    SperLBDData = []
    for LBDName in sameLBDList.groups:
        IndexList = sameLBDList.groups[LBDName].to_list()
        PreData = pd.DataFrame(columns=['LBD','inducer','RPU','kd'])
        for eachIndex in IndexList:
            temp = pd.Series()
            temp = dataframe.iloc[eachIndex,[2,3,4]]
            tempKd = float(GetKd(api_url,FixDBDName,session))
            temp['kd'] = tempKd
            PreData.loc[len(PreData.index)] = temp
            
            
        SperLBDData.append(PreData)


    if(algorithm == "CNN"):
        index = 0
        for eachLBDName in LBDNameList:
            Result = DiffLBD.cal(eachLBDName,SperLBDData[index],I0,Imax)
            index += 1
            lbddimer = LBD.LBDDimer(eachLBDName,"","","","","","","",Result[0],Result[1],Result[2],1)
            lbddimer.save(api_url,session)
            index+=1
            eachresult = {}
            eachresult["name"] = eachLBDName
            eachresult["k1"] = Result[0]
            eachresult["k2"] = Result[1]
            eachresult["k3"] = Result[2]
            eachresult["I"] = 1
            resultListLBD.append(eachresult)
            # k1 = Result[0]
            # k2 = Result[1]
            # k3 = Result[2]
            # Dict = {"name":Name,"k1":k1,"k2":k2,"k3":k3,"I":1}
            # EXCELAppend("LBDDimer",Dict)

    else:
        index = 0
        for eachLBDName in LBDNameList:
            Result = DiffLBDCurveFit.cal(eachLBDName,SperLBDData[index],I0,Imax)
            index += 1
            lbddimer = LBD.LBDDimer(eachLBDName,"","","","","","","",Result[0],Result[1],Result[2],1)
            lbddimer.save(api_url,session)
            eachresult = {}
            eachresult["name"] = eachLBDName
            eachresult["k1"] = Result[0]
            eachresult["k2"] = Result[1]
            eachresult["k3"] = Result[2]
            eachresult["I"] = 1
            resultListLBD.append(eachresult)
    return resultList
if __name__ == '__main__':
    AnalysisExcel()