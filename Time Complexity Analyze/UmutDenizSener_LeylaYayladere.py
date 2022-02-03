import time
import numpy as numpy

def listCreator(operation, case, size):
    if (case == 'best' or case == 'worst'):

        if (case == 'best' and operation == 3) or (case == 'worst' and operation ==4):
            list = [1] * size
        elif (case == 'worst' and operation ==3) or (case == 'best' and operation ==4):
            list = [0] * size
        else:
            list = [1] * size
        return list

    elif(case == 'average'):
        #list = random.choices(population= [0, 1], weights= [1/3, 2/3], k= size)
        list = numpy.ones(size)
        list[:size//3] = 0
        numpy.random.shuffle(list)

        return list

def func(operation, case, size):
    list = listCreator(operation, case, size)
    start = time.time()
    y=0
    for i in range(0, len(list)):
        if(list[i] == 0):
            for j in range(i, len(list)):
                k = len(list)
                while(k>=1):
                    k = k//2
                    y = y+1
        else:
            for m in range(i, len(list)):
                for t in range(1, len(list)+1):
                    x = len(list)
                    while x>0:
                        x = x-t
                        y = y+1
    end = time.time()

    print("Case:",case,"Size:", size,"Elapsted Time:", end - start)
    return y
    
data = [1,10,50,100,200,300,400,500,600,700]
for n in data:
    func(4, 'worst', n)
    func(4, 'average', n)
    func(4, 'best', n)

