from pymysql import connect
class DA():
    def __init__(self,host,user,password,database):
        # self.__connection = connect(host = "10.30.76.2",user="WebUser",password="WebUser",database="labdnadata")
        self.__connection = connect(host=host,user=user,password=password,database=database)
        self.__cur = self.__connection.cursor()
    def GetConnection(self):
        return self.__connection
    def GetCursor(self):
        return self.__cur
    
    

    

    

