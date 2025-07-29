import flask
from bokeh.client import pull_session
from bokeh.embed import server_session
from TFDesignWeb.Services.opt import HtmlReturn
# from WebAssembly import WebAssembly
from TFDesignWeb.Services.WebAssembly import WebAssembly
from werkzeug.utils import secure_filename
import os
import TFDesignWeb.Services.ParaCal as ParaCal
import pymysql
from Database.DA import DA
app = flask.Flask(__name__,template_folder='templates')
ALLOWED_EXTENSIONS = {'xlsx','xls','csv'}
UPLOAD_File = r'\UPLOAD_FOLDER'
app.config['UPLOAD_FILE'] = UPLOAD_File
#固定用户
@app.route("/createConnect",methods=['POST'])
def Connect():
    host = flask.request.form.get("host")
    user = flask.request.form.get("user")
    password = flask.request.form.get("password")
    database = flask.request.form.get("database")
    try:
        app.config['data_access'] = DA(host=host,user=user,password=password,database=database)
        return flask.jsonify({"Success":"True"})
    except Exception:
        return flask.jsonify({"Error":"Login Error"})
@app.route("/Opt",methods=['POST'])
def Opt():
    alpha = flask.request.form.get('alpha')
    beta = flask.request.form.get('beta')
    Result = HtmlReturn(alpha,beta,app.config['data_access'].GetCursor())
    #使用Result中的LBD和DBD进行自动化设计对于上游TF的选择
    response = {'MaxFoldchange':Result[0],"LBD":Result[1],"DBD":Result[2],"L":Result[3],"RPU":Result[4]}
    return flask.jsonify(response)
@app.route("/TFPlot",methods=['GET'])
def bkapp_page():
    with pull_session(url="http://10.30.76.75:5006/Plot") as session:
        script = server_session(session_id=session.id,url='http://10.30.76.75:5006/Plot')
        return flask.render_template("TF Plot.html",script = script,template="Flask")
@app.route("/Assembly",methods=['POST'])
def AssemblyServe():
    LBD = flask.request.form.get('LBD')
    DBD = flask.request.form.get('DBD')
    L = flask.request.form.get('L')
    assembly = WebAssembly(LBD,DBD,L,app.config['data_access'])
    assembly.AssemblyFuntion()
    return flask.jsonify({"success":"True"})
@app.route("/Download",methods=['GET'])
def DownloadFile():
    return flask.send_file(r'/home/database/TFDesignWeb/File/output/Level3.gb')
@app.route("/UploadData",methods=['POST'])
def UploadDataMethod():
    if(flask.request.method == 'POST'):
        print(flask.request.files)
        upload_file = flask.request.files.getlist('file')
        if(len(upload_file) !=0):
            index = 1
            for EachFile in upload_file:
                if(EachFile.filename !=''):
                    filename = secure_filename(EachFile.filename)
                    objectname = "Data"+str(index)+".csv"
                    EachFile.save(os.path.join(app.config['UPLOAD_FILE'],objectname))
                    index += 1
    return flask.jsonify({"success":"True"})
@app.route("/DownloadTempalte",methods=['GET'])
def DownloadTemplate():
    return flask.send_file(r'/home/database/TFDesignWeb/File/UPLOAD_FOLDER/Template.csv')
@app.route("/Fitting")
def FittingCal():
    ParaCal.AnalysisExcel(app.config['data_access'].GetConnection(),app.config['data_access'].GetCursor())
    return flask.jsonify({"success":"True"})


app.run(host = "10.30.76.75",port=8101,debug=True)