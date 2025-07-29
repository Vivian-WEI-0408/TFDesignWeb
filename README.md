<h1>Transription Factor Design Tool</h1>
<p>转录因子自动化设计工具，基于Flask的Web服务，支持数据可视化，参数自动化拟合，转录因子最优设计，转录因子图谱拼装</p>
<h3>手动部署</h3>
<p>1.要求python3.10和TF Bokeh服务</p>
<p>2.依赖 pip install -r requirements.txt</p>
<p>3.启动</p>

    $ cd WebPlot/GUI

    $ bokeh serve --show Plot.py --allow-websocket-origin="*"
    
    $cd ..

    $ python main.py

<h3>Data Access</h3>
<p>使用pymysql连接服务器数据库</p>
<h3>Entity</h3>
<P>包括TF Design中要使用到的元件、backbone等</p>

|      Type      |    Description    |
|----------------|-------------------|
|Part            |元件父类            |
|Backbone        |载体类              |
|Plasmid         |质粒类              |
|LBD             |(Part)子类          |
|DBD             |(Part)子类          |
|Promoter        |(Part)启动子        |
|Terminator      |(Part)终止子        |

<h4>Part Class</h4>

|      Attribute      |    Description    |
|---------------------|-------------------|
|Name                 |元件名称            |
|Length               |元件长度            |
|Alias                |元件别名            |
|ConfirmedSequence    |元件序列(验证序列)   |
|Level0Sequence       |Level0序列          |
|SourceOrganism       |来源物种            |
|Reference            |参考文献            |
|Note                 |备注信息            |

<h4>Backbone Class</h4>

|      Attribute      |    Description    |
|---------------------|-------------------|
|Name                 |载体名称            |
|Length               |载体长度            |
|Sequence             |载体序列            |
|Ori                  |复制起点标识         |
|Marker               |抗性标识            |
|Species              |来源物种            |
|CopyNumber           |复制数              |
|Notes                |备注信息            |
|Scar                 |疤痕编号            |

<h4>Plasmid Class</h4>

|      Attribute      |    Description    |
|---------------------|-------------------|
|Name                 |质粒名称            |
|Length               |质粒长度            |
|Sequence             |质粒序列            |
|OriClone             |复制起点(Clone)     |
|MarkerClone          |抗性标识(Clone)     |
|OriHost              |复制起点(Host)      |
|MarkerHost           |抗性标识(Host)      |
|Level                |质粒等级            |
|Plate                |质粒存储位置        |
|State                |质粒存储状态        |
|ParentID             |双亲质粒ID          |
|Species              |来源物种            |
|Note                 |备注信息            |

