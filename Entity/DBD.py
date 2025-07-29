from Entity import Part
#导入所有DBD
def GetDBDList(cur):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,pt.ConfirmedSequence,pt.InsertSequence,dbdt.I0,dbdt.kd from PartTable as pt join DBDTable as dbdt where dbdt.Name = pt.Name;"
    cur.execute(sql)
    result = cur.fetchall()
    DBDList = []
    for each in result:
        dbd = DBD(each[1],each[3],each[2],each[7],each[8],each[4],each[5],each[6],each[9])
        DBDList.append(dbd)
    return DBDList

def GetDBD(cur,Name):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,pt.ConfirmedSequence,pt.InsertSequence,dbdt.I0,dbdt.kd from PartTable as pt join DBDTable as dbdt where dbdt.Name = pt.Name and pt.Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        dbd = DBD(each[1],each[3],each[2],each[7],each[8],each[4],each[5],each[6],each[9])
    return dbd

def GetDBDMenu(cur):
    sql = "select Name,I0,kd from dbdtable;"
    DBDMenu = {}
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        DBDMenu[each[0]] = [float(each[1]),float(each[2])]
    return DBDMenu

def GetDBDNameList(cur):
    sql = "select Name from dbdtable;"
    DBDNameList = []
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        DBDNameList.append(each[0])
    return DBDNameList

def GetDBDKdList(cur):
    sql = "select kd from dbdtable;"
    DBDList = []
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        DBDList.append(each[0])
    return DBDList

def GetDBDKd(cur,Name):
    sql = "select kd from DBDTable where Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    return result[0][0]


class DBD(Part.Part):
    def __init__(self,Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,I0,kd):
        Part.Part.__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note)
        self.Type = "DBD"
        self.I0 = I0
        self.kd = kd
    def save(self,conn,cur):
        sql = "insert into DBDTable (Name,I0,kd) values ('"+self.Name+"',"+str(self.I0)+","+str(self.kd)+");"
        cur.execute(sql)
        conn.commit()