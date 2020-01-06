#使用卷积网络进行监督训练
import sys
#import os.path
sys.path.append("..")
#sys.path.append("../..")
from keras.models import Sequential
from keras.layers import Dense,Conv2D,Flatten,MaxPooling2D,Dropout
from utility.genDataFromHDF5 import HDF5OBJ
import keras
size=19
file_with_path='../SGF_Parser/sgf_hdf5/h5py.h5'
h5_path='../agentTrainModel/models/'

class modelConvEasy:
    def __init__(self):
        self.model=Sequential()
        self.constructModel()
    def constructModel(self):
        self.model.add(Conv2D(512,(2,2),input_shape=(19,19,3),activation='tanh',dilation_rate=(2, 2)))
        
        #self.model.add(Dropout(rate=0.1))
        
        self.model.add(Conv2D(512,(2,2),activation='tanh'))
        self.model.add(MaxPooling2D())
        
        self.model.add(Conv2D(512,(2,2),activation='tanh'))
        self.model.add(MaxPooling2D())
        self.model.add(Dropout(0.1))
        #'''
        self.model.add(Conv2D(256,(2,2),activation='tanh'))
        #self.model.add(Conv2D(256,(2,2),activation='tanh'))
        #self.model.add(MaxPooling2D())
        self.model.add(Dropout(0.25))
        #'''
        self.model.add(Flatten())
        self.model.add(Dense(1024,activation='tanh'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(1024,activation='relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(512,activation='relu'))        
        self.model.add(Dense(size*size,activation='softmax'))

    def compile(self):
        #opt = keras.optimizers.rmsprop(lr=0.0001,decay=1e-6)
        opt=keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
        self.model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])

    def run(self,batch_size):
        self.loadWeights()
        def genData(obj5,batch_size):
            while True:
               yield obj5.fetchRandomData(batch_size)
        obj5=HDF5OBJ(file_with_path)
        self.model.fit_generator(genData(obj5,batch_size),
            #steps_per_epoch=1024,
            #epochs=1024,
            steps_per_epoch=8,
            epochs=2,
            callbacks=[ #为了避免训练中断，每次训练都保存一下，model.load_weights("easy_model_epoch.h5") 装载保存的权重
                #keras.callbacks.ModelCheckpoint(check_path+'small_model_epoch_{epoch}.h5')
                keras.callbacks.ModelCheckpoint(h5_path+'easy_model_epoch.h5',period=1) #每一个epoch保存一次，并覆盖
            ]
        )
        self.saveModel()
    def loadWeights(self):
        #self.model.load_weights(check_path+"easy_model_epoch.h5")
        #'''
        try: #文件如果没有就跳过
            self.model.load_weights(h5_path+"easy_model_epoch.h5")
        except IOError:
            print("Warning:easy_model_epoch.h5 error. No such file.")  
        #'''      
    def predict(self,input):
        return self.model.predict(input) #这里返回原始值，怎么加工就留给调用的人
    
    def saveModel(self):
        self.model.save(h5_path+'easy_model.h5')
    
    def loadModel(self):
        keras.models.load_model(h5_path+'easy_model.h5')
    '''
    def evaluate(self):
        pass
    '''
model=modelConvEasy()
model.compile()
model.run(128)
