import h5py
import random
import numpy as np

#batch_num=1000
size=19

def roll(matrix,transpose=False,rotate=0):
    if transpose:
        matrix=matrix.T
    return np.rot90(matrix,k=rotate)

file_with_path='../SGF_Parser/sgf_hdf5/h5py.h5'
class HDF5OBJ:
    def __init__(self,file_with_path,mode='a'):
        self.file_handle=h5py.File(file_with_path,mode)

    def fetchRandomData(self,batch):
        sub_dir_len=len(self.file_handle['z'].keys())
        data_x=[] 
        data_y=[] 
        for i in range(batch):
            sub_rand_num=random.randint(0,sub_dir_len-1)
            lens=self.file_handle['z'][str(sub_rand_num)].len()
            num=random.randint(0,lens-1)
            #print(sub_rand_num,num)
            x=self.file_handle['x'][str(sub_rand_num)][num]
            y=self.file_handle['y'][str(sub_rand_num)][num]
            z=self.file_handle['z'][str(sub_rand_num)][num]
            #x,y,z全部变成19*19的整数
            x=x.astype(int)
            y=y.astype(int)
            t=np.zeros((19,19))
            t[tuple(y.tolist())]=1
            y=t
            z=int(z)
            z=z*np.ones((19,19))
            #对获取的数据增加随机变形功能
            transpose=random.randint(0,1)
            rotate=random.randint(0,3)
            x=roll(x,transpose=transpose,rotate=rotate) #当前局势
            y=roll(y,transpose=transpose,rotate=rotate) #该下哪一步
            y=y.astype(int).flatten()
            z=z.astype(int) #该谁下
            w=1-np.abs(x) #哪些地方可以下
            #z=roll(z,transpose=transpose,rotate=rotate)
            data_x.append([x,z,w])
            data_y.append(y)
        return np.array(data_x).reshape(batch,size,size,3),np.array(data_y) #调整成tf的图像格式

'''for test
obj5=HDF5OBJ(file_with_path)
[a,b]=obj5.fetchRandomData(2)
print(a,a.shape)
print(b,b.shape)

'''

            

