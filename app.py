import flask
from bokeh.client import pull_session
from bokeh.embed import server_session
from Services.opt import HtmlReturn
# from WebAssembly import WebAssembly
from Services.WebAssembly import WebAssembly
from werkzeug.utils import secure_filename
import os
import Services.ParaCal as ParaCal
from Entity import LBD, DBD
import sys
sys.path.append("/home/database/TFDesignWeb")
app = flask.Flask(__name__,template_folder='templates')
ALLOWED_EXTENSIONS = {'xlsx','xls','csv'}
UPLOAD_File = r'\UPLOAD_FOLDER'
app.config['UPLOAD_FILE'] = UPLOAD_File
import requests
app.config['api_url'] =  'http://10.30.76.2:8000/WebDatabase/'
UploadFileList = []
global session
# session = requests.Session()
#固定用户
# @app.route("/createConnect",methods=['POST'])
# def Connect():
#     host = flask.request.form.get("host")
#     user = flask.request.form.get("user")
#     password = flask.request.form.get("password")
#     database = flask.request.form.get("database")
#     try:
#         app.config['data_access'] = DA(host=host,user=user,password=password,database=database)
#         return flask.jsonify({"Success":"True"})
#     except Exception:
#         return flask.jsonify({"Error":"Login Error"})
# @app.route("/login",methods = ['GET'])
# def login():
#     # print("111111")
    # login_url = f'{app.config["api_url"]}login'
    # test_url = f'{app.config["api_url"]}Part'
    # credentials = {'uname':'root','password':'chenlab'}
    # session = requests.Session()
    # response = session.get(login_url)
    # csrftoken = session.cookies.get('csrftoken')
    # headers = {'X-CSRFToken':csrftoken,'Content-Type':'application/json'}
    # response = session.post(login_url,json=credentials,headers=headers)
    # if(response.status_code == 200):
    #     print(111)
    #     return flask.redirect('/test')
    # else:
    #     print("000")
    # session = requests.get(f'{app.config["api_url"]}login')
    # print(f'{app.config["api_url"]}login')
    # print(session.text)
# @app.route("/test",methods=['GET'])
# def test_connection():
#     try:
#         print(f'{app.config["api_url"]}GetLBDDimerNameList')
#         response = requests.get(f'{app.config["api_url"]}GetLBDDimerNameList')
#         return f"{response.text}"
#     except requests.exceptions.ConnectionError:
#         return False
def getsession():
    return session
@app.route("/Opt",methods=['POST'])
def Opt():
    alpha = flask.request.form.get('alpha')
    beta = flask.request.form.get('beta')
    Result = HtmlReturn(alpha,beta,app.config['api_url'],session)
    #使用Result中的LBD和DBD进行自动化设计对于上游TF的选择
    response = {'MaxFoldchange':Result[0],"LBD":Result[1],"DBD":Result[2],"L":Result[3],"RPU":Result[4]}
    return flask.jsonify(response)
@app.route("/TFPlot",methods=['GET'])
def bkapp_page():
    # url 为Bokeh服务的启动地址（根据实际情况更改）
    with pull_session(url="http://10.30.76.75:5006/Plot") as session_bokeh:
        # session = requests.Session()
        # login_response = session.get(f'{app.config["api_url"]}login')
        # response = requests.post(f'{app.config["api_url"]}login')
        # print(f'{app.config["api_url"]}login')
        session = requests.Session()
        response = session.get(f'{app.config["api_url"]}login')
        csrf_token = session.cookies.get('csrftoken')
        loginfo = {'uname':'root','password':'chenlab','csrfmiddlewaretoken': csrf_token}
        headers = {'Referer':f'{app.config["api_url"]}login','X-CSRFToken':csrf_token}
        response = session.post(f'{app.config["api_url"]}login',data=loginfo,headers=headers)


        script = server_session(session_id=session_bokeh.id,url='http://10.30.76.75:5006/Plot')
        LBDList = LBD.GetLBDDimerNameList(app.config['api_url'],session)
        DBDList = DBD.GetDBDNameList(app.config['api_url'],session)
        return flask.render_template("TF Plot.html",LBDList = LBDList, DBDList = DBDList, script = script,template="Flask")
@app.route("/Assembly",methods=['POST'])
def AssemblyServe():
    LBD = flask.request.form.get('LBD')
    DBD = flask.request.form.get('DBD')
    L = flask.request.form.get('L')
    assembly = WebAssembly(LBD,DBD,L,app.config['api_url'],session)
    assembly.AssemblyFuntion()
    return flask.jsonify({"success":True})
@app.route("/Download",methods=['GET'])
def DownloadFile():
    # 发送文件地址根据实际情况更改
    return flask.send_file(r'/home/database/TFDesignWeb/File/output/Level3.gb')
@app.route("/UploadData",methods=['POST'])
def UploadDataMethod():
    if(flask.request.method == 'POST'):
        upload_file = flask.request.files.getlist('file')
        if(len(upload_file) !=0):
            index = 1
            for EachFile in upload_file:
                if(EachFile.filename !=''):
                    filename = secure_filename(EachFile.filename)
                    objectname = "Data"+str(index)+".csv"
                    EachFile.save(os.path.join(app.config['UPLOAD_FILE'],objectname))
                    UploadFileList.append(os.path.join(app.config['UPLOAD_FILE'],objectname))
                    index += 1
    return flask.jsonify({"success":True})
@app.route("/DownloadTempalte",methods=['GET'])
def DownloadTemplate():
    # 发送文件地址根据实际情况更改
    return flask.send_file(r'/home/database/TFDesignWeb/File/UPLOAD_FOLDER/Template.csv')
@app.route("/Fitting")
def FittingCal():
    if(flask.request.method == "POST"):
        algorithm = flask.request.form.get("Algorithm")
        I0 = flask.request.form.get("I0")
        if(I0 == None or I0 == "" or I0 == 0):
            I0 = 0.015930056
        else:
            I0 = float(I0)
        Imax = 35.84931505
        result = ParaCal.AnalysisExcel(UploadFileList,algorithm,I0,Imax,app.config['api_url'],session)
        DBDResult = result[0][0]
        LBDResult = result[1][0]
        return flask.jsonify({"success":True,"DBD":DBDResult['name'],"LBD":LBDResult['name']})


app.run(host = "10.30.76.75",port=8101,debug=True)