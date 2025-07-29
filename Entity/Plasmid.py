def GetPlasmid(Name,cur):
    sql = "select Oricloing,OriHost,MarkerCloning,MarkerHost,Level,SequenceConfirm,Plate,State,Note from PlasmidNeed where Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    if(len(result) != 0):
        sql2 = "select PlasmidID from PlasmidNeed where Name = '"+Name+"';"
        cur.execute(sql2)
        ID = cur.fetchall()[0][0]
        plasmidIDList = GetParentID(ID,cur)
        return Plasmid(Name,result[0][5],result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][6],result[0][7],plasmidIDList,result[0][8])
    else:
        return None
    
def GetParentID(plasmidID,c):
    sql = "select ParentPlasmidID from parentplasmidtable where SonPlasmidID = "+str(plasmidID)+";"
    c.execute(sql)
    plasmidIDList = []
    result = c.fetchall()
    for each in result:
        plasmidIDList.append(each[0])
    return plasmidIDList

class Plasmid():
    def __init__(self,Name,Sequence,OriClone,OriHost,MarkerClone,MarkerHost,Level,Plate = None,State = None,ParentID = None,Note = None):
        self.Name = Name
        self.Length = len(Sequence)
        self.Sequence = Sequence
        self.OriClone = OriClone
        self.OriHost = OriHost
        self.MarkerClone = MarkerClone
        self.MarkerHost = MarkerHost
        self.Level = Level
        self.Plate = Plate
        self.State = State
        self.ParentID = ParentID
        self.Note = Note

    def GetFileAddress(self,cur):
        sql = "select fileaddress from tb_plasmid_userfileaddress as tpf join PlasmidNeed as pn where pn.Name = '"+self.Name+"' and tpf.plasmidid = pn.PlasmidID;"
        cur.execute(sql)
        result = cur.fetchall()
        if(len(result) != 0):
            return result[0][0]
        else:
            return None