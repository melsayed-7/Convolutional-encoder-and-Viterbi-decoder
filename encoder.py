def convolutional_encoder(seq):
    s_0 = 0
    s_1 = 0
    
    encoded = []

    x_1 = s_0 ^ s_1 ^ seq[0]
    x_2 = s_0 ^ seq[0]

    encoded.append(x_1)
    encoded.append(x_2)

    for i in range(len(seq)-1):
        s_0 = s_1
        s_1 = seq[i]
        s_2 = seq[i+1]

        x_1 = s_0 ^ s_1 ^ s_2
        x_2 = s_0 ^ s_2

        encoded.append(x_1)
        encoded.append(x_2)

    
    return encoded


# test = [1,0,0,1,1]

 

# result = convolutional_encoder(test)
# print(result)