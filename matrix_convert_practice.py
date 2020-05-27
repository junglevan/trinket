'''(扩展)定义函数,对方阵进行变换'''
import itertools
import inspect, re
import sys


def varname_br(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname_br\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


#def convert(func):
#    def wrapper(*args):
#        n=1
#        for i in func(*args):
#            if not n%len(*args):
#                print(i)
#            else:
#                print(i,end=' ')
#            n+=1
#    return wrapper

#@convert
def anticlock(a):
    print('逆时针变换')
    for k,v in itertools.product(range(len(a)),repeat=2):
        yield a[v][len(a)-1-k]

#@convert
def clockwise(a):
    print('顺时针变换')
    for k,v in itertools.product(range(len(a)),repeat=2):
        yield a[len(a)-1-v][k]

#@convert
def transpose(a):
    print('转置')
    for k,v in itertools.product(range(len(a)),repeat=2):
        yield a[v][k]

#@convert
#def read(a):
#    print('原始表格')
#    return itertools.chain(*a)

# 二维列表
a = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
while True:
    order=[]
    for k,v in itertools.product(range(len(a)),repeat=2): 
        order.append('%s[%s][%s]'%(varname_br(a),k,v)) 
    print('1逆2顺3转')
    s=sys.stdin.readline().strip()
    if s=='1':
        q=anticlock(a) 
    elif s=='2':
        q=clockwise(a) 
    elif s=='3':
        q=transpose(a) 
    else:
        break
    
    exec(','.join(order)+'='+'q')
    for i in a:
        print(i)

#read(a)
#anticlock(a)
#clockwise(a)
#transpose(a)
