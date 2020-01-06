import h5py
import numpy as np
import glob

batch_num=1

class HDF5Integration: #把sgf分析好的数据，集成到hdf5文件中去
    def __init__(self,file_with_path,mode='a'):
        self.file_handle=h5py.File(file_with_path,mode)

    def saveAllNpzs(self,dir): #一次性录入全部数据
        self.file_handle.clear() #clear并不会释放文件所占的磁盘空间
        x_data=np.zeros((1,19,19))
        y_data=np.zeros((1,2))
        z_data=np.zeros((1,))
        count=0
        batch=0
        for file_name in glob.iglob(dir+'*win*.npz'): #dir目录下npz目录的全部npz文件
            print("Processing:",file_name,count)
            npzs=np.load(file_name)
            if npzs['x'].size==0 or npzs['y'].size==0 or npzs['z'].size==0: #部分原始sgf文件是空的
                continue
            x_data=np.vstack((x_data,npzs['x']))
            y_data=np.vstack((y_data,npzs['y']))
            z_data=np.hstack((z_data,npzs['z']))
            #print(z_data.shape)
            count+=1
            if count%batch_num==0:
                print("Writing:",batch)
                count=0
                '''
                #self.file_handle['x/'+str(batch)]=x_data[1:]
                #self.file_handle['y/'+str(batch)]=y_data[1:]
                #self.file_handle['z/'+str(batch)]=z_data[1:]
                '''
                self.file_handle.create_dataset('x/'+str(batch), data=x_data[1:],  compression="lzf")
                self.file_handle.create_dataset('y/'+str(batch), data=y_data[1:],  compression="lzf")
                self.file_handle.create_dataset('z/'+str(batch), data=z_data[1:],  compression="lzf")
                batch+=1
                x_data=np.zeros((1,19,19))
                y_data=np.zeros((1,2))
                z_data=np.zeros((1,))
        '''
        #self.file_handle['x/'+str(batch)]=x_data[1:]
        #self.file_handle['y/'+str(batch)]=y_data[1:]
        #self.file_handle['z/'+str(batch)]=z_data[1:]
        '''
        if count!=0:
            print("Writing:",batch)
            self.file_handle.create_dataset('x/'+str(batch), data=x_data[1:],  compression="lzf")
            self.file_handle.create_dataset('y/'+str(batch), data=y_data[1:],  compression="lzf")
            self.file_handle.create_dataset('z/'+str(batch), data=z_data[1:],  compression="lzf")
        #batch+=1
        #x_data=np.zeros((1,19,19))
        #y_data=np.zeros((1,2))
        #z_data=np.zeros((1,))
        
    ''' 暂不实现，下面是错误的
    def addNpzs(self,dir): #追加某个目录下的全部数据
        
        for file_name in glob.iglob(dir+'/*win*.npz'): #dir目录下npz目录的全部npz文件
            #npzs=np.load(file_name,allow_pickle=True)
            npzs=np.load(file_name)
            x_data=np.vstack((x_data,npzs['x']))
            y_data=np.vstack((y_data,npzs['y']))
            z_data=np.hstack((z_data,npzs['z']))
        
        self.file_handle['x']=x_data
        self.file_handle['y']=y_data
        self.file_handle['z']=z_data
    '''
file_with_path='./sgf_hdf5/h5py.h5'
dir='./npz1/'
hdf5=HDF5Integration(file_with_path,'w')
hdf5.saveAllNpzs(dir)



