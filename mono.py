import argparse
import numpy as np
import time

class mono_routing():
    def __init__(self, args):
        pass
    def parser(self): #You can modify it by yourself.
        with open("%s" % args.input, 'r', newline='') as file_in:
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("BoundaryIndex"):
                    value_list = lines.split(' ')
                    self.Bx1 = int(value_list[1])
                    self.By1 = int(value_list[2])
                    self.Bx2 = int(value_list[3])
                    self.By2 = int(value_list[4])
                if lines.startswith("DefaultCost"):
                    value_list = lines.split(' ')
                    self.default_cost = int(value_list[-1])
                if lines.startswith("NumNonDefaultCost"):
                    value_list = lines.split(' ')
                    self.size = int(value_list[-1])
                    break
            
            source_list = list(f[-2].split(' '))
            target_list = list(f[-1].split(' '))
            self.sx = source_list[1]
            self.sy = source_list[2]
            self.tx = target_list[1]
            self.ty = target_list[2]
            """Saving cost"""
            self.NDcost = {}
            for x in range(self.Bx2+1):
                for y in range(self.By2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x,y+1)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x,y+1)] = self.default_cost
            
            for y in range(self.By2+1):
                for x in range(self.Bx2+1):
                    #self.NDcost['%d%d%d%d' %(x,y,x+1,y)] = self.default_cost --> this is wrong
                    self.NDcost[(x,y,x+1,y)] = self.default_cost
            
            num_cost = f[3:3+int(self.size)]
            for NDcost in num_cost:
                NDcost_list = NDcost.split(' ')
                self.NDcost[(int(NDcost_list[0]), int(NDcost_list[1]), int(NDcost_list[2]), int(NDcost_list[3]))] += int(NDcost_list[4])

        #print(self.NDcost)
        self.costs_up = [[] for i in range(self.By2+1)]
        self.costs_right = [[] for i in range(self.Bx2+1)]
        num = 1
        total_num = 0
        for i in self.NDcost:
            total_num+=1
            if total_num<= (self.By2+1)*(self.By2+1):# 5*5 #有多餘的之後要去掉
                self.costs_up[num-1].append(self.NDcost[i])
                num+=1
            if total_num > (self.By2+1)*(self.By2+1):
                self.costs_right[num-1].append(self.NDcost[i])
                num+=1
            if num%(self.By2+2) == 0:
                num = 1

        self.costs_up = self.costs_up[:-1]
        self.costs_right = self.costs_right[:-1]
        #print(self.costs_up)
        #print("len(self.costs_up):",len(self.costs_up))
        #print(self.costs_right)
        #print("len(self.costs_right):",len(self.costs_right))
        
        
        """Print parameters"""
        print('BoundaryIndex:',self.Bx1,self.By1,self.Bx2,self.By2)
        print('DefaultCost:',self.default_cost)
        print('NumNonDefaultCost:',self.size)
        #for i in range(len(num_cost)):
        #    print(num_cost[i])
        print('Source:',self.sx, self.sy)
        print('Target:',self.tx, self.ty)


        
    def routing(self):
        self.routing_path = np.zeros((self.Bx2+self.By2+1,2),dtype=int)
        self.grid_cost = np.zeros((self.By2+1,self.Bx2+1),dtype=int)

        # ---TODO:
        # Write down your routing algorithm by using dynamic programming.
        # ---

        cost = [[ 0 for j in range(len(self.costs_up)+1) ] for i in range(len(self.costs_up)+1)]
        #print("len(cost):",len(cost))
        n = len(cost)-1
        cost[len(cost)-1][0] = 0 #左下角是0

        self.path = [[ [] for j in range(len(self.costs_up)+1) ] for i in range(len(self.costs_up)+1)]
        self.path[len(cost)-1][0].append((0,0))
        #print(path)


        #print(len(self.costs_up))
        # 往上走
        for i in range(len(cost)-1, 0, -1): # 4~0
            cost[i-1][0]=(cost[i][0] + self.costs_up[len(self.costs_up)-i][0]) # 4~0
            self.path[i-1][0].append((0,n-i))
        #print(path)

        # 往右走
        for i in range(1, len(cost)): # 1~4
            cost[-1][i]=(cost[-1][i-1] + self.costs_right[i-1][0])
            if i != 0:
                self.path[-1][i].append((i-1,0))
        #print(path)

        #print(cost)

        # others取min
        for i in range(len(cost)-2, -1, -1): # 3~0 cost的座標
            for j in range(1, len(cost)): #1~4 cost的座標
                cost[i][j] = min(self.costs_up[(self.By2-1)-i][j]+cost[i+1][j], self.costs_right[j-1][n-i]+cost[i][j-1])        

                if self.costs_up[(self.By2-1)-i][j]+cost[i+1][j] != self.costs_right[j-1][n-i]+cost[i][j-1]:
                    if cost[i][j] == self.costs_up[n-1-i][j]+cost[i+1][j]:
                        self.path[i][j].append((j,n-1-i))
                    if cost[i][j] == self.costs_right[j-1][n-i]+cost[i][j-1]:
                        self.path[i][j].append((j-1,n-i))
                else:
                    #cost[i][j] == self.costs_up[n-1-i][j]+cost[i+1][j]
                    #self.path[i][j].append((j,n-1-i))
                    cost[i][j] == self.costs_right[j-1][n-i]+cost[i][j-1]
                    self.path[i][j].append((j-1,n-i))
                    
        #for i in self.path:
            #print(i)


        #print("cost:")
        #for i in cost:
            #print(i)


        self.ans_cost = cost[0][-1]
        #print(self.ans_cost)

        self.path_list = []
        self.path_list.append([(n,n)])
        i = 0
        j = n
        ans = self.path[i][j]
        #print(ans)
        self.path_list.append(ans)
        while ans!= [(0,0)]:
            i = n-ans[0][1]
            j = ans[0][0]
            ans = self.path[i][j]
            #print(ans)
            self.path_list.append(ans)
            
        
        #for i in range(len(self.path_list)-1,-1,-1):
        #    print(self.path_list[i][0][0], self.path_list[i][0][1])

        #print(len(self.path_list))

        
        

        

        
       
        

    def output(self): # You can modify it by yourself, but the output format should be correct.
        with open("%s" % args.output, 'w', newline='') as file_out:
            #file_out.writelines('RoutingCost %d'% self.grid_cost[self.By2][self.Bx2])
            file_out.writelines('RoutingCost %d'% self.ans_cost)
            #file_out.writelines('\nRoutingPath %d'% len(self.routing_path))
            file_out.writelines('\nRoutingPath %d'% len(self.path_list))
            #for i in range(len(self.routing_path)):
            for i in range(len(self.path_list)-1,-1,-1):
                file_out.writelines('\n%d %d'% (self.path_list[i][0][0], self.path_list[i][0][1]))
            
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './500x500.in',help="Input file root.")
    parser.add_argument("--output", type=str, default = './500x500.out',help="Output file root.")
    args = parser.parse_args()

    print('#################################################')
    print('#              Monotonic Routing                #')
    print('################################################# \n')

    routing = mono_routing(args)
    """Parser"""
    routing.parser()
    print('################ Parser Down ####################')
    """monotonic route"""
    start = time.time()
    routing.routing()
    print('run time:', round(time.time()-start,3))
    """output"""
    routing.output()
