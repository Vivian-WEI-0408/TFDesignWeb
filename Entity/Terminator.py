from Entity import Part
#导入所有表明强度的终止子
def GetTerminatorList(cur):
    sql = "select pt.partid,pt.Name,pt.Alias,pt.Level0Sequence,pt.SourceOrganism,pt.Reference,pt.Note,prt.RPU,pt.ConfirmedSequence,pt.InsertSequence from PartTable as pt join partrputable as prt on pt.Type=3 and pt.partid = prt.partid and prt.rpu>0;"
    cur.execute(sql)
    result = cur.fetchall()
    TerminatorList = []
    for each in result:
        # Name,Level0Sequence,Strength,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note
        terminator = Terminator(each[1],each[3],each[7],each[2],each[8],each[9],each[4],each[5],each[6])
        TerminatorList.append(terminator)
    return TerminatorList
class Terminator(Part.Part):
    def __init__(self,Name,Level0Sequence,Strength,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note):
        super().__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note)
        self.Strength = Strength
        self.Type = "Terminator"