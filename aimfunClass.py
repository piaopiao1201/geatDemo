import numpy as np
from sklearn import preprocessing
import geatpy as ga
import math

class aimfunc:
    instance=None
    strategy=2
    orderSum=None
    faInfo=None
    def __init__(self, data,strategy):
        self.orderSum = data["orderSum"]
        self.faInfo = data["faInfo"]
        self.strategy = strategy
        #print (data)
        # print (self.orderSum)
        # print (self.faInfo)
    @staticmethod
    def get_instance(data=None,strategy=None):
        if aimfunc.instance is None:
            aimfunc.instance = aimfunc(data,strategy)
        return aimfunc.instance

    def aimfuc(self, x, LegV):
        xList=[]
        xSum=0

        for i in range(len(self.faInfo)-1):
            xList.append(x[:,i])
            xSum+=x[:,i]


        xList.append(self.orderSum-xSum)
        #x[:,i+1]=self.orderSum-xSum
        #print (x)
        # print(self.orderSum-xSum)
        fun1=0
        fun2=0
        for i in range(len(xList)):
            fun1+=self.faInfo[i]["C"]*xList[i]
            fun2+=((xList[i]/(30*self.faInfo[i]["P"])+self.faInfo[i]["L"]/100)-(xList[(i+1)%len(xList)]/(30*self.faInfo[(i+1)%len(xList)]["P"])+self.faInfo[(i+1)%len(xList)]["L"]/100))**2
        # print(self.faInfo[i]["minAccept"])
        # print(self.faInfo[i]["P"]*30*(1-self.faInfo[i]["L"]/100))
        # 约束条件
        idx1 = np.where(self.orderSum-xSum < self.faInfo[i]["minAccept"])[0]
        idx2 = np.where(self.orderSum-xSum > math.floor(self.faInfo[i]["P"]*30*(1-self.faInfo[i]["L"]/100)))[0]
        exIdx = np.unique(np.hstack([idx1, idx2])) # 得到非可行解的下标
        # print(exIdx)
        # print(self.orderSum-xSum)
        # print(math.floor(self.faInfo[i]["P"]*30*(1-self.faInfo[i]["L"]/100)))
        # #print(self.orderSum-xSum)
        LegV[exIdx] = 0 # 标记非可行解对应的可行性列向量中元素的值为0
        # x1 = x[:, 0];
        # x2 = x[:, 1];
        # x3 = x[:, 2];
        # x6 = x[:, 3];
        # x8 = 4500 - x1 - x2 - x3 - x6
        # fun1 = 23 * x1 + 43 * x2 + 34 * x3 + 28 * x6 + 30 * x8 + 288
        # fun2 = ((x1 / 1380 + 0.45) - (x2 / 2010 + 0.23)) ** 2 + ((x2 / 2010 + 0.23) - (x3 / 1590 + 0.68)) ** 2 + (
        #         (x3 / 1590 + 0.68) - (x6 / 1740 + 0.51)) ** 2 + ((x6 / 1740 + 0.51) - (x8 / 2100 + 0.35)) ** 2 + (
        #                (x8 / 2100 + 0.35) - (x1 / 1380 + 0.45)) ** 2
        return [np.vstack([fun1, fun2]).T, LegV]  # 对矩阵进行转置使得目标函数矩阵符合Geatpy数据结构
    def getData(self):
        return self.data

    def runExe(self):
        AIM_M = __import__('aimfunClass')  # 获取函数接口所在文件的地址
        # 边界设置
        lowerBoundtemp1=np.array([])
        upperBoundtemp2=np.array([])
        for i in range(len(self.faInfo)-1):
            lowerBoundtemp1=np.append(lowerBoundtemp1,np.array([self.faInfo[i]["minAccept"]]))
            upperBoundtemp2=np.append(upperBoundtemp2,np.array([math.floor(self.faInfo[i]["P"]*30*(1-self.faInfo[i]["L"]/100))]))
        rangesLowerBound=np.array([lowerBoundtemp1])
        rangesUpperBound=np.array([upperBoundtemp2])
        ranges=np.concatenate([rangesLowerBound,rangesUpperBound])
        #print (ranges)
        #borders
        borders=np.array([np.ones(len(self.faInfo)-1),np.ones(len(self.faInfo)-1)])
        #ranges = np.array([[600, 1300, 460, 750], [759, 1547, 508, 852]])  # 生成自变量的范围矩阵
        #borders = np.array([[1, 1, 1, 1], [1, 1, 1, 1]])  # 生成自变量的边界矩阵（1表示变量的区间是闭区间）
        precisions = [1, 1]  # 根据crtfld的函数特性，这里需要设置精度为任意正值，否则在生成区域描述器时会默认为整数编码，并对变量范围作出一定调整
        FieldDR = ga.crtfld(ranges, borders, precisions)  # 生成区域描述器
        # 调用编程模板
        [ObjV, NDSet, NDSetObjV, times] = ga.moea_nsga2_templet(AIM_M, 'getAimFunc', None, None, FieldDR, 'R', maxormin=1,
                                                                MAXGEN=200, MAXSIZE=300, NIND=30, SUBPOP=1, GGAP=1,
                                                                selectStyle='tour', recombinStyle='xovdp', recopt=0.9,
                                                                pm=0.1, distribute=True, drawing=0)

        # print('--------ObjV为------------')
        # print(ObjV)
        # print('--------NDSet为------------')
        # print(NDSet.shape)
        # print('--------NDSetObjV为------------')
        # print(NDSetObjV)
        # print('--------times为------------')
        # print(times)

        add = self.orderSum - np.sum(NDSet, axis=1)
        # print(sum(add>=1265))
        # 所有分配方案的集合
        res = np.c_[NDSet, add]

        #结果序号集合
        index=None

        #结果集合
        resList=None
        #NDSetObjV 为目标函数集合

        if self.strategy==1:
            guiyiObj = preprocessing.StandardScaler().fit(NDSetObjV).transform(NDSetObjV)
            # 找到原点的坐标
            origin = np.min(guiyiObj, axis=0)

            #print("--原点坐标--")
            #print(origin)
            # 欧氏距离的集合
            distance = np.sum(np.square(guiyiObj - origin), axis=1)
            # 选出5个最优解
            index = np.argsort(distance)[0:5]



            #print(NDSetObjV[index])
            #print(res[index])


        #取目标函数1最小即成本最小
        elif self.strategy==2:
            index=np.argsort(NDSetObjV[:,0])[0:5]
        # 取目标函数2最小即差异最小
        elif self.strategy == 3:
            index = np.argsort(NDSetObjV[:, 1])[0:5]
        resList = {
            'answer': np.around(res[index]),
            'answerObjV': NDSetObjV[index],
            'plotPoint': NDSetObjV
        }
        return resList

def getAimFunc(x, LegV):
    return aimfunc.get_instance().aimfuc(x,LegV)




