def GetBackbone(Name,cur):
    sql = "select Name,Length,Sequence,Ori,Marker,Species,CopyNumber,Notes,Scar from BackboneTable where Name = '"+Name+"';"
    cur.execute(sql)
    result = cur.fetchall()
    if(len(result) != 0):
        return Backbone(result[0][0],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8])
    else:
        return None
class Backbone():
    def __init__(self,Name,Sequence,Ori,Marker,Species=None,CopyNumber=None,Notes=None,Scar=None):
        self.Name = Name
        self.Length = len(Sequence)
        self.Sequence = Sequence
        self.Ori = Ori
        self.Marker = Marker
        self.Species = Species
        self.CopyNumber = CopyNumber
        self.Notes = Notes
        self.Scar = Scar

    def GetFileAddress(self,cur):
        sql = "select fileaddress from tb_backbone_userfileaddress as tbf join BackboneTable as bt where bt.Name = '"+self.Name+"' and tbf.backboneid = bt.ID;"
        cur.execute(sql)
        result = cur.fetchall()
        if(len(result) != 0):
            return result[0][0]
        else:
            return None