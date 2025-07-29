def GetPartByName(Name,cur):
    sql = "select Alias,Level0Sequence,SourceOrganism,Reference,Note,ConfirmedSequence,InsertSequence from PartTable where Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    if(len(result) != 0):
        return Part(Name,result[0][1],result[0][0],result[0][5],result[0][6],result[0][2],result[0][3],result[0][4])
    else:
        return None


class Part():
    def __init__(self,Name,Level0Sequence,Alias = None,ConfirmedSequence = None,InsertSequence = None,SourceOrganism = None,Reference = None,Note = None):
        self.Name = Name
        self.Length = len(Level0Sequence)
        self.Alias = Alias
        self.ConfirmedSequence = ConfirmedSequence
        self.InsertSequence = InsertSequence
        self.Level0Sequence = Level0Sequence
        self.SourceOrganism = SourceOrganism
        self.Reference = Reference
        self.Note = Note

    def GetFileAddress(self,cur):
        sql = "select fileaddress from tb_part_userfileaddress,PartTable where PartTable.Name = '"+self.Name+"' and tb_part_userfileaddress.partid = PartTable.PartID;"
        cur.execute(sql)
        result = cur.fetchall()
        if(len(result) != 0):
            return result[0][0]
        else:
            return None


    




