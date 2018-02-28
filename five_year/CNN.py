from sklearn.metrics import mean_squared_error,mean_absolute_error, accuracy_score
from keras.models import Sequential
from keras.layers import Dense
#from keras.layers import LSTM
from math import sqrt
import numpy as np
import lstms as LS

def model_CNN_Build (trainlistx, trainlisty, testlistx, testlisty):
    new_list_y = []
    new_list_yhat = []
    model = Sequential()
    model.add(Conv2D(24, kernel_size=(4, 4), strides=(1, 1),
                     activation='relu',
                     input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
    model.add(Conv2D(48, (5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(1000, activation='relu'))
    model.add(Dense(6, activation='softmax'))
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.SGD(lr=0.01),
                  metrics=['accuracy'])
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    for i in range(len(trainlistx)):
        temp = sc.fit_transform(trainlistx[i])
        model.fit(temp, trainlisty[i],
                batch_size=10,
                epochs=100,
                verbose=1)
    for i in range(len(testlistx)):
        temptestx = testlistx[i]
        temptesty = testlisty[i]
        yhat = model.predict(temptestx)
        new_list_y.extend(temptesty)
        new_list_yhat.extend(yhat)
    mse = mean_squared_error(new_list_y, new_list_yhat)
    rmse = sqrt(mean_squared_error(new_list_y, new_list_yhat))
    mae = mean_absolute_error(new_list_y, new_list_yhat)
    #acc = accuracy_score(new_list_y,new_list_yhat ,normalize=False)
    return rmse, mse, mae

datas = LS.readfile("/Users/candacechou/Desktop/Airquality/five_year")

CO = LS.series_to_supervised_in_list(LS.pick_datas_in_list(datas,"CO"))
trainlistx, trainlisty, testlistx, testlisty = LS.train_test_set_in_list(CO)
rmse,mse,mae = model_ANN_build(trainlistx,trainlisty,testlistx,testlisty)
print ("rmse:", rmse)
print ("mse:",mse)
print ("mae:",mae)
#print ("accuracy score:" ,acc)
