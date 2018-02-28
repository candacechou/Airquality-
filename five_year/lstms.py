import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error,mean_absolute_error,accuracy_score
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
import numpy as np
import tensorflow as tf
def readfile(location):
    #####read files in folder and store the dataframe into a list
    allist = []
    a = 0
    for filename in os.listdir(location):
        if filename.endswith(".csv"):
            temp = pd.read_csv(filename)
            #print (filename)
            temp.drop(columns = ["time"], axis=1,inplace=True)
            allist.append(temp)

            a = a + 1
    # print (a)
    return allist


# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    for vars, values in agg.iteritems():
        if "t-1" not in vars and "var1" not in vars:
            # print("hi")
            try:
                agg.drop(columns=[vars], axis=1,inplace=True)
            except:
                print("higa")
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
#pick up air datas to calculate
def pick_datas(df,air):
    temp = pd.DataFrame()
    obss = [air,"NO","NOx","AMB_TEMP","RAINFALL","RH"]
    for colname, values in df.iteritems():
        if colname in obss :
            temp[colname] = values
    temp =temp[obss]
    return temp
# pick up air datas in a list of dataframe
def pick_datas_in_list(dflist,air):
    temp = []
    df = pd.DataFrame()
    for items in dflist:
        df = pick_datas(items,air)
        temp.append(df)
    return temp
### supervised in list
def series_to_supervised_in_list(datalist):
    temptolist = []
    temp = pd.DataFrame()
    for items in datalist:
        temp = series_to_supervised(items, 1, 1)
        temptolist.append(temp)
    #print (temptolist)
    return temptolist

##### split the training and test data in list
def train_test_set_in_list(datas):
    trainlistx = []
    trainlisty = []
    testlistx = []
    testlisty = []
    temptrain = pd.DataFrame()
    temptest = pd.DataFrame()
    train_x = pd.DataFrame()
    train_y = pd.DataFrame()
    test_x = pd.DataFrame()
    test_y = pd.DataFrame()
    #### split four years as training data
    n_train_hours = 365 * 24 * 3
    for items in datas:

        temptrain = items.iloc[:n_train_hours, :]
        temptest = items.iloc[n_train_hours:, :]
        #print (temptest.shape)
        #print (temptrain.shape)
        train_x , train_y = temptrain.iloc[:,:5],temptrain.iloc[:,0]
        test_x, test_y = temptest.iloc[:,:5],temptest.iloc[:,0]
        #scaler = MinMaxScaler(feature_range=(0, 1))
        #train_x = scaler.fit_transform(train_x)
        #test_x = scaler.fit_transform(test_x)
        #print (len(train_x),len(train_y))
        #print (len(test_x),len(test_y))
        # reshape input to be 3D [samples, timesteps, features]
        train_x = train_x.values.reshape((train_x.shape[0], 1, train_x.shape[1]))
        test_x = test_x.values.reshape((test_x.shape[0], 1, test_x.shape[1]))

        ### add into list
        trainlistx.append(train_x)
        trainlisty.append(train_y)
        testlistx.append(test_x)
        testlisty.append(test_y)
        ##### split into input and output
    return trainlistx,trainlisty,testlistx,testlisty

#### create a model
def model_build(trainlistx, trainlisty, testlistx, testlisty):
    print ('hi')
    model = Sequential()
    model.add(LSTM(50, input_shape=(trainlistx[0].shape[1], trainlistx[0] .shape[2])))
    model.add(Dense(1))
    model.compile(loss='mae', optimizer='adam')
    #### MODEL fit
    for i in range(len(trainlistx)):
        history = model.fit(trainlistx[i],trainlisty[i],
                            epochs=50, batch_size=72, validation_data=None, verbose=2, shuffle=False)
    #### make a prediction
    new_list_y = []
    new_list_yhat = []
    for i in range(len(testlistx)):
        temptestx = testlistx[i]
        temptesty = testlisty[i]
        yhat = model.predict(temptestx)
        #print (temptesty.shape)
        #print (temptestx.shape)
        #print(len(yhat),type(yhat))
        #new_list_yhat.extend(yhat)
        temptestx = temptestx.reshape((temptestx.shape[0], temptestx.shape[2]))
        ### inverse scaling for forcast
        #print(temptestx.shape)
        inv_yhat = np.concatenate((yhat, temptestx[:, 1:]), axis=1)
        inv_yhat = inv_yhat[:, 0].tolist()
        new_list_yhat.extend(inv_yhat)
        #new_list_yhat.extend(inv_yhat)
        ### inverse scaling for actual
        #temptesty = temptesty.reshape((len(temptesty), 1))
        #print (len(temptesty))
        #print (temptestx.shape)
        #inv_y = np.concatenate((temptesty, temptestx[:, 1:]), axis=1)
        #inv_y = inv_y[:,0].tolist()
        new_list_y.extend(temptesty)
    ###calculate the RMSE
    #print (len(new_list_yhat),len(new_list_y))
    mse = mean_squared_error(new_list_y, new_list_yhat)
    rmse = sqrt(mean_squared_error(new_list_y, new_list_yhat))
    mae = mean_absolute_error(new_list_y, new_list_yhat)
    #acc = accuracy_score(new_list_y,new_list_yhat ,normalize=False)
    return rmse,mse,mae



# datas = readfile("/Users/candacechou/Desktop/Airquality/five_year")
#
# CO = series_to_supervised_in_list(pick_datas_in_list(datas,"O3"))
# trainlistx, trainlisty, testlistx, testlisty = train_test_set_in_list(CO)
# rmse,mse,mae = model_build(trainlistx,trainlisty,testlistx,testlisty)
# print ("rmse:", rmse)
# print ("mse:",mse)
# print ("mae:",mae)
#print ("accuracy score:",acc)
#print(normalized_the_feature_in_list(datas))

# # integer encode direction
# encoder = LabelEncoder()
# datas[1].iloc[:, 4] = encoder.fit_transform(datas[1].iloc[:, 4])
# values = datas[1].iloc[:, 1:]
# # ensure all data is float
# values = values.astype('float32')
# # normalize features
# #scaler = MinMaxScaler(feature_range=(0, 1))
# #scaled = scaler.fit_transform(values)
# # frame as supervised learning
# reframed = series_to_supervised(values, 1, 1)
#
# print(reframed.head())
#
# values = reframed.values
# n_train_hours = 365 * 24 * 3
# train = values[:n_train_hours, :]
# test = values[n_train_hours:, :]
# # split into input and outputs
# train_X, train_y = train[:, :-1], train[:, -1]
# test_X, test_y = test[:, :-1], test[:, -1]
# # reshape input to be 3D [samples, timesteps, features]
# train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
# test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
# print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
#
# # design network
# model = Sequential()
# model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
# model.add(Dense(1))
# model.compile(loss='mae', optimizer='adam')
# # fit network
# history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# # plot history
# # pyplot.plot(history.history['loss'], label='train')
# # pyplot.plot(history.history['val_loss'], label='test')
# # pyplot.legend()
# # pyplot.show()
# # make a prediction
# yhat = model.predict(test_X)
# test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# # invert scaling for forecast
# inv_yhat = np.concatenate((yhat, test_X[:, 1:]), axis=1)
# #inv_yhat = scaler.inverse_transform(inv_yhat)
# inv_yhat = inv_yhat[:,0]
# # invert scaling for actual
# test_y = test_y.reshape((len(test_y), 1))
# inv_y = np.concatenate((test_y, test_X[:, 1:]), axis=1)
# #inv_y = scaler.inverse_transform(inv_y)
# inv_y = inv_y[:,0]
# # calculate RMSE
# rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
# print('Test RMSE: %.3f' % rmse)