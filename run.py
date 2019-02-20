import os
import json
from subprocess import *
from aimfunClass import aimfunc
import sys
#这里可以接收外部传入脚本的参数

#p =Popen('python test2.py',stdin=PIPE,stdout=PIPE)
#print(p.stdout.readline().decode())
strategy=sys.argv[2]
data=json.loads(sys.argv[1])

# strategy=1
# data={"orderSum":4500,"faInfo":[{"minAccept":0,"No":3,"P":53,"C":34,"Q":93,"O":57,"L":68},{"minAccept":0,"No":1,"P":46,"C":23,"Q":95,"O":67,"L":45},{"minAccept":0,"No":8,"P":70,"C":30,"Q":96,"O":58,"L":35},{"minAccept":0,"No":2,"P":67,"C":43,"Q":97,"O":92,"L":23},{"minAccept":0,"No":6,"P":58,"C":28,"Q":96,"O":75,"L":51}],"strategy":1}

#print (type(data["faInfo"][0]["C"]))
#print (type(data['faInfo']))
o1=aimfunc.get_instance(data=data,strategy=int(strategy))
# #o2=aimfunc.get_instance()
res=o1.runExe()
res['answer']=res['answer'].tolist()
res['plotPoint']=res['plotPoint'].tolist()
res['answerObjV']=res['answerObjV'].tolist()
print(json.dumps(res))