import numpy as np
from encoder import *

def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i + n]
        if len(val) == n:
            yield tuple(val)


def generate_bits(n, p):
    try:
        return (np.random.rand(*n) > p).astype(int)
    except TypeError:
        return (np.random.rand(n) > p).astype(int)


class ViterbiHard(object):

    def __init__(self):
        self.message = []
        

        # channel-coded data for comparing errors
        self.zero_zero = (0, 0)
        self.zero_one = (0, 1)
        self.one_zero = (1, 0)
        self.one_one = (1, 1)

    def conv_encode(self):
        
        output = []
    
        bucket = list(generate_bits(10000, 0.5))  # generate lots at once
        # bucket = [1,0,0,1,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,0,0,1,0,0]
        self.message += bucket
        # decrease the weights equally every so often

        output = convolutional_encoder(bucket)
        return output

    def dist(self, one, two):
        return sum((one[0] != two[0], one[1] != two[1]))


    def run(self):
        """ Runs the decoder on data as it's produced by `conv_encode`. Yields the original bit from `self.message`
         along with the received bit. """
        # initialize the states so beginning at 00 will be the cheapest path
        res = []

        path_1 = []
        path_2 = []
        path_3 = []
        path_4 = []

        path_1_w = [0]
        path_2_w = [0]
        path_3_w = [0]
        path_4_w = [0]

        prev_1 = []
        prev_2 = []
        prev_3 = []
        prev_4 = [] 
        
            # pass bits through BSC
        received = self.conv_encode()

        for bit_pair in group(received, 2):
            w_1 = path_1_w[-1]
            w_2 = path_2_w[-1]
            w_3 = path_3_w[-1]
            w_4 = path_4_w[-1]



            # 00->00 case
            weight1 =w_1 + self.dist(bit_pair, self.zero_zero)
            # 01->00 case
            weight2 = w_2 +self.dist(bit_pair, self.one_one)
            if weight1 <= weight2:
                
                path_1 = path_1 + [0, 0] 
                path_1_w.append(weight1)
                 
                prev_1.append([0,0])

            else:
                
                path_1 = path_1 + [1,1]
                path_1_w.append(weight2)
                
                prev_1.append([0,1])
                    
               

            # 10->01 case
            weight1 =  w_3 + self.dist(bit_pair, self.one_zero)
            # 11->01 case
            weight2 =  w_4 + self.dist(bit_pair, self.zero_one)
            if weight1 <= weight2:
                
                path_2 = path_2 + [0, 1]
                path_2_w.append(weight1)

             
                prev_2.append([1,0])
                    

            else:
                
                path_2 = path_2 + [1, 0]
                path_2_w.append(weight2)
                prev_2.append([1,1])
                

            # 00->10 case
            weight1 =  w_1 + self.dist(bit_pair, self.one_one)
            # 01->10 case
            weight2 =   w_2 + self.dist(bit_pair, self.zero_zero)
            if weight1 <= weight2:
                
                path_3 = path_3 + [1,1]
                path_3_w.append(weight1)

                
                    
                prev_3.append([0,0])
                
                
            else:
               
                path_3 = path_3 + [0,0]
                path_3_w.append(weight2)
                prev_3.append([0,1])

               
                # if(len(path_3_w)==0):
                    
                # else:
                #     path_3_w.append(weight2+path_3_w[-1])
                #     prev_3.append([0,1])

            # 10->11 case
            weight1 =   w_3 + self.dist(bit_pair, self.zero_one)
            # 11->11 case
            weight2 =   w_4 + self.dist(bit_pair, self.one_zero)
            if weight1 <= weight2:
                
                path_4 = path_4 + [1, 0]
                path_4_w.append(weight1)

               
                prev_4.append([1,0])
                
            else:
                
                path_4 = path_4 + [0,1]
                path_4_w.append(weight2)
              
                prev_4.append([1,1])
                

           
        backward_path = []
        length = len(path_1_w)
        for i in range(len(path_1_w)):
            end = [path_1_w[-1],path_2_w[-1],path_3_w[-1],path_4_w[-1]]
            end_path = [path_1[-2:],path_2[-2:],path_3[-2:],path_4[-2:]]
            min_index = end.index(min(end))
            backward_path.append(end_path[min_index])
             
            path_1_w = path_1_w[:-1]
            path_2_w = path_2_w[:-1]
            path_3_w = path_3_w[:-1]
            path_4_w = path_4_w[:-1]
            
            if (i != length-1):
                path_1 = path_1[:-2]
                path_2 = path_2[:-2]
                path_3 = path_3[:-2]
                path_4 = path_4[:-2]

            else:
                path_1 = path_1
                path_2 = path_2
                path_3 = path_3
                path_4 = path_4
            
                    

        res = backward_path[:-1]
        # print(res)
        res.reverse()
        final_res = []

        for i in range(len(res)):
            final_res.append(res[i][0])
            final_res.append(res[i][1])

        for i in range(0,len(final_res),2):
            if (final_res[i] != final_res[i+1]):
                temp = final_res[i]
                final_res[i] = final_res[i+1]
                final_res[i+1] = temp
        
        return final_res, received





experiment = ViterbiHard()
output, message = experiment.run()

print(message)
print(output)
print(output == message)



# print(len(output))
# print(error_count)