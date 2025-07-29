import torch
import torch.nn as nn
import pandas as pd
import os
import numpy as np
import torch.nn.init as init
import os
import numpy as np
import pandas as pd
import math

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.k1 = nn.Parameter(torch.Tensor(1))
        self.k2 = nn.Parameter(torch.Tensor(1))
        self.k3 = nn.Parameter(torch.Tensor(1))
        self.kd = nn.Parameter(torch.Tensor(1))
        init.constant_(self.k1, 0.0001)
        init.constant_(self.k2, 1.0)
        init.constant_(self.k3, 0.01)
        init.constant_(self.kd, 10.0)

    def forward(self, L, I, I0, Imax,n=1):
        x1 = torch.sqrt((self.k2*I+1)*(self.k2*I+1)+ 8 * L * (self.k2*self.k2*self.k3*I*I + self.k1)+1e-9)
        y1 = (2*L)/(x1+(self.k2*I+1))
        P1 = (Imax * (1-(1-((y1**2*self.k1*(1e-9)+y1**2*self.k2**2*self.k3*I**2*(1e-9))/(1+(y1**2*self.k1*(1e-9)+(y1**2*self.k2**2*self.k3*I**2*(1e-9))))))**n))+I0
        #old version
        # P1 = (Imax * ((L / 2+1e-9) * ((x1 -  (self.k2*I+1)+1e-9) / (x1 +  (self.k2*I+1))) * (self.kd+1e-9) / (1 + (L / 2+1e-9) * ((x1 -  (self.k2*I+1)+1e-9) / (x1 +  (self.k2*I+1))) *(self.kd+1e-9))) + I0)
        
        return (P1)

# 初始化模型
def cal(model,data_all,DBDNameList,SperAllData):
    # model = MyModel()
    # results = []
    # # 遍历文件夹中的csv文件，将所有的数据合并到一起
    # folder_path = 'c:\\Users\\admin\\Desktop\\data1'
    # data = data_all
    # for filename in os.listdir(folder_path):
    #     if filename.endswith('.csv'):
    #     # 读取csv文件
    #         df = pd.read_csv(os.path.join(folder_path, filename))
    #         data.append(df)

    # 合并所有的数据
    # data_all = pd.concat(data_all)

    # 提取你需要的列
        
    I_all = torch.tensor(list(data_all['inducer'].values), dtype=torch.float64)
    I0_all = torch.tensor(list(data_all['I0'].values), dtype=torch.float64)
    Imax_all = torch.tensor(35.84931505, dtype=torch.float64)
    y_all = torch.tensor(list((data_all['RPU']).values), dtype=torch.float64)


    # 训练模型得到k1, k2, k3
    optimizer_all = torch.optim.Adam([model.k1, model.k2, model.k3], lr=0.0001)
    for _ in range(10000):  # 迭代10000次
        optimizer_all.zero_grad()
        output_all = model(L_all, I_all, I0_all, Imax_all)
        loss_all = nn.MSELoss()(output_all, y_all)
        loss_all.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
        optimizer_all.step()
    
    print(f'Iteration {_}, Loss {loss_all.item()}')
    print(f'k1={model.k1.item()}, k2={model.k2.item()}, k3={model.k3.item()}')

    # 对每个文件单独拟合kd
    KdList = []
    index = 0
    for DBDName in DBDNameList:
        EachPart = {}
        # 读取csv文件
        # df = pd.read_csv(os.path.join(folder_path, filename))
        # 提取你需要的列
        df = SperAllData[index]
        L = torch.tensor(list(df['LBD'].values), dtype=torch.float32)
        I = torch.tensor(list(df['inducer'].values), dtype=torch.float32)
        I0 = torch.tensor(list(df['I0'].values), dtype=torch.float32)
        Imax = torch.tensor(list(df['Imax'].values), dtype=torch.float32)
        y = torch.tensor(list(df['RPU'].values), dtype=torch.float32)

        # 训练模型
        optimizer_kd = torch.optim.Adam([model.kd], lr=0.0001)
        for _ in range(10000):  
            optimizer_kd.zero_grad()
            output = model(L, I, I0, Imax)
            loss = nn.MSELoss()(output, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1)
            optimizer_kd.step()
            
        print(f'File {DBDName}, Iteration {_}, Loss {loss.item()}')
        print(f'For file {DBDName}, kd={model.kd.item()}')
        EachPart["name"] = DBDName
        EachPart["I0"] = 0.035485714
        EachPart["kd"] = model.kd.item()
        KdList.append(EachPart)
        index+=1
    return KdList
            

   