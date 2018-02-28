import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score
from keras.models import Sequential
from keras.layers import Dense
# from keras.layers import LSTM
from math import sqrt
import numpy as np
# import lstms as LS
import tensorflow as tf


def readfile(location):
    # Read files in folder and store the dataframe into a list
    allist = []
    a = 0
    for filename in os.listdir(location):
        if filename.endswith(".csv"):
            temp = pd.read_csv(filename)
            # print (filename)
            temp.drop(columns=["time"], axis=1, inplace=True)
            allist.append(temp)

            a = a + 1
    # print (a)
    return allist


# pick up air datas to calculate
def pick_datas(df, air):
    temp = pd.DataFrame()
    obss = [air, "NO", "NOx", "AMB_TEMP", "RAINFALL", "RH"]
    for colname, values in df.iteritems():
        if colname in obss:
            temp[colname] = values
    temp = temp[obss]
    return temp


# pick up air datas in a list of dataframe
def pick_datas_in_list(dflist, air):
    temp = []
    df = pd.DataFrame()
    for items in dflist:
        df = pick_datas(items, air)
        temp.append(df)
    return temp


# supervised in list
def series_to_supervised_in_list(datalist):
    temptolist = []
    temp = pd.DataFrame()
    for items in datalist:
        temp = series_to_supervised(items, 1, 1)
        temptolist.append(temp)
    # print (temptolist)
    return temptolist


# split the training and test data in list
# remake the form
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
    # from sklearn.preprocessing import LabelEncoder, OneHotEncoder
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # train_x = scaler.fit_transform(train_x)
    # test_x = scaler.fit_transform(test_x)

    for items in datas:
        temptrain = items.iloc[:n_train_hours, :]
        temptest = items.iloc[n_train_hours:, :]
        # print (temptest.shape)
        # print (temptrain.shape)
        train_x, train_y = temptrain.iloc[:, :5].values, temptrain.iloc[:, 0].values
        test_x, test_y = temptest.iloc[:, :5].values, temptest.iloc[:, 0].values

        # for feature in range(len(temptrain)):
        #     trainmax_x = train_x[feature].max()
        #     train_x[feature] = (train_x[feature] - trainmax_x) * (-1)
        #     #print (train_x[feature])
        # for feature in range(len(temptest)):
        #     testmax_x = test_x[feature].max()
        #     test_x[feature] = (test_x[feature] - testmax_x) * (-1)
        # onehotencoder = OneHotEncoder(categorical_features=[1])
        # train_x = onehotencoder.fit_transform(train_x)
        # print(train_x.shape)
        # test_x = onehotencoder.fit_transform(test_x).toarray()
        scaler = MinMaxScaler(feature_range=(0, 1))
        train_x = scaler.fit_transform(train_x)
        test_x = scaler.fit_transform(test_x)
        # print (len(train_x),len(train_y))
        # print (len(test_x),len(test_y))
        # reshape input to be 3D [samples, timesteps, features]
        # train_x = train_x.values.reshape((train_x.shape[0], 1, train_x.shape[1]))
        # test_x = test_x.values.reshape((test_x.shape[0], 1, test_x.shape[1]))

        ### add into list
        trainlistx.append(train_x)
        trainlisty.append(train_y)
        testlistx.append(test_x)
        testlisty.append(test_y)
        ##### split into input and output
    return trainlistx, trainlisty, testlistx, testlisty


def model_ANN_build(trainlistx, trainlisty, testlistx, testlisty):
    classifier = Sequential()

    # Adding the input layer and the first hidden layer
    classifier.add(Dense(output_dim=3, activation='relu', input_shape=(5,)))

    # Adding the second hidden layer
    classifier.add(Dense(output_dim=3, init='uniform', activation='relu'))

    # classifier.add(Dense(output_dim=2, init='uniform', activation='relu'))
    # classifier.add(Dense(output_dim=10, init='uniform', activation='relu'))

    # Adding the output layer
    classifier.add(Dense(output_dim=1, init='uniform', activation='softmax'))

    # compile the model
    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Feature Scaling
    from sklearn.preprocessing import StandardScaler

    sc = StandardScaler()

    for i in range(len(trainlistx)):
        # print (trainlistx[i].shape)
        classifier.fit(trainlistx[i], trainlisty[i], batch_size=5, nb_epoch=20)

    for i in range(len(testlistx)):
        temptestx = sc.fit_transform(testlistx[i])
        temptesty = testlisty[i]
        yhat = classifier.predict(temptestx)
        new_list_y.extend(temptesty)
        new_list_yhat.extend(yhat)

    mse = mean_squared_error(new_list_y, new_list_yhat)

    rmse = sqrt(mean_squared_error(new_list_y, new_list_yhat))

    mae = mean_absolute_error(new_list_y, new_list_yhat)

    # print('Test score:', score[0])

    # acc = accuracy_score(new_list_y,new_list_yhat ,normalize=False)

    return rmse, mse, mae


datas = readfile("/Users/candacechou/Desktop/Airquality/five_year")

trainlistx, trainlisty, testlistx, testlisty = train_test_set_in_list(pick_datas_in_list(datas, "CO"))
# = train_test_set_in_list(CO)
rmse, mse, mae = model_ANN_build(trainlistx, trainlisty, testlistx, testlisty)
print("rmse:", rmse)
print("mse:", mse)
print("mae:", mae)
# print ("accuracy score:",acc)
