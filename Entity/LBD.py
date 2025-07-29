from Entity import Part


#导入所有LBD Dimer
def GetLBDDimerList(cur):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,pt.ConfirmedSequence,pt.InsertSequence,lbdt.k1,lbdt.k2,lbdt.k3,lbdt.I from PartTable as pt join LBDDimerTable as lbdt where lbdt.Name = pt.Name;"
    cur.execute(sql)
    result = cur.fetchall()
    LBDDimerList = []
    for each in result:
        lbddimer = LBDDimer(each[1],each[3],each[2],each[7],each[8],each[4],each[5],each[6],each[9],each[10],each[11],each[12])
        LBDDimerList.append(lbddimer)
    return LBDDimerList

def GetLBDDimer(cur,Name):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,pt.ConfirmedSequence,pt.InsertSequence,lbdt.k1,lbdt.k2,lbdt.k3,lbdt.I from PartTable as pt join LBDDimerTable as lbdt where lbdt.Name = pt.Name and pt.Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        lbddimer = LBDDimer(each[1],each[3],each[2],each[7],each[8],each[4],each[5],each[6],each[9],each[10],each[11],each[12])
    return lbddimer


#导入所有LBD NR
def GetLBDNR(cur,Name):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,pt.ConfirmedSequence,pt.InsertSequence,lbdt.k1,lbdt.k2,lbdt.k3,lbdt.kx1, lbdt.kx2 from PartTable as pt join LBDNRTable as lbdt where lbdt.Name = pt.Name and pt.Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    LBDNRList = []
    for each in result:
        lbdnr = LBDNR(each[1],each[3],each[2],each[7],each[8],each[4],each[5],each[6],each[9],each[10],each[11],each[12])
    return lbdnr

def GetLBDDimerMenu(cur):
    sql = "select Name, k1,k2,k3,I from lbddimertable;"
    LBDDimerMenu = {}
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        LBDDimerMenu[each[0]] = [float(each[1]),float(each[2]),float(each[3]),float(each[4])]
    return LBDDimerMenu

def GetLBDNRMenu(cur):
    sql = "select Name,k1,k2,k3,kx1,kx2 from lbdnrtable;"
    LBDNRMenu = {}
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        LBDNRMenu[each[0]] = [float(each[1]),float(each[2]),float(each[3]),float(each[4]),float(each[5])]
    return LBDNRMenu

def GetLBDDimerNameList(cur):
    sql = "select Name from lbddimertable;"
    LBDDimerNameList = []
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        LBDDimerNameList.append(each[0])
    return LBDDimerNameList

def GetLBDNRNameList(cur):
    sql = "select Name from lbdnrtable;"
    LBDNRNameList = []
    cur.execute(sql)
    result = cur.fetchall()
    for each in result:
        LBDNRNameList.append(each[0])
    return LBDNRNameList



class LBD(Part.Part):
    def __init__(self,Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3):
        Part.Part.__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note)
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3

class LBDDimer(LBD):
    def __init__(self,Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3,I):
        LBD.__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3)
        self.I = I
        self.Type = "LBD Dimer"
    def save(self,conn,cur):
        sql = "insert into LBDDimerTable (Name,k1,k2,k3,I) values ('"+self.Name+"',"+str(self.k1)+","+str(self.k2)+","+str(self.k3)+","+str(self.I)+");"
        cur.execute(sql)
        conn.commit()

class LBDNR(LBD):
    def __init__(self,Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3,kx1,kx2):
        LBD.__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3)
        self.kx1 = kx1
        self.kx2 = kx2
        self.Type = "LBD NR"
    def save(self,conn,cur):
        sql = "insert into LBDNRTable (Name,k1,k2,k3,kx1,kx2) values ('"+self.Name+"',"+str(self.k1)+","+str(self.k2)+","+str(self.k3)+","+str(self.kx1)+","+str(self.kx2)+");"
        cur.execute(sql)
        conn.commit()


