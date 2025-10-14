from Entity import Part
import requests

#导入所有LBD Dimer
def GetLBDDimerList(api_url,session):
    response = session.get(f'{api_url}GetLBDDimer')
    LBDDimerList = []
    if(response.status_code == 200):
        result = response.json()
        for each in result:
            LBDDimerList.append(LBDDimer(each['name'],each['level0sequence'],each['alias'],
                                         each['confirmedsequence'],each['insertsequence'],each['sourceorganism'],
                                         each['reference'],each['note'],each['k1'],each['k2'],each['k3'],each['i']))
    return LBDDimerList


def GetLBDDimer(api_url,Name,session):
    response = session.get(f'{api_url}GetLBDDimerAllByName?name={Name}')
    if(response.status_code == 200):
        result = response.json()
        lbddimer = LBDDimer(result['name'],result['level0sequence'],result['alias'],
                                         result['confirmedsequence'],result['insertsequence'],result['sourceorganism'],
                                         result['reference'],result['note'],result['k1'],result['k2'],result['k3'],result['i'])
        return lbddimer
    else:
        return None



#导入所有LBD NR
def GetLBDNR(api_url,Name,session):
    response = session.get(f'{api_url}GetLBDAllByName?name={Name}')
    if(response.status_code == 200):
        result = response.json()
        lbd = LBDNR(result['name'],result['level0sequence'],result['alias'],result['confirmedsequence'],
                    result['insertsequence'],result['sourceorganism'],result['reference'],
                    result['note'],result['k1'],result['k2'],result['k3'],result['kx1'],result['kx2'])
        return lbd
    else:
        return None
def GetLBDDimerMenu(api_url,session):
    response = session.get(f'{api_url}GetLBDDimerMenu')
    LBDDimerMenu = {}
    if(response.status_code == 200):
        result = response.json()
        for each in result:
            LBDDimerMenu[each['name']] = [float(each['k1']),float(each['k2']),float(each['k3']),float(each['i'])]
        return LBDDimerMenu
    else:
        return LBDDimerMenu


def GetLBDNRMenu(api_url,session):
    response = session.get(f'{api_url}GetLBDNRMenu')
    LBDNRMenu = {}
    if(response.status_code == 200):
        result = response.json()
        for each in result:
            LBDNRMenu[each['name']] = [float(each['k1']),float(each['k2']),float(each['k3']),float(each['kx1']),float(each['kx2'])]
        return LBDNRMenu
    else:
        return LBDNRMenu


def GetLBDDimerNameList(api_url,session):
    try:
        response = session.get(f'{api_url}GetLBDDimerNameList')
        if(response.status_code == 200):
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(e)

def GetLBDNRNameList(api_url,session):
    response = session.get(f'{api_url}GetLBDNRNameList')
    if(response.status_code == 200):
        return response.json()
    else:
        return None





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
    def save(self,api_url,session):
        newLBDDimer = {'data':{'Name':self.Name,'k1':self.k1,'k2':self.k2,'k3':self.k3,'I':self.I}}
        response = session.post(f'{api_url}AddLBDDimer',data=newLBDDimer)

class LBDNR(LBD):
    def __init__(self,Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3,kx1,kx2):
        LBD.__init__(Name,Level0Sequence,Alias,ConfirmedSequence,InsertSequence,SourceOrganism,Reference,Note,k1,k2,k3)
        self.kx1 = kx1
        self.kx2 = kx2
        self.Type = "LBD NR"
    def save(self,api_url,session):
        newLBDNR = {'data':{'name':self.Name,'k1':self.k1,'k2':self.k2,'k3':self.k3,'kx1':self.kx1,'kx2':self.kx2}}
        response = session.post(f'{api_url}AddLbdnr',data=newLBDNR)

