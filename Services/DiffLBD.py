import torch
from torch import nn

class Energy(nn.Module):
    def __init__(self):
        super().__init__()
        self.k1 = nn.Parameter(torch.tensor(0.000000016039030626416206))
        self.k2 = nn.Parameter(torch.tensor(0.01934155970811844))
        self.k3 = nn.Parameter(torch.tensor(0.15068600187078118))
    

    def forward(self, L, I, I0, Imax,kd):
        x1 = torch.sqrt((self.k2*I+1)*(self.k2*I+1)+ 8 * L * (self.k2*self.k2*self.k3*I*I + self.k1))
        x2 = torch.sqrt(1 + 8 * L * self.k1)
        F1 = torch.log(L / 2) + torch.log((x1 - (self.k2*I+1)) / (x1 + (self.k2*I+1))) + torch.log(kd)
        F2 = torch.log(L / 2) + torch.log((x2 - (self.k2*I+1)) / (x2 + (self.k2*I+1))) + torch.log(kd)
        n = (Imax + I0) / (Imax - I0)
        y1 = (2*L)/(x1+(self.k2*I+1))
        P1 = (Imax * (1-(1-((y1**2*self.k1*(1e-9)+y1**2*self.k2**2*self.k3*I**2*(1e-9))/(1+(y1**2*self.k1*(1e-9)+(y1**2*self.k2**2*self.k3*I**2*(1e-9))))))**n))+I0
        # Old Version
        # P1 = (Imax * ((L / 2) * ((x1 -  (self.k2*I+1)) / (x1 +  (self.k2*I+1))) * kd / (1 + (L / 2) * ((x1 -  (self.k2*I+1)) / (x1 +  (self.k2*I+1))) *kd)) + I0)
        # (Imax * ((L / 2+1e-9) * ((x1 -  (self.k2*I+1)+1e-9) / (x1 +  (self.k2*I+1))) * (self.kd+1e-9) / (1 + (L / 2+1e-9) * ((x1 -  (self.k2*I+1)+1e-9) / (x1 +  (self.k2*I+1))) *(self.kd+1e-9))) + I0)
        
        
        
        # P2 = (Imax / (1 + torch.exp(-F2))) + I0
        # P1 = (Imax * (1-(1-(1+math.exp(-(beta * F1))))**n))+I0


        #P1 = (Imax * (1-(1-(1/(1+math.exp(-9*(-KB*T*(2*math.log((2*L)/(x1+(self.k2*I+1)))+math.log(self.k1+(self.k2**2)*self.k3*(I**2)))+self.kd)))))**n))+I0
        
        
        
        return (P1) 


def cal(LBDName,SperLBDData):
    # 定义新的损失函数
    loss = nn.MSELoss()
    # 迭代周期
    num_epochs = 50000
    # 模型
    net = Energy()
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    # df = pd.read_csv("/T18/lizengli/MyProject/new_fitter/quantification&crossvalidation4/354.csv") 
    # df = pd.read_csv(FileAddress) 
    L = SperLBDData["LBD"].dropna(axis=0)
    I = SperLBDData['inducer'].dropna(axis=0)
    I0 = SperLBDData['I0'].dropna(axis=0)
    Imax = 35.84931505

    kd = SperLBDData['kd'].dropna(axis=0)
    y = torch.tensor((SperLBDData['RPU']).dropna(axis=0), dtype=torch.float)
    bestk1 = 0
    bestk2 = 0
    bestk3 = 0
    k1 = 0
    k2 = 0
    k3 = 0
    OldL = 1000000000
    for epoch in range(num_epochs):
        l = 0
        for idx in range(len(L)):
            L_element = torch.tensor(L[idx], dtype=torch.float)
            I0_element = torch.tensor(I0[idx], dtype=torch.float)
            Imax = torch.tensor(Imax, dtype=torch.float)
            I_element = torch.tensor(I[idx], dtype=torch.float)
            kd_element = torch.tensor(kd[idx], dtype=torch.float)
            y_element = y[idx:idx+1]
            output = net(L_element, I_element, I0_element, Imax,kd_element)
            if torch.isnan(output): 
                break
            l += loss(output, y_element)
        else:
            optimizer.zero_grad()
            l.backward()
            # 对kb、kc、kd的取值进行限制，避免取到非法值
            net.k1.data = torch.clamp(net.k1.data, min=0, max=1)
            net.k2.data = torch.clamp(net.k2.data, min=0, max=10000)
            net.k3.data = torch.clamp(net.k3.data, min=0, max=10000)
            optimizer.step()
        if(OldL < l):
            bestk1 = net.k1.data
            bestk2 = net.k2.data
            bestk3 = net.k3.data
        if epoch % 100 == 0:
            print('epoch: {}, loss: {}'.format(epoch, l))
            print('k1: {}, k2: {}, k3: {}'.format(net.k1.data, net.k2.data,net.k3.data))
            if(epoch != 0 and abs(l - OldL) > 20000):
                break
            OldL = l
    print(LBDName)
    print(bestk1.item())
    return [bestk1.item(),bestk2.item(),bestk3.item()]


