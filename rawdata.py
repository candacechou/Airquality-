import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import re
import xlrd
import dateutil

pd.options.display.encoding = sys.stdout.encoding


# def Checkfunction(df,initime):
#     months=0
#     year=0
#     for i in range(0,16):
#         time = initime + dateutil.relativedelta(months=1)
#         for j in range(1,12):
#             time=initime +dateutil.relativedelta(months=j)
#             if j==1 or j==3 or j==5 or j==7 or j==8 or j==10 or j==12:
#                 if len(df[time].index) !=744:
#                     print ("error",df[time])
#             if j==4 or j==6 or j==9 or j==1:
#                 if len(df[time].index) !=720:
#                     print ("error",df[time])
#             if j==2 and (i==0 or i==4 or i==8 or i==12 or i==16):
#                 if len(df[time].index) != 696:
#                     print ("error",df[time])
#             if j ==2 and (i!=0 or i!=4 or i!=8 or i!=12 or i!=16):
#                 if len(df[time].index) != 672:
#                     print ("error" , df[time])
#     return "----"


def dataframe2timeseries(df, air) -> dict:
    dftemp = {}

    for times, rows in df.iterrows():
        for hours, items in rows.iteritems():
            if hours is not 'items' and items is not air:

                tempitems = str(items)
                temphours = int(hours)
                newdatetime = times + dt.timedelta(hours=temphours)

                if ' ' in tempitems:
                    tempitems.replace(' ', '')

                if not tempitems:
                    foo5 = dftemp[newdatetime] = findlastdate(dftemp, newdatetime)

                elif 'x' in tempitems:
                    dftemp[newdatetime] = float(re.sub('x', '', tempitems))
                    foo = dftemp[newdatetime]

                    try:
                        float(re.sub('x', '', tempitems))
                    except ValueError:
                        print(type(foo))
                    dftemp[newdatetime] = float(re.sub('x', '', tempitems))

                elif '#' in tempitems:
                    if tempitems == '#':
                        dftemp[newdatetime] = 0.0
                        foo4 = float(dftemp[newdatetime])
                        #print(type(foo4))
                    try:
                        dftemp[newdatetime] = float(re.sub('#', '', tempitems))
                    except ValueError:
                        dftemp[newdatetime] = findlastdate(dftemp, newdatetime)

                elif '*' in tempitems:
                    foo3 = float(re.sub('[*]', '', tempitems))

                    try:
                        float(re.sub('[*]', '', tempitems))
                    except ValueError:
                        print(type(foo3))

                    dftemp[newdatetime] = float(re.sub('[*]', '', tempitems))

                elif tempitems == 'NR':
                    dftemp[newdatetime] = 0

                elif 'xxx' in tempitems:
                    dftemp[newdatetime] = findlastdate(dftemp, newdatetime)

                else:
                    dftemp[newdatetime] = float(items)

                    # print (dftemp)

    NewDataFrame = pd.DataFrame.from_records(data=list(dftemp.items()), columns=['time', air])

    NewDataFrame.reset_index(inplace=True)

    NewDataFrame['time'] = pd.to_datetime(NewDataFrame['time'])

    NewDataFrame = NewDataFrame.set_index('time').resample('H').bfill()

    del NewDataFrame['index']

    # NewDataFrame = NewDataFrame.reindex(pd.date_range(start=NewDataFrame.index[0], end=NewDataFrame.index[-1], freq='30s'))

    return NewDataFrame


def findlastdate(df, time) -> float:
    temp = 0.0

    if time - dt.timedelta(days=1) in df:
        temp = df[time - dt.timedelta(days=1)]

    else:
        temp = df[time - dt.timedelta(hours=1)]

    return float(temp)


def dealwithcsv(name, air):
    if 'csv' in name:

        Doc = pd.read_csv(name, header=0, encoding="big5")
        Doc = Doc.rename(index=str, columns={"日期": "DATE"})
        Doc = Doc.rename(index=str, columns={"測項": "items"})
        Doc['DATE'] = pd.to_datetime(Doc['DATE'])
        Doc.index = Doc['DATE']
        del Doc['DATE']
        del Doc['測站']
        Doc_ts = dataframe2timeseries(Doc[Doc['items'] == air], air)
    elif 'xls' in name:
        Doc = pd.read_excel(name, header=0)
        Doc = Doc.rename(index=str, columns={"日期": "DATE"})
        Doc = Doc.rename(index=str, columns={"測項": "items"})
        Doc['DATE'] = pd.to_datetime(Doc['DATE'])
        Doc.index = Doc['DATE']
        del Doc['DATE']
        del Doc['測站']
        Doc_ts = dataframe2timeseries(Doc[Doc['items'] == air], air)
    # print (air, len(Doc_ts.index))
    return Doc_ts


def dataframemerge(air, name):
    name1 = name[0]
    name2 = name[1]
    name3 = name[2]
    name4 = name[3]
    name5 = name[4]
    name6 = name[5]
    name7 = name[6]
    name8 = name[7]
    name9 = name[8]
    name10 = name[9]
    name11 = name[10]
    name12 = name[11]
    name13 = name[12]
    name14 = name[13]
    name15 = name[14]
    name16 = name[15]
    name17 = name[16]

    return pd.concat([dealwithcsv(name1, air), dealwithcsv(name2, air),
                      dealwithcsv(name3, air), dealwithcsv(name4, air),
                      dealwithcsv(name5, air), dealwithcsv(name6, air),
                      dealwithcsv(name7, air), dealwithcsv(name8, air),
                      dealwithcsv(name9, air), dealwithcsv(name10, air),
                      dealwithcsv(name11, air), dealwithcsv(name12, air),
                      dealwithcsv(name13, air), dealwithcsv(name14, air),
                      dealwithcsv(name15, air), dealwithcsv(name16, air),
                      dealwithcsv(name17, air)])


def alldataprepare(name1, name2, name3, name4, name5, name6,
                   name7, name8, name9, name10, name11, name12,
                   name13, name14, name15, name16, name17):
    CO = dataframemerge("CO", name1, name2, name3, name4, name5, name6,
                        name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    TEMP = dataframemerge("AMB_TEMP", name1, name2, name3, name4, name5, name6,
                          name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    SO2 = dataframemerge("SO2", name1, name2, name3, name4, name5, name6,
                         name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    NO = dataframemerge("NO", name1, name2, name3, name4, name5, name6,
                        name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    NO2 = dataframemerge("NO2", name1, name2, name3, name4, name5, name6,
                         name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    NOx = dataframemerge("NOx", name1, name2, name3, name4, name5, name6,
                         name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    PM10 = dataframemerge("PM10", name1, name2, name3, name4, name5, name6,
                          name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    O3 = dataframemerge("O3", name1, name2, name3, name4, name5, name6,
                        name7, name8, name9, name10, name11, name12, name13, name14, name15, name16, name17)
    return CO, TEMP, SO2, NO, NO2, NOx, PM10, O3


##### 北部
SHANCHUN = []

# ------------------北部開始-------------------------------#
## 三重SHANCHUN

SHANCHUN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年三重站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年三重站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年三重站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年三重站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年三重站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年三重站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年三重站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年三重站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年三重站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年三重站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年三重站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年三重站_20170217.xls']
SHANCHUNO3 = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年土城站_20081006.csv',
              '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年土城站_20090901.csv',
              '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年土城站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年土城站_20090301.xls',
              '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年土城站_20100331.csv',
              '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年土城站_20110329.csv',
              '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年土城站_20120409.csv',
              '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年土城站_20130424.xls',
              '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年土城站_20140417.xls',
              '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年土城站_20170317.xls',
              '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年土城站_20160318.xls',
              '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年土城站_20170217.xls']
# # SHANCHUN_CO,SHANCHUN_TEMP, SHANCHUN_SO2, SHANCHUN_NO, SHANCHUN_NO2, SHANCHUN_NOx, SHANCHUN_PM10, SHANCHUN_O3 = alldataprepare(
# #                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年三重站_20081006.csv',
# #                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年三重站_20090901.csv',
# #                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年三重站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年三重站_20090301.xls',
# #                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年三重站_20100331.csv',
# #                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年三重站_20110329.csv',
# #                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年三重站_20120409.csv',
# #                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年三重站_20130424.xls',
# #                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年三重站_20140417.xls',
# #                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年三重站_20170317.xls',
# #                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年三重站_20160323.xls',
# #                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年三重站_20170217.xls')
# #
# #
# # SHANCHUN_O3 = dataframemerge("O3",
# #                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年土城站_20081006.csv',
# #                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年土城站_20090901.csv',
# #                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年土城站_20080801.csv',
# #                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年土城站_20090301.xls',
# #                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年土城站_20100331.csv',
# #                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年土城站_20110329.csv',
# #                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年土城站_20120409.csv',
# #                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年土城站_20130424.xls',
# #                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年土城站_20140417.xls',
# #                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年土城站_20170317.xls',
# #                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年土城站_20160318.xls',
# #                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年土城站_20170217.xls')
# #
# # print(len(SHANCHUN_CO.index),len(SHANCHUN_NO.index),len(SHANCHUN_NO2.index),len(SHANCHUN_NOx.index),
# #        len(SHANCHUN_O3.index),len(SHANCHUN_PM10.index),len(SHANCHUN_SO2.index),len(SHANCHUN_TEMP.index))
#
# #中壢Chungli
# ##  first five year has no o3 data , use longtan's
# CHUNGLI_CO,CHUNGLI_TEMP, CHUNGLI_SO2, CHUNGLI_NO, CHUNGLI_NO2, CHUNGLI_NOx, CHUNGLI_PM10, CHUNGLI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年中壢站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年中壢站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中壢站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中壢站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中壢站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中壢站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中壢站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中壢站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中壢站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中壢站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中壢站_20170217.xls')
CHUNGLI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年中壢站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年中壢站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中壢站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中壢站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中壢站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中壢站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中壢站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中壢站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中壢站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中壢站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中壢站_20160323.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中壢站_20170217.xls']
# CHUNGLI_O3 = dataframemerge("O3",
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年龍潭站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年龍潭站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中壢站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中壢站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中壢站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中壢站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中壢站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中壢站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中壢站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中壢站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中壢站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中壢站_20170217.xls')

CHUNGLIO3 = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年龍潭站_20081006.csv',
             '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年龍潭站_20090901.csv',
             '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年龍潭站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年龍潭站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年龍潭站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中壢站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中壢站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中壢站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中壢站_20090301.xls',
             '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中壢站_20100331.csv',
             '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中壢站_20110329.csv',
             '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中壢站_20120409.csv',
             '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中壢站_20130424.xls',
             '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中壢站_20140417.xls',
             '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中壢站_20170317.xls',
             '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中壢站_20160323.xls',
             '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中壢站_20170217.xls']
#
# # print (len(CHUNGLI_CO.index),len(CHUNGLI_TEMP.index), len(CHUNGLI_SO2.index), len(CHUNGLI_NO.index)
# #        ,len(CHUNGLI_NO2.index), len(CHUNGLI_NOx.index), len(CHUNGLI_PM10.index), len(CHUNGLI_O3.index))
# ##### 中山 CHUNGSHAN
#
# #
# CHUNGSHAN_CO,CHUNGSHAN_TEMP, CHUNGSHAN_SO2, CHUNGSHAN_NO, CHUNGSHAN_NO2, CHUNGSHAN_NOx, CHUNGSHAN_PM10,CHUNGSHAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年中山站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年中山站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中山站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中山站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中山站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中山站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中山站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中山站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中山站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中山站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中山站_20170217.xls')
#
# # print(len(CHUNGSHAN_CO.index),len(CHUNGSHAN_NO.index),len(CHUNGSHAN_NO2.index),len(CHUNGSHAN_NOx.index),
# #        len(CHUNGSHAN_O3.index),len(CHUNGSHAN_PM10.index),len(CHUNGSHAN_SO2.index),len(CHUNGSHAN_TEMP.index))
#

CHUNGSHAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年中山站_20081006.csv',
             '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年中山站_20090901.csv',
             '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年中山站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年中山站_20090301.xls',
             '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年中山站_20100331.csv',
             '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年中山站_20110329.csv',
             '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年中山站_20120409.csv',
             '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年中山站_20130424.xls',
             '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年中山站_20140417.xls',
             '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年中山站_20170317.xls',
             '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年中山站_20160318.xls',
             '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年中山站_20170217.xls']
# # ###古亭KOOTIN
# KOOTIN_CO,KOOTIN_TEMP, KOOTIN_SO2, KOOTIN_NO, KOOTIN_NO2, KOOTIN_NOx, KOOTIN_PM10, KOOTIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年古亭站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年古亭站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年古亭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年古亭站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年古亭站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年古亭站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年古亭站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年古亭站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年古亭站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年古亭站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年古亭站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年古亭站_20170217.xls')
#
# # print(len(KOOTIN_CO.index),len(KOOTIN_NO.index),len(KOOTIN_NO2.index),len(KOOTIN_NOx.index),
# #        len(KOOTIN_O3.index),len(KOOTIN_PM10.index),len(KOOTIN_SO2.index),len(KOOTIN_TEMP.index))
KOOTIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年古亭站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年古亭站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年古亭站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年古亭站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年古亭站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年古亭站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年古亭站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年古亭站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年古亭站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年古亭站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年古亭站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年古亭站_20170217.xls']
# # #####土城 TUCHAN
# TOOCHAN_CO,TOOCHAN_TEMP, TOOCHAN_SO2, TOOCHAN_NO, TOOCHAN_NO2, TOOCHAN_NOx, TOOCHAN_PM10, TOOCHAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年土城站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年土城站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年土城站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年土城站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年土城站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年土城站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年土城站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年土城站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年土城站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年土城站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年土城站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年土城站_20170217.xls')
#
# # print(len(TOOCHAN_CO.index),len(TOOCHAN_NO.index),len(TOOCHAN_NO2.index),len(TOOCHAN_NOx.index),
# #        len(TOOCHAN_O3.index),len(TOOCHAN_PM10.index),len(TOOCHAN_SO2.index),len(TOOCHAN_TEMP.index))
TOOCHAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年土城站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年土城站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年土城站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年土城站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年土城站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年土城站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年土城站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年土城站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年土城站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年土城站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年土城站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年土城站_20170217.xls']
# ## 基隆KEELUNG
# #
# KEELUNG_CO,KEELUNG_TEMP, KEELUNG_SO2, KEELUNG_NO, KEELUNG_NO2, KEELUNG_NOx, KEELUNG_PM10, KEELUNG_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年基隆站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年基隆站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年基隆站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年基隆站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年基隆站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年基隆站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年基隆站_20081120.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年基隆站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年基隆站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年基隆站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年基隆站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年基隆站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年基隆站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年基隆站_20140416.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年基隆站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年基隆站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年基隆站_20170217.xls')
KEELUNG = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年基隆站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年基隆站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年基隆站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年基隆站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年基隆站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年基隆站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年基隆站_20081120.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年基隆站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年基隆站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年基隆站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年基隆站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年基隆站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年基隆站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年基隆站_20140416.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年基隆站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年基隆站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年基隆站_20170217.xls']
# # print(len(KEELUNG_CO.index),len(KEELUNG_NO.index),len(KEELUNG_NO2.index),len(KEELUNG_NOx.index),
# #        len(KEELUNG_O3.index),len(KEELUNG_PM10.index),len(KEELUNG_SO2.index),len(KEELUNG_TEMP.index))
#
# # ##士林 SILIN
# SILIN_CO,SILIN_TEMP, SILIN_SO2, SILIN_NO, SILIN_NO2, SILIN_NOx, SILIN_PM10, SILIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年士林站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年士林站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年士林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年士林站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年士林站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年士林站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年士林站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年士林站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年士林站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年士林站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年士林站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年士林站_20170217.xls')
SILIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年士林站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年士林站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年士林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年士林站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年士林站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年士林站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年士林站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年士林站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年士林站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年士林站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年士林站_20160318.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年士林站_20170217.xls']
# # print(len(SILIN_CO.index),len(SILIN＿NO.index),len(SILIN_NO2.index),len(SILIN_NOx.index),
# #        len(SILIN_O3.index),len(SILIN_PM10.index),len(SILIN_SO2.index),len(SILIN_TEMP.index))
#
#
# ##大園DAYUAN
# DAYUAN_CO,DAYUAN_TEMP, DAYUAN_SO2, DAYUAN_NO, DAYUAN_NO2, DAYUAN_NOx, DAYUAN_PM10, DAYUAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年大園站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年大園站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年大園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年大園站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年大園站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年大園站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年大園站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年大園站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年大園站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年大園站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年大園站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年大園站_20170217.xls')
#
# # print(len(DAYUAN_CO.index),len(DAYUAN_NO.index),len(DAYUAN_NO2.index),len(DAYUAN_NOx.index),
# #        len(DAYUAN_O3.index),len(DAYUAN_PM10.index),len(DAYUAN_SO2.index),len(DAYUAN_TEMP.index))
DAYUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年大園站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年大園站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年大園站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年大園站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年大園站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年大園站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年大園站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年大園站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年大園站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年大園站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年大園站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年大園站_20170217.xls']
#
# ##平鎮PINZHEN
#
# PINZHEN_CO,PINZHEN_TEMP, PINZHEN_SO2, PINZHEN_NO, PINZHEN_NO2, PINZHEN_NOx, PINZHEN_PM10, PINZHEN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年平鎮站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年平鎮站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年平鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年平鎮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年平鎮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年平鎮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年平鎮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年平鎮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年平鎮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年平鎮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年平鎮站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年平鎮站_20170217.xls')
#
# # print(len(PINZHEN_CO.index),len(PINZHEN_NO.index),len(PINZHEN_NO2.index),len(PINZHEN_NOx.index),
# #        len(PINZHEN_O3.index),len(PINZHEN_PM10.index),len(PINZHEN_SO2.index),len(PINZHEN_TEMP.index))
#
PINZHEN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年平鎮站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年平鎮站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年平鎮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年平鎮站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年平鎮站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年平鎮站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年平鎮站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年平鎮站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年平鎮站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年平鎮站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年平鎮站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年平鎮站_20170217.xls']
# ##新店ZINTIEN
#
# ZINTIEN_CO,ZINTIEN_TEMP, ZINTIEN_SO2, ZINTIEN_NO, ZINTIEN_NO2, ZINTIEN_NOx, ZINTIEN_PM10, ZINTIEN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年新店站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年新店站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年新店站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年新店站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年新店站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年新店站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年新店站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年新店站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年新店站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年新店站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年新店站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年新店站_20170217.xls')
# #
# # print(len(ZINTIEN_CO.index),len(ZINTIEN_NO.index),len(ZINTIEN_NO2.index),len(ZINTIEN_NOx.index),
# #        len(ZINTIEN_O3.index),len(ZINTIEN_PM10.index),len(ZINTIEN_SO2.index),len(ZINTIEN_TEMP.index))
ZINTIEN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年新店站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年新店站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年新店站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年新店站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年新店站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年新店站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年新店站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年新店站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年新店站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年新店站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年新店站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年新店站_20170217.xls']
#
#
# ##新莊ZINCHUAN
# #
# ZINCHUAN_CO,ZINCHUAN_TEMP, ZINCHUAN_SO2, ZINCHUAN_NO, ZINCHUAN_NO2, ZINCHUAN_NOx, ZINCHUAN_PM10, ZINCHUAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年新莊站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年新莊站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年新莊站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年新莊站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年新莊站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年新莊站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年新莊站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年新莊站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年新莊站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年新莊站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年新莊站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年新莊站_20170217.xls')
ZINCHUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年新莊站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年新莊站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年新莊站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年新莊站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年新莊站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年新莊站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年新莊站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年新莊站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年新莊站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年新莊站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年新莊站_20160318.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年新莊站_20170217.xls']
# # print(len(ZINCHUAN_CO.index),len(ZINCHUAN_NO.index),len(ZINCHUAN_NO2.index),len(ZINCHUAN_NOx.index),
# #        len(ZINCHUAN_O3.index),len(ZINCHUAN_PM10.index),len(ZINCHUAN_SO2.index),len(ZINCHUAN_TEMP.index))
#
# # ##松山SONGSHAN
# SONGSHAN_CO,SONGSHAN_TEMP, SONGSHAN_SO2, SONGSHAN_NO, SONGSHAN_NO2, SONGSHAN_NOx, SONGSHAN_PM10, SONGSHAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年松山站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年松山站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年松山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年松山站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年松山站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年松山站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年松山站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年松山站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年松山站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年松山站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年松山站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年松山站_20170217.xls')
#
# # print(len(SONGSHAN_CO.index),len(SONGSHAN_NO.index),len(SONGSHAN_NO2.index),len(SONGSHAN_NOx.index),
# #        len(SONGSHAN_O3.index),len(SONGSHAN_PM10.index),len(SONGSHAN_SO2.index),len(SONGSHAN_TEMP.index))
SONGSHAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年松山站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年松山站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年松山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年松山站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年松山站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年松山站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年松山站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年松山站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年松山站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年松山站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年松山站_20160318.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年松山站_20170217.xls']
# # ##板橋BANQIAO
# BANQIAO_CO,BANQIAO_TEMP, BANQIAO_SO2, BANQIAO_NO, BANQIAO_NO2, BANQIAO_NOx, BANQIAO_PM10, BANQIAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年板橋站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年板橋站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年板橋站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年板橋站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年板橋站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年板橋站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年板橋站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年板橋站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年板橋站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年板橋站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年板橋站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年板橋站_20170217.xls')
BANQIAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年板橋站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年板橋站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年板橋站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年板橋站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年板橋站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年板橋站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年板橋站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年板橋站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年板橋站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年板橋站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年板橋站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年板橋站_20170217.xls']
# # print(len(BANQIAO_CO.index),len(BANQIAO_NO.index),len(BANQIAO_NO2.index),len(BANQIAO_NOx.index),
# #        len(BANQIAO_O3.index),len(BANQIAO_PM10.index),len(BANQIAO_SO2.index),len(BANQIAO_TEMP.index))
#
# ##林口LINKAO
#
# #
# LINKAO_CO,LINKAO_TEMP, LINKAO_SO2, LINKAO_NO, LINKAO_NO2, LINKAO_NOx, LINKAO_PM10, LINKAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年林口站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年林口站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年林口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年林口站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年林口站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年林口站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年林口站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年林口站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年林口站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年林口站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年林口站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年林口站_20170217.xls')
#
# # print(len(LINKAO_CO.index),len(LINKAO_NO.index),len(LINKAO_NO2.index),len(LINKAO_NOx.index),
# #        len(LINKAO_O3.index),len(LINKAO_PM10.index),len(LINKAO_SO2.index),len(LINKAO_TEMP.index))
LINKAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年林口站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年林口站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年林口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年林口站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年林口站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年林口站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年林口站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年林口站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年林口站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年林口站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年林口站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年林口站_20170217.xls']
# ##桃園 TAOYUAN
#
#
# TAOYUAN_CO,TAOYUAN_TEMP, TAOYUAN_SO2, TAOYUAN_NO, TAOYUAN_NO2, TAOYUAN_NOx, TAOYUAN_PM10, TAOYUAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年桃園站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年桃園站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年桃園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年桃園站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年桃園站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年桃園站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年桃園站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年桃園站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年桃園站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年桃園站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年桃園站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年桃園站_20170217.xls')
# #
# # print(len(TAOYUAN_CO.index),len(TAOYUAN_NO.index),len(TAOYUAN_NO2.index),len(TAOYUAN_NOx.index),
# #        len(TAOYUAN_O3.index),len(TAOYUAN_PM10.index),len(TAOYUAN_SO2.index),len(TAOYUAN_TEMP.index))
TAOYUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年桃園站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年桃園站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年桃園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年桃園站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年桃園站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年桃園站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年桃園站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年桃園站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年桃園站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年桃園站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年桃園站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年桃園站_20170217.xls']
# ##永和 YONHE
#
# #
# YONHE_CO,YONHE_TEMP, YONHE_SO2, YONHE_NO, YONHE_NO2, YONHE_NOx, YONHE_PM10, YONHE_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年永和站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年永和站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年永和站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年永和站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年永和站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年永和站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年永和站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年永和站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年永和站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年永和站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年永和站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年永和站_20170217.xls')
YONGHE = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年永和站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年永和站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年永和站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年永和站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年永和站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年永和站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年永和站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年永和站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年永和站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年永和站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年永和站_20160323.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年永和站_20170217.xls']
# # print(len(YONHE_CO.index),len(YONHE_NO.index),len(YONHE_NO2.index),len(YONHE_NOx.index),
# #        len(YONHE_O3.index),len(YONHE_PM10.index),len(YONHE_SO2.index),len(YONHE_TEMP.index))
#
# ##汐止SHITZI
# #
# SHITZI_CO,SHITZI_TEMP, SHITZI_SO2, SHITZI_NO, SHITZI_NO2, SHITZI_NOx, SHITZI_PM10, SHITZI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年汐止站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年汐止站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年汐止站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年汐止站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年汐止站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年汐止站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年汐止站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年汐止站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年汐止站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年汐止站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年汐止站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年汐止站_20170217.xls')
# #
# # print(len(SHITZI_CO.index),len(SHITZI_NO.index),len(SHITZI_NO2.index),len(SHITZI_NOx.index),
# #        len(SHITZI_O3.index),len(SHITZI_PM10.index),len(SHITZI_SO2.index),len(SHITZI_TEMP.index))
SHITZI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年汐止站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年汐止站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年汐止站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年汐止站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年汐止站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年汐止站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年汐止站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年汐止站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年汐止站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年汐止站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年汐止站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年汐止站_20170217.xls']
# ##淡水DANSHUI
# ## 9年沒有temp
# DANSHUI_CO,DANSHUI_TEMP, DANSHUI_SO2, DANSHUI_NO, DANSHUI_NO2, DANSHUI_NOx, DANSHUI_PM10, DANSHUI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年淡水站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年淡水站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年淡水站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年淡水站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年淡水站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年淡水站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年淡水站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年淡水站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年淡水站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年淡水站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年淡水站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年淡水站_20170217.xls')
# #
# # print(len(DANSHUI_CO.index),len(DANSHUI_NO.index),len(DANSHUI_NO2.index),len(DANSHUI_NOx.index),
# #        len(DANSHUI_O3.index),len(DANSHUI_PM10.index),len(DANSHUI_SO2.index),len(DANSHUI_TEMP.index))
DANSHUI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年淡水站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年淡水站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年淡水站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年淡水站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年淡水站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年淡水站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年淡水站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年淡水站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年淡水站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年淡水站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年淡水站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年淡水站_20170217.xls']
# ##菜寮TZIALAO
#
# #
# TZIALAO_CO,TZIALAO_TEMP, TZIALAO_SO2, TZIALAO_NO, TZIALAO_NO2, TZIALAO_NOx, TZIALAO_PM10, TZIALAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年菜寮站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年菜寮站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年菜寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年菜寮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年菜寮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年菜寮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年菜寮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年菜寮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年菜寮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年菜寮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年菜寮站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年菜寮站_20170217.xls')
#
# # print(len(TZIALAO_CO.index),len(TZIALAO_NO.index),len(TZIALAO_NO2.index),len(TZIALAO_NOx.index),
# #        len(TZIALAO_O3.index),len(TZIALAO_PM10.index),len(TZIALAO_SO2.index),len(TZIALAO_TEMP.index))
TZIALAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年菜寮站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年菜寮站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年菜寮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年菜寮站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年菜寮站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年菜寮站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年菜寮站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年菜寮站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年菜寮站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年菜寮站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年菜寮站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年菜寮站_20170217.xls']
#
# ##萬華 WANHUA
# #
# WANHUA_CO,WANHUA_TEMP, WANHUA_SO2, WANHUA_NO, WANHUA_NO2, WANHUA_NOx, WANHUA_PM10, WANHUA_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年萬華站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年萬華站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年萬華站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年萬華站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年萬華站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年萬華站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年萬華站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年萬華站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年萬華站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年萬華站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年萬華站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年萬華站_20170217.xls')
# #
# # print(len(WANHUA_CO.index),len(WANHUA_NO.index),len(WANHUA_NO2.index),len(WANHUA_NOx.index),
# #        len(WANHUA_O3.index),len(WANHUA_PM10.index),len(WANHUA_SO2.index),len(WANHUA_TEMP.index))
WANHUA = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年萬華站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年萬華站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年萬華站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年萬華站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年萬華站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年萬華站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年萬華站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年萬華站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年萬華站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年萬華站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年萬華站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年萬華站_20170217.xls']
# ##萬里 WANLI
#
# #
# WANLI_CO,WANLI_TEMP, WANLI_SO2, WANLI_NO, WANLI_NO2, WANLI_NOx, WANLI_PM10, WANLI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年萬里站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年萬里站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年萬里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年萬里站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年萬里站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年萬里站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年萬里站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年萬里站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年萬里站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年萬里站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年萬里站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年萬里站_20170217.xls')
#
# # print(len(WANLI_CO.index),len(WANLI_NO.index),len(WANLI_NO2.index),len(WANLI_NOx.index),
# #        len(WANLI_O3.index),len(WANLI_PM10.index),len(WANLI_SO2.index),len(WANLI_TEMP.index))
#
WANLI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年萬里站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年萬里站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年萬里站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年萬里站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年萬里站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年萬里站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年萬里站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年萬里站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年萬里站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年萬里站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年萬里站_20160318.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年萬里站_20170217.xls']
# ##觀音KUANIN
# KUANIN_CO,KUANIN_TEMP, KUANIN_SO2, KUANIN_NO, KUANIN_NO2, KUANIN_NOx, KUANIN_PM10, KUANIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年觀音站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年觀音站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年觀音站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年觀音站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年觀音站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年觀音站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年觀音站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年觀音站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年觀音站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年觀音站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年觀音站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年觀音站_20170217.xls')
KUANIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年觀音站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年觀音站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年觀音站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年觀音站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年觀音站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年觀音站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年觀音站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年觀音站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年觀音站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年觀音站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年觀音站_20160323.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年觀音站_20170217.xls']
# # print(len(KUANIN_CO.index),len(KUANIN_NO.index),len(KUANIN_NO2.index),len(KUANIN_NOx.index),
# #        len(KUANIN_O3.index),len(KUANIN_PM10.index),len(KUANIN_SO2.index),len(KUANIN_TEMP.index))
#
# ##陽明YANMING
# #
# YANMING_CO,YANMING_TEMP, YANMING_SO2, YANMING_NO, YANMING_NO2, YANMING_NOx, YANMING_PM10, YANMING_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年陽明站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年陽明站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年陽明站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年陽明站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年陽明站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年陽明站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年陽明站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年陽明站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年陽明站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年陽明站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年陽明站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年陽明站_20170217.xls')
# #
# # print(len(YANMING_CO.index),len(YANMING_NO.index),len(YANMING_NO2.index),len(YANMING_NOx.index),
# #        len(YANMING_O3.index),len(YANMING_PM10.index),len(YANMING_SO2.index),len(YANMING_TEMP.index))
YANMING = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年陽明站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年陽明站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年陽明站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年陽明站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年陽明站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年陽明站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年陽明站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年陽明站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年陽明站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年陽明站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年陽明站_20160323.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年陽明站_20170217.xls']
# ##龍潭 LONGTANG
# #
# LONGTANG_CO,LONGTANG_TEMP, LONGTANG_SO2, LONGTANG_NO, LONGTANG_NO2, LONGTANG_NOx, LONGTANG_PM10, LONGTANG_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年龍潭站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年龍潭站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年龍潭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年龍潭站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年龍潭站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年龍潭站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年龍潭站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年龍潭站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年龍潭站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年龍潭站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年龍潭站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年龍潭站_20170217.xls')
# #
# # print(len(LONGTANG_CO.index),len(LONGTANG_NO.index),len(LONGTANG_NO2.index),len(LONGTANG_NOx.index),
# #        len(LONGTANG_O3.index),len(LONGTANG_PM10.index),len(LONGTANG_SO2.index),len(LONGTANG_TEMP.index))
LONGTANG = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年北部空品區/89年龍潭站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年北部空品區/90年龍潭站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年北部空品區/91年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年北部空品區/92年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年北部空品區/93年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年北部空品區/94年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年北部空品區/95年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年北部空品區/96年龍潭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 北部空品區/97年龍潭站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 北部空品區/98年龍潭站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 北部空品區/99年龍潭站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 北部空品區/100年龍潭站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 北部空品區/101年龍潭站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 北部空品區/102年龍潭站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 北部空品區/103年龍潭站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 北部空品區/104年龍潭站_20160318.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 北部空品區/105年龍潭站_20170217.xls']
# #-------------------北部結束-------------------------#
# #-------------------宜蘭開始-------------------------#
#
# # ##宜蘭YILAN
# YILAN_CO,YILAN_TEMP, YILAN_SO2, YILAN_NO, YILAN_NO2, YILAN_NOx, YILAN_PM10, YILAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年宜蘭空品區/89年宜蘭站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年宜蘭空品區/90年宜蘭站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年宜蘭空品區/91年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年宜蘭空品區/92年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年宜蘭空品區/93年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年宜蘭空品區/94年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年宜蘭空品區/95年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年宜蘭空品區/96年宜蘭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 宜蘭空品區/97年宜蘭站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 宜蘭空品區/98年宜蘭站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 宜蘭空品區/99年宜蘭站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 宜蘭空品區/100年宜蘭站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 宜蘭空品區/101年宜蘭站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 宜蘭空品區/102年宜蘭站_20140416.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 宜蘭空品區/103年宜蘭站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 宜蘭空品區/104年宜蘭站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 宜蘭空品區/105年宜蘭站_20170217.xls')
# #
# # print(len(YILAN_CO.index),len(YILAN_NO.index),len(YILAN_NO2.index),len(YILAN_NOx.index),
# #        len(YILAN_O3.index),len(YILAN_PM10.index),len(YILAN_SO2.index),len(YILAN_TEMP.index))
YULAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年宜蘭空品區/89年宜蘭站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年宜蘭空品區/90年宜蘭站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年宜蘭空品區/91年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年宜蘭空品區/92年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年宜蘭空品區/93年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年宜蘭空品區/94年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年宜蘭空品區/95年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年宜蘭空品區/96年宜蘭站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 宜蘭空品區/97年宜蘭站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 宜蘭空品區/98年宜蘭站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 宜蘭空品區/99年宜蘭站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 宜蘭空品區/100年宜蘭站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 宜蘭空品區/101年宜蘭站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 宜蘭空品區/102年宜蘭站_20140416.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 宜蘭空品區/103年宜蘭站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 宜蘭空品區/104年宜蘭站_20160320.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 宜蘭空品區/105年宜蘭站_20170217.xls']
# ##冬山DONSHAN
#
# DONSHAN_CO,DONSHAN_TEMP, DONSHAN_SO2, DONSHAN_NO, DONSHAN_NO2, DONSHAN_NOx, DONSHAN_PM10, DONSHAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年宜蘭空品區/89年冬山站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年宜蘭空品區/90年冬山站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年宜蘭空品區/91年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年宜蘭空品區/92年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年宜蘭空品區/93年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年宜蘭空品區/94年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年宜蘭空品區/95年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年宜蘭空品區/96年冬山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 宜蘭空品區/97年冬山站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 宜蘭空品區/98年冬山站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 宜蘭空品區/99年冬山站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 宜蘭空品區/100年冬山站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 宜蘭空品區/101年冬山站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 宜蘭空品區/102年冬山站_20140416.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 宜蘭空品區/103年冬山站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 宜蘭空品區/104年冬山站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 宜蘭空品區/105年冬山站_20170217.xls')
#
# # print(len(DONSHAN_CO.index),len(DONSHAN_NO.index),len(DONSHAN_NO2.index),len(DONSHAN_NOx.index),
# #        len(DONSHAN_O3.index),len(DONSHAN_PM10.index),len(DONSHAN_SO2.index),len(DONSHAN_TEMP.index))
DONSHAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年宜蘭空品區/89年冬山站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年宜蘭空品區/90年冬山站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年宜蘭空品區/91年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年宜蘭空品區/92年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年宜蘭空品區/93年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年宜蘭空品區/94年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年宜蘭空品區/95年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年宜蘭空品區/96年冬山站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 宜蘭空品區/97年冬山站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 宜蘭空品區/98年冬山站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 宜蘭空品區/99年冬山站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 宜蘭空品區/100年冬山站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 宜蘭空品區/101年冬山站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 宜蘭空品區/102年冬山站_20140416.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 宜蘭空品區/103年冬山站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 宜蘭空品區/104年冬山站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 宜蘭空品區/105年冬山站_20170217.xls']
# #-------------------宜蘭結束-------------------------#
#
# #-------------------竹苗開始-------------------------#
#
# ##三義SANYI
# #
# SANYI_CO,SANYI_TEMP, SANYI_SO2, SANYI_NO, SANYI_NO2, SANYI_NOx, SANYI_PM10, SANYI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年三義站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年三義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年三義站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年三義站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年三義站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年三義站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年三義站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年三義站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年三義站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年三義站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年三義站_20170217.xls')
#
# # print(len(SANYI_CO.index),len(SANYI_NO.index),len(SANYI_NO2.index),len(SANYI_NOx.index),
# #        len(SANYI_O3.index),len(SANYI_PM10.index),len(SANYI_SO2.index),len(SANYI_TEMP.index))
SANYI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年三義站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年三義站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年三義站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年三義站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年三義站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年三義站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年三義站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年三義站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年三義站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年三義站_20160318.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年三義站_20170217.xls']
# ## 新竹 HSINCHU
# #
# HSINCHU_CO,HSINCHU_TEMP, HSINCHU_SO2, HSINCHU_NO, HSINCHU_NO2, HSINCHU_NOx, HSINCHU_PM10, HSINCHU_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年新竹站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年新竹站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年新竹站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年新竹站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年新竹站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年新竹站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年新竹站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年新竹站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年新竹站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年新竹站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年新竹站_20170217.xls')
# #
# #
HSINCHU = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年新竹站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年新竹站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年新竹站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年新竹站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年新竹站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年新竹站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年新竹站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年新竹站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年新竹站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年新竹站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年新竹站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年新竹站_20170217.xls']
# HSINCHU_TEMP = dataframemerge("AMB_TEMP",'/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年新竹站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年竹東站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年新竹站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年新竹站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年新竹站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年新竹站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年新竹站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年新竹站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年新竹站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年新竹站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年新竹站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年新竹站_20170217.xls' )
# # print(len(HSINCHU_CO.index),len(HSINCHU_NO.index),len(HSINCHU_NO2.index),len(HSINCHU_NOx.index),
# #        len(HSINCHU_O3.index),len(HSINCHU_PM10.index),len(HSINCHU_SO2.index),len(HSINCHU_TEMP.index))
HSINCHUTEMP = ['/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年竹東站_20090901.csv',
               '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年新竹站_20080801.csv',
               '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年新竹站_20090301.xls',
               '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年新竹站_20100331.csv',
               '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年新竹站_20110329.csv',
               '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年新竹站_20120409.csv',
               '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年新竹站_20130424.xls',
               '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年新竹站_20140417.xls',
               '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年新竹站_20170317.xls',
               '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年新竹站_20160318.xls',
               '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年新竹站_20170217.xls']
#
# ##湖口WHOKAO
#
# #
# WHOKAO_CO,WHOKAO_TEMP, WHOKAO_SO2, WHOKAO_NO, WHOKAO_NO2, WHOKAO_NOx, WHOKAO_PM10, WHOKAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年湖口站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年湖口站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年湖口站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年湖口站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年湖口站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年湖口站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年湖口站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年湖口站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年湖口站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年湖口站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年湖口站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年湖口站_20170217.xls')
#
# # print(len(WHOKAO_CO.index),len(WHOKAO_NO.index),len(WHOKAO_NO2.index),len(WHOKAO_NOx.index),
# #        len(WHOKAO_O3.index),len(WHOKAO_PM10.index),len(WHOKAO_SO2.index),len(WHOKAO_TEMP.index))
WHOKAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年湖口站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年湖口站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年湖口站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年湖口站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年湖口站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年湖口站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年湖口站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年湖口站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年湖口站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年湖口站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年湖口站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年湖口站_20170217.xls']
# ##竹東CHUTONG
#
# #
# CHUTONG_CO,CHUTONG_TEMP, CHUTONG_SO2, CHUTONG_NO, CHUTONG_NO2, CHUTONG_NOx, CHUTONG_PM10, CHUTONG_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年竹東站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年竹東站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年竹東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年竹東站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年竹東站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年竹東站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年竹東站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年竹東站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年竹東站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年竹東站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年竹東站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年竹東站_20170217.xls')
# #
# # print(len(CHUTONG_CO.index),len(CHUTONG_NO.index),len(CHUTONG_NO2.index),len(CHUTONG_NOx.index),
# #        len(CHUTONG_O3.index),len(CHUTONG_PM10.index),len(CHUTONG_SO2.index),len(CHUTONG_TEMP.index))
CHUTUNG = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年竹東站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年竹東站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年竹東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年竹東站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年竹東站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年竹東站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年竹東站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年竹東站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年竹東站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年竹東站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年竹東站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年竹東站_20170217.xls']
# ##苗栗 MIAOLI
#
#
# MIAOLI_CO,MIAOLI_TEMP, MIAOLI_SO2, MIAOLI_NO, MIAOLI_NO2, MIAOLI_NOx, MIAOLI_PM10, MIAOLI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年苗栗站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年苗栗站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年苗栗站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年苗栗站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年苗栗站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年苗栗站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年苗栗站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年苗栗站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年苗栗站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年苗栗站_20170217.xls')
# #
# # print(len(MIAOLI_CO.index),len(MIAOLI_NO.index),len(MIAOLI_NO2.index),len(MIAOLI_NOx.index),
# #        len(MIAOLI_O3.index),len(MIAOLI_PM10.index),len(MIAOLI_SO2.index),len(MIAOLI_TEMP.index))
MIAOLI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年苗栗站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年苗栗站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年苗栗站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年苗栗站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年苗栗站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年苗栗站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年苗栗站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年苗栗站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年苗栗站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年苗栗站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年苗栗站_20170217.xls']
# #頭份 TOFEN
#
#
# TOFEN_CO,TOFEN_TEMP, TOFEN_SO2, TOFEN_NO, TOFEN_NO2, TOFEN_NOx, TOFEN_PM10, TOFEN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年頭份站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年頭份站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年頭份站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年頭份站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年頭份站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年頭份站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年頭份站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年頭份站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年頭份站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年頭份站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年頭份站_20170217.xls')
# #
# #
TOFEN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年頭份站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年頭份站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年頭份站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年頭份站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年頭份站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年頭份站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年頭份站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年頭份站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年頭份站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年頭份站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年頭份站_20160323.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年頭份站_20170217.xls']
# TOFEN_CO = dataframemerge("CO",'/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年竹苗空品區/89年苗栗站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年苗栗站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年頭份站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年頭份站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年頭份站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年頭份站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年頭份站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年頭份站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年頭份站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年頭份站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年頭份站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年頭份站_20170217.xls')
# #

TOFENCO = ['/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年竹苗空品區/90年苗栗站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年竹苗空品區/91年苗栗站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年竹苗空品區/92年苗栗站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年竹苗空品區/93年頭份站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年竹苗空品區/94年頭份站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年竹苗空品區/95年頭份站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年竹苗空品區/96年頭份站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 竹苗空品區/97年頭份站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 竹苗空品區/98年頭份站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 竹苗空品區/99年頭份站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 竹苗空品區/100年頭份站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 竹苗空品區/101年頭份站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 竹苗空品區/102年頭份站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 竹苗空品區/103年頭份站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 竹苗空品區/104年頭份站_20160323.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 竹苗空品區/105年頭份站_20170217.xls']
# # print(len(TOFEN_CO.index),len(TOFEN_NO.index),len(TOFEN_NO2.index),len(TOFEN_NOx.index),
# #        len(TOFEN_O3.index),len(TOFEN_PM10.index),len(TOFEN_SO2.index),len(TOFEN_TEMP.index))
# #-------------------竹苗結束-------------------------#
# #-------------------花東開始-------------------------#
# ##台東TAITUNG
# #
# TAITUNG_CO,TAITUNG_TEMP, TAITUNG_SO2, TAITUNG_NO, TAITUNG_NO2, TAITUNG_NOx, TAITUNG_PM10, TAITUNG_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年花東空品區/89年台東站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年花東空品區/90年台東站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年花東空品區/91年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年花東空品區/92年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年花東空品區/93年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年花東空品區/94年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年花東空品區/95年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年花東空品區/96年台東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 花東空品區/97年台東站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 花東空品區/98年台東站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 花東空品區/99年台東站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 花東空品區/100年台東站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 花東空品區/101年台東站_20130426.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 花東空品區/102年台東站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 花東空品區/103年臺東站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 花東空品區/104年臺東站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 花東空品區/105年臺東站_20170217.xls')
#
# #
# # print(len(TAITUNG_CO.index),len(TAITUNG_NO.index),len(TAITUNG_NO2.index),len(TAITUNG_NOx.index),
# #    len(TAITUNG_O3.index),len(TAITUNG_PM10.index),len(TAITUNG_SO2.index),len(TAITUNG_TEMP.index))
#
TAITUNG = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年花東空品區/89年台東站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年花東空品區/90年台東站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年花東空品區/91年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年花東空品區/92年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年花東空品區/93年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年花東空品區/94年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年花東空品區/95年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年花東空品區/96年台東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 花東空品區/97年台東站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 花東空品區/98年台東站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 花東空品區/99年台東站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 花東空品區/100年台東站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 花東空品區/101年台東站_20130426.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 花東空品區/102年台東站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 花東空品區/103年臺東站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 花東空品區/104年臺東站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 花東空品區/105年臺東站_20170217.xls']
# ##花蓮 HUALIAN
#
# HUALIAN_CO,HUALIAN_TEMP, HUALIAN_SO2, HUALIAN_NO, HUALIAN_NO2, HUALIAN_NOx, HUALIAN_PM10, HUALIAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年花東空品區/89年花蓮站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年花東空品區/90年花蓮站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年花東空品區/91年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年花東空品區/92年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年花東空品區/93年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年花東空品區/94年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年花東空品區/95年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年花東空品區/96年花蓮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 花東空品區/97年花蓮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 花東空品區/98年花蓮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 花東空品區/99年花蓮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 花東空品區/100年花蓮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 花東空品區/101年花蓮站_20130426.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 花東空品區/102年花蓮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 花東空品區/103年花蓮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 花東空品區/104年花蓮站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 花東空品區/105年花蓮站_20170217.xls')
# #
# #
# # print(len(HUALIAN_CO.index),len(HUALIAN_NO.index),len(HUALIAN_NO2.index),len(HUALIAN_NOx.index),
# #    len(HUALIAN_O3.index),len(HUALIAN_PM10.index),len(HUALIAN_SO2.index),len(HUALIAN_TEMP.index))

HUALIAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年花東空品區/89年花蓮站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年花東空品區/90年花蓮站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年花東空品區/91年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年花東空品區/92年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年花東空品區/93年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年花東空品區/94年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年花東空品區/95年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年花東空品區/96年花蓮站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 花東空品區/97年花蓮站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 花東空品區/98年花蓮站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 花東空品區/99年花蓮站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 花東空品區/100年花蓮站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 花東空品區/101年花蓮站_20130426.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 花東空品區/102年花蓮站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 花東空品區/103年花蓮站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 花東空品區/104年花蓮站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 花東空品區/105年花蓮站_20170217.xls']
# ####關山前五年沒資料故不用
# #-------------------花東結束-------------------------#
#
# #-------------------雲嘉南開始-------------------------#
# #
# # ##台南TAINAN
# #
# TAINAN_CO,TAINAN_TEMP, TAINAN_SO2, TAINAN_NO, TAINAN_NO2, TAINAN_NOx, TAINAN_PM10, TAINAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年台南站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年台南站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年台南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年台南站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年台南站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年台南站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年台南站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年台南站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年台南站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年臺南站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年臺南站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年臺南站_20170217.xls')
#
# #
# # print(len(TAINAN_CO.index),len(TAINAN_NO.index),len(TAINAN_NO2.index),len(TAINAN_NOx.index),
# #    len(TAINAN_O3.index),len(TAINAN_PM10.index),len(TAINAN_SO2.index),len(TAINAN_TEMP.index))
TAINAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年台南站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年台南站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年台南站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年台南站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年台南站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年台南站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年台南站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年台南站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年台南站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年臺南站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年臺南站_20160320.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年臺南站_20170217.xls']
#
# ##台西TAISI
# #
# TAISI_CO,TAISI_TEMP, TAISI_SO2, TAISI_NO, TAISI_NO2, TAISI_NOx, TAISI_PM10, TAISI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年台西站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年台西站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年台西站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年台西站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年台西站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年台西站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年台西站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年台西站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年台西站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年臺西站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年臺西站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年臺西站_20170217.xls')
#
# #
# # print(len(TAISI_CO.index),len(TAISI_NO.index),len(TAISI_NO2.index),len(TAISI_NOx.index),
# #    len(TAISI_O3.index),len(TAISI_PM10.index),len(TAISI_SO2.index),len(TAISI_TEMP.index))
TAISI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年台西站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年台西站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年台西站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年台西站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年台西站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年台西站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年台西站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年台西站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年台西站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年臺西站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年臺西站_20160323.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年臺西站_20170217.xls']
#
# ##善化SHANHUA
# #
# SHANHUA_CO,SHANHUA_TEMP, SHANHUA_SO2, SHANHUA_NO, SHANHUA_NO2, SHANHUA_NOx, SHANHUA_PM10, SHANHUA_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年善化站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年善化站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年善化站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年善化站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年善化站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年善化站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年善化站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年善化站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年善化站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年善化站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年善化站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年善化站_20170217.xls')
#
# #
# # print(len(SHANHUA_CO.index),len(SHANHUA_NO.index),len(SHANHUA_NO2.index),len(SHANHUA_NOx.index),
# #    len(SHANHUA_O3.index),len(SHANHUA_PM10.index),len(SHANHUA_SO2.index),len(SHANHUA_TEMP.index))
SHANHUA = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年善化站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年善化站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年善化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年善化站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年善化站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年善化站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年善化站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年善化站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年善化站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年善化站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年善化站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年善化站_20170217.xls']
#
# ##嘉義 CHIAYI
# #
# CHIAYI_CO,CHIAYI_TEMP, CHIAYI_SO2, CHIAYI_NO, CHIAYI_NO2, CHIAYI_NOx, CHIAYI_PM10, CHIAYI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年嘉義站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年嘉義站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年嘉義站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年嘉義站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年嘉義站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年嘉義站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年嘉義站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年嘉義站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年嘉義站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年嘉義站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年嘉義站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年嘉義站_20170217.xls')
#

CHIAYI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年嘉義站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年嘉義站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年嘉義站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年嘉義站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年嘉義站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年嘉義站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年嘉義站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年嘉義站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年嘉義站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年嘉義站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年嘉義站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年嘉義站_20170217.xls']
# #
# # print(len(CHIAYI_CO.index),len(CHIAYI_NO.index),len(CHIAYI_NO2.index),len(CHIAYI_NOx.index),
# #    len(CHIAYI_O3.index),len(CHIAYI_PM10.index),len(CHIAYI_SO2.index),len(CHIAYI_TEMP.index))
# ##安南ANNAN
# ANNAN_CO,ANNAN_TEMP, ANNAN_SO2, ANNAN_NO, ANNAN_NO2, ANNAN_NOx, ANNAN_PM10, ANNAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年安南站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年安南站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年安南站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年安南站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年安南站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年安南站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年安南站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年安南站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年安南站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年安南站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年安南站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年安南站_20170217.xls')
#
#
# # print(len(ANNAN_CO.index),len(ANNAN_NO.index),len(ANNAN_NO2.index),len(ANNAN_NOx.index),
# #    len(ANNAN_O3.index),len(ANNAN_PM10.index),len(ANNAN_SO2.index),len(ANNAN_TEMP.index))
ANNAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年安南站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年安南站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年安南站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年安南站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年安南站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年安南站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年安南站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年安南站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年安南站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年安南站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年安南站_20160320.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年安南站_20170217.xls']
# ##崙背 LUNBAY
# #
# LUNBAY_CO,LUNBAY_TEMP, LUNBAY_SO2, LUNBAY_NO, LUNBAY_NO2, LUNBAY_NOx, LUNBAY_PM10, LUNBAY_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年崙背站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年崙背站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年崙背站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年崙背站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年崙背站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年崙背站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年崙背站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年崙背站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年崙背站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年崙背站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年崙背站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年崙背站_20170217.xls')
#
#
# # print(len(LUNBAY_CO.index),len(LUNBAY_NO.index),len(LUNBAY_NO2.index),len(LUNBAY_NOx.index),
# #    len(LUNBAY_O3.index),len(LUNBAY_PM10.index),len(LUNBAY_SO2.index),len(LUNBAY_TEMP.index))
LUNBAY = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年崙背站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年崙背站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年崙背站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年崙背站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年崙背站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年崙背站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年崙背站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年崙背站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年崙背站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年崙背站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年崙背站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年崙背站_20170217.xls']
#
# ##斗六 DOLIAO
# #
# DOLIAO_CO,DOLIAO_TEMP, DOLIAO_SO2, DOLIAO_NO, DOLIAO_NO2, DOLIAO_NOx, DOLIAO_PM10, DOLIAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年斗六站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年斗六站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年斗六站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年斗六站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年斗六站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年斗六站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年斗六站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年斗六站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年斗六站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年斗六站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年斗六站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年斗六站_20170217.xls')
#
# #
# # print(len(DOLIAO_CO.index),len(DOLIAO_NO.index),len(DOLIAO_NO2.index),len(DOLIAO_NOx.index),
# #    len(DOLIAO_O3.index),len(DOLIAO_PM10.index),len(DOLIAO_SO2.index),len(DOLIAO_TEMP.index))
DOLIAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年斗六站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年斗六站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年斗六站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年斗六站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年斗六站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年斗六站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年斗六站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年斗六站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年斗六站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年斗六站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年斗六站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年斗六站_20170217.xls']
# ##新港 HSINKAN
#
# #
# HSINKAN_CO,HSINKAN_TEMP, HSINKAN_SO2, HSINKAN_NO, HSINKAN_NO2, HSINKAN_NOx, HSINKAN_PM10, HSINKAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年新港站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年新港站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年新港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年新港站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年新港站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年新港站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年新港站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年新港站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年新港站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年新港站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年新港站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年新港站_20170217.xls')
# #
# #
# # print(len(HSINKAN_CO.index),len(HSINKAN_NO.index),len(HSINKAN_NO2.index),len(HSINKAN_NOx.index),
# #    len(HSINKAN_O3.index),len(HSINKAN_PM10.index),len(HSINKAN_SO2.index),len(HSINKAN_TEMP.index))
HSINKAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年新港站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年新港站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年新港站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年新港站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年新港站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年新港站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年新港站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年新港站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年新港站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年新港站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年新港站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年新港站_20170217.xls']
# ##新營HSINYIN
# #
# HSINYIN_CO,HSINYIN_TEMP, HSINYIN_SO2, HSINYIN_NO, HSINYIN_NO2, HSINYIN_NOx, HSINYIN_PM10, HSINYIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年新營站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年新營站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年新營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年新營站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年新營站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年新營站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年新營站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年新營站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年新營站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年新營站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年新營站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年新營站_20170217.xls')
#
HSINYIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年新營站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年新營站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年新營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年新營站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年新營站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年新營站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年新營站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年新營站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年新營站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年新營站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年新營站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年新營站_20170217.xls']
# # print(len(HSINYIN_CO.index),len(HSINYIN_NO.index),len(HSINYIN_NO2.index),len(HSINYIN_NOx.index),
# #    len(HSINYIN_O3.index),len(HSINYIN_PM10.index),len(HSINYIN_SO2.index),len(HSINYIN_TEMP.index))
#
# ##朴子 POOTZI
# #
# POOTZI_CO,POOTZI_TEMP, POOTZI_SO2, POOTZI_NO, POOTZI_NO2, POOTZI_NOx, POOTZI_PM10, POOTZI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年朴子站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年朴子站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年朴子站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年朴子站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年朴子站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年朴子站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年朴子站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年朴子站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年朴子站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年朴子站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年朴子站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年朴子站_20170217.xls')
POOZI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年雲嘉南空品區/89年朴子站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年雲嘉南空品區/90年朴子站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年雲嘉南空品區/91年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年雲嘉南空品區/92年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年雲嘉南空品區/93年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年雲嘉南空品區/94年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年雲嘉南空品區/95年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年雲嘉南空品區/96年朴子站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 雲嘉南空品區/97年朴子站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 雲嘉南空品區/98年朴子站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 雲嘉南空品區/99年朴子站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 雲嘉南空品區/100年朴子站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 雲嘉南空品區/101年朴子站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 雲嘉南空品區/102年朴子站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 雲嘉南空品區/103年朴子站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 雲嘉南空品區/104年朴子站_20160318.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 雲嘉南空品區/105年朴子站_20170217.xls']
# #
# # print(len(POOTZI_CO.index),len(POOTZI_NO.index),len(POOTZI_NO2.index),len(POOTZI_NOx.index),
# #    len(POOTZI_O3.index),len(POOTZI_PM10.index),len(POOTZI_SO2.index),len(POOTZI_TEMP.index))
#
# #-------------------雲嘉南結束-------------------------#
# #-------------------高屏開始---------------------------#
#
#
# ##仁武 RENWOO
# #
# RENWOO_CO,RENWOO_TEMP, RENWOO_SO2, RENWOO_NO, RENWOO_NO2, RENWOO_NOx, RENWOO_PM10, RENWOO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年仁武站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年仁武站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年仁武站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年仁武站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年仁武站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年仁武站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年仁武站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年仁武站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年仁武站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年仁武站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年仁武站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年仁武站_20170217.xls')
#
# #
# # print(len(RENWOO_CO.index),len(RENWOO_NO.index),len(RENWOO_NO2.index),len(RENWOO_NOx.index),
# #    len(RENWOO_O3.index),len(RENWOO_PM10.index),len(RENWOO_SO2.index),len(RENWOO_TEMP.index))
#
RENWOO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年仁武站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年仁武站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年仁武站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年仁武站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年仁武站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年仁武站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年仁武站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年仁武站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年仁武站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年仁武站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年仁武站_20160320.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年仁武站_20170217.xls']
# ##前金CHIENKIN
# #
# CHIENKIN_CO,CHIENKIN_TEMP, CHIENKIN_SO2, CHIENKIN_NO, CHIENKIN_NO2, CHIENKIN_NOx, CHIENKIN_PM10, CHIENKIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前金站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前金站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前金站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前金站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前金站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前金站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前金站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前金站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前金站_20170217.xls')
# #
# #
# # print(len(CHIENKIN_CO.index),len(CHIENKIN_NO.index),len(CHIENKIN_NO2.index),len(CHIENKIN_NOx.index),
# #    len(CHIENKIN_O3.index),len(CHIENKIN_PM10.index),len(CHIENKIN_SO2.index),len(CHIENKIN_TEMP.index))
CHIENKIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前金站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前金站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前金站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前金站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前金站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前金站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前金站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前金站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前金站_20160320.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前金站_20170217.xls']
#
# ## 前鎮 CHIENZEN
#
# #
# CHIENZEN_CO,CHIENZEN_TEMP, CHIENZEN_SO2, CHIENZEN_NO, CHIENZEN_NO2, CHIENZEN_NOx, CHIENZEN_PM10, CHIENZEN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前鎮站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前鎮站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls')
CHIENZEN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前鎮站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前鎮站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls']
# CHIENZEN_CO = dataframemerge("CO",
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls'
#                              )
CHIENZENCO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
              '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
              '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
              '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
              '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
              '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
              '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
              '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
              '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
              '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
              '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls']
# CHIENZEN_O3 = dataframemerge("O3",
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls'
#                              )
CHIENZENO3 = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年前金站_20081006.csv',
              '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年前金站_20090901.csv',
              '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年前金站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年前金站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年前鎮站_20080801.csv',
              '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年前鎮站_20090301.xls',
              '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年前鎮站_20100331.csv',
              '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年前鎮站_20110329.csv',
              '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年前鎮站_20120409.csv',
              '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年前鎮站_20130424.xls',
              '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年前鎮站_20140417.xls',
              '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年前鎮站_20170317.xls',
              '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年前鎮站_20160323.xls',
              '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年前鎮站_20170217.xls']
# #
# # print(len(CHIENZEN_CO.index),len(CHIENZEN_NO.index),len(CHIENZEN_NO2.index),len(CHIENZEN_NOx.index),
# #    len(CHIENZEN_O3.index),len(CHIENZEN_PM10.index),len(CHIENZEN_SO2.index),len(CHIENZEN_TEMP.index))
#
#
# # ##大寮 DALIAO
# #
# DALIAO_CO, DALIAO_TEMP, DALIAO_SO2, DALIAO_NO, DALIAO_NO2, DALIAO_NOx, DALIAO_PM10, DALIAO_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年大寮站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年大寮站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年大寮站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年大寮站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年大寮站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年大寮站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年大寮站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年大寮站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年大寮站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年大寮站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年大寮站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年大寮站_20170217.xls')
#
DALIAO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年大寮站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年大寮站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年大寮站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年大寮站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年大寮站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年大寮站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年大寮站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年大寮站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年大寮站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年大寮站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年大寮站_20160320.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年大寮站_20170217.xls']
# #
# # print(len(DALIAO_CO.index),len(DALIAO_NO.index),len(DALIAO_NO2.index),len(DALIAO_NOx.index),
# #    len(DALIAO_O3.index),len(DALIAO_PM10.index),len(DALIAO_SO2.index),len(DALIAO_TEMP.index))
#
# #小港 HSIAOKAN
#
# HSIAOKAN_CO, HSIAOKAN_TEMP, HSIAOKAN_SO2, HSIAOKAN_NO, HSIAOKAN_NO2, HSIAOKAN_NOx, HSIAOKAN_PM10, HSIAOKAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年小港站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年小港站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年小港站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年小港站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年小港站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年小港站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年小港站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年小港站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年小港站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年小港站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年小港站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年小港站_20170217.xls')
#
#
# # print(len(HSIAOKAN_CO.index),len(HSIAOKAN_NO.index),len(HSIAOKAN_NO2.index),len(HSIAOKAN_NOx.index),
# #    len(HSIAOKAN_O3.index),len(HSIAOKAN_PM10.index),len(HSIAOKAN_SO2.index),len(HSIAOKAN_TEMP.index))
HSIAOKAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年小港站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年小港站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年小港站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年小港站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年小港站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年小港站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年小港站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年小港站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年小港站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年小港站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年小港站_20160320.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年小港站_20170217.xls']
#
# ## 屏東 PINTUNG
#
# PINTUNG_CO, PINTUNG_TEMP, PINTUNG_SO2, PINTUNG_NO, PINTUNG_NO2, PINTUNG_NOx, PINTUNG_PM10, PINTUNG_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年屏東站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年屏東站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年屏東站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年屏東站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年屏東站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年屏東站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年屏東站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年屏東站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年屏東站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年屏東站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年屏東站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年屏東站_20170217.xls')
#
# #
# # print(len(PINTUNG_CO.index),len(PINTUNG_NO.index),len(PINTUNG_NO2.index),len(PINTUNG_NOx.index),
# #    len(PINTUNG_O3.index),len(PINTUNG_PM10.index),len(PINTUNG_SO2.index),len(PINTUNG_TEMP.index))
PINTUNG = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年屏東站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年屏東站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年屏東站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年屏東站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年屏東站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年屏東站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年屏東站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年屏東站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年屏東站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年屏東站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年屏東站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年屏東站_20170217.xls']
# ##左營 TZUOYIN
# #
# TZUOYIN_CO, TZUOYIN_TEMP, TZUOYIN_SO2, TZUOYIN_NO, TZUOYIN_NO2, TZUOYIN_NOx, TZUOYIN_PM10, TZUOYIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年左營站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年左營站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年左營站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年左營站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年左營站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年左營站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年左營站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年左營站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年左營站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年左營站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年左營站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年左營站_20170217.xls')
#
#
# # print(len(TZUOYIN_CO.index),len(TZUOYIN_NO.index),len(TZUOYIN_NO2.index),len(TZUOYIN_NOx.index),
# #    len(TZUOYIN_O3.index),len(TZUOYIN_PM10.index),len(TZUOYIN_SO2.index),len(TZUOYIN_TEMP.index))
TZUOYIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年左營站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年左營站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年左營站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年左營站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年左營站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年左營站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年左營站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年左營站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年左營站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年左營站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年左營站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年左營站_20170217.xls']
# ##復興 FUZIN
# #
# FUZIN_CO, FUZIN_TEMP, FUZIN_SO2, FUZIN_NO, FUZIN_NO2, FUZIN_NOx, FUZIN_PM10, FUZIN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年復興站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年復興站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年復興站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年復興站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年復興站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年復興站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年復興站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年復興站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年復興站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年復興站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年復興站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年復興站_20170217.xls')
#
FUZIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年復興站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年復興站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年復興站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年復興站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年復興站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年復興站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年復興站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年復興站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年復興站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年復興站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年復興站_20160323.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年復興站_20170217.xls']
# #
# # print(len(FUZIN_CO.index),len(FUZIN_NO.index),len(FUZIN_NO2.index),len(FUZIN_NOx.index),
# #    len(FUZIN_O3.index),len(FUZIN_PM10.index),len(FUZIN_SO2.index),len(FUZIN_TEMP.index))
#
# ##恆春 HENTZUAN
#
# HENTZUAN_CO, HENTZUAN_TEMP, HENTZUAN_SO2, HENTZUAN_NO, HENTZUAN_NO2, HENTZUAN_NOx, HENTZUAN_PM10, HENTZUAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年恆春站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年恆春站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年恆春站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年恆春站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年恆春站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年恆春站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年恆春站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年恆春站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年恆春站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年恆春站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年恆春站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年恆春站_20170217.xls')
#
# #
# # print(len(HENTZUAN_CO.index),len(HENTZUAN_NO.index),len(HENTZUAN_NO2.index),len(HENTZUAN_NOx.index),
# #    len(HENTZUAN_O3.index),len(HENTZUAN_PM10.index),len(HENTZUAN_SO2.index),len(HENTZUAN_TEMP.index))
#
HENZUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年恆春站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年恆春站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年恆春站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年恆春站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年恆春站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年恆春站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年恆春站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年恆春站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年恆春站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年恆春站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年恆春站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年恆春站_20170217.xls']
# # ##林園 LINYUAN
# LINYUAN_CO, LINYUAN_TEMP, LINYUAN_SO2, LINYUAN_NO, LINYUAN_NO2, LINYUAN_NOx, LINYUAN_PM10, LINYUAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年林園站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年林園站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年林園站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年林園站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年林園站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年林園站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年林園站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年林園站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年林園站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年林園站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年林園站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年林園站_20170217.xls')
#
# #
# # print(len(LINYUAN_CO.index),len(LINYUAN_NO.index),len(LINYUAN_NO2.index),len(LINYUAN_NOx.index),
# #    len(LINYUAN_O3.index),len(LINYUAN_PM10.index),len(LINYUAN_SO2.index),len(LINYUAN_TEMP.index))
LINYUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年林園站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年林園站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年林園站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年林園站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年林園站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年林園站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年林園站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年林園站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年林園站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年林園站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年林園站_20160320.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年林園站_20170217.xls']
# ##楠梓 NANTZI
# #
# NANTZI_CO, NANTZI_TEMP, NANTZI_SO2, NANTZI_NO, NANTZI_NO2, NANTZI_NOx, NANTZI_PM10, NANTZI_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年楠梓站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年楠梓站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年楠梓站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年楠梓站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年楠梓站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年楠梓站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年楠梓站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年楠梓站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年楠梓站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年楠梓站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年楠梓站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年楠梓站_20170217.xls')
#
# #
# # print(len(NANTZI_CO.index),len(NANTZI_NO.index),len(NANTZI_NO2.index),len(NANTZI_NOx.index),
# #    len(NANTZI_O3.index),len(NANTZI_PM10.index),len(NANTZI_SO2.index),len(NANTZI_TEMP.index))
NANTZI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年楠梓站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年楠梓站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年楠梓站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年楠梓站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年楠梓站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年楠梓站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年楠梓站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年楠梓站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年楠梓站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年楠梓站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年楠梓站_20160320.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年楠梓站_20170217.xls']
# ## 橋頭 CIAOTOU
# #
# #
# CIAOTOU_CO, CIAOTOU_TEMP, CIAOTOU_SO2, CIAOTOU_NO, CIAOTOU_NO2, CIAOTOU_NOx, CIAOTOU_PM10, CIAOTOU_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年橋頭站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年橋頭站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年橋頭站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年橋頭站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年橋頭站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年橋頭站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年橋頭站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年橋頭站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年橋頭站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年橋頭站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年橋頭站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年橋頭站_20170217.xls')
#
#
# # print(len(CIAOTOU_CO.index),len(CIAOTOU_NO.index),len(CIAOTOU_NO2.index),len(CIAOTOU_NOx.index),
# #    len(CIAOTOU_O3.index),len(CIAOTOU_PM10.index),len(CIAOTOU_SO2.index),len(CIAOTOU_TEMP.index))
CHIAOTOU = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年橋頭站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年橋頭站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年橋頭站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年橋頭站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年橋頭站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年橋頭站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年橋頭站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年橋頭站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年橋頭站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年橋頭站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年橋頭站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年橋頭站_20170217.xls']
# ##潮州CHIAOCHOU
#
# #
# CHIAOCHOU_CO, CHIAOCHOU_TEMP, CHIAOCHOU_SO2, CHIAOCHOU_NO, CHIAOCHOU_NO2, CHIAOCHOU_NOx, CHIAOCHOU_PM10, CHIAOCHOU_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年潮州站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年潮州站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年潮州站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年潮州站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年潮州站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年潮州站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年潮州站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年潮州站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年潮州站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年潮州站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年潮州站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年潮州站_20170217.xls')
CHIAOCHOU = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年潮州站_20081006.csv',
             '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年潮州站_20090901.csv',
             '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年潮州站_20080801.csv',
             '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年潮州站_20090301.xls',
             '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年潮州站_20100331.csv',
             '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年潮州站_20110329.csv',
             '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年潮州站_20120409.csv',
             '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年潮州站_20130424.xls',
             '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年潮州站_20140417.xls',
             '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年潮州站_20170317.xls',
             '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年潮州站_20160320.xls',
             '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年潮州站_20170217.xls']
# #
# # print(len(CHIAOCHOU_CO.index),len(CHIAOCHOU_NO.index),len(CHIAOCHOU_NO2.index),len(CHIAOCHOU_NOx.index),
# #    len(CHIAOCHOU_O3.index),len(CHIAOCHOU_PM10.index),len(CHIAOCHOU_SO2.index),len(CHIAOCHOU_TEMP.index))
#
# ##美濃 MEINON
#
#
# #
# MEINON_CO, MEINON_TEMP, MEINON_SO2, MEINON_NO, MEINON_NO2, MEINON_NOx, MEINON_PM10, MEINON_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年美濃站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年美濃站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年美濃站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年美濃站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年美濃站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年美濃站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年美濃站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年美濃站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年美濃站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年美濃站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年美濃站_20160320.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年美濃站_20170217.xls')
MEINON = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年美濃站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年美濃站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年美濃站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年美濃站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年美濃站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年美濃站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年美濃站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年美濃站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年美濃站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年美濃站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年美濃站_20160320.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年美濃站_20170217.xls']
# #
# # print(len(MEINON_CO.index),len(MEINON_NO.index),len(MEINON_NO2.index),len(MEINON_NOx.index),
# #    len(MEINON_O3.index),len(MEINON_PM10.index),len(MEINON_SO2.index),len(MEINON_TEMP.index))
#
# ##鳳山 FENGSHAN
#
#
# FENGSHAN_CO, FENGSHAN_TEMP, FENGSHAN_SO2, FENGSHAN_NO, FENGSHAN_NO2, FENGSHAN_NOx, FENGSHAN_PM10, FENGSHAN_O3 = alldataprepare(
#                           '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年鳳山站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年鳳山站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年鳳山站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年鳳山站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年鳳山站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年鳳山站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年鳳山站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年鳳山站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年鳳山站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年鳳山站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年鳳山站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年鳳山站_20170217.xls')
FENGSHAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年高屏空品區/89年鳳山站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年高屏空品區/90年鳳山站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年高屏空品區/91年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年高屏空品區/92年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年高屏空品區/93年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年高屏空品區/94年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年高屏空品區/95年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年高屏空品區/96年鳳山站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 高屏空品區/97年鳳山站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 高屏空品區/98年鳳山站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 高屏空品區/99年鳳山站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 高屏空品區/100年鳳山站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 高屏空品區/101年鳳山站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 高屏空品區/102年鳳山站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 高屏空品區/103年鳳山站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 高屏空品區/104年鳳山站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 高屏空品區/105年鳳山站_20170217.xls']
# #
# # print(len(FENGSHAN_CO.index),len(FENGSHAN_NO.index),len(FENGSHAN_NO2.index),len(FENGSHAN_NOx.index),
# #    len(FENGSHAN_O3.index),len(FENGSHAN_PM10.index),len(FENGSHAN_SO2.index),len(FENGSHAN_TEMP.index))
# #-------------------高屏結束---------------------------#
# #-------------------中部開始---------------------------#
# ## 二林ERLIN
# ERLIN_CO, ERLIN_TEMP, ERLIN_SO2, ERLIN_NO, ERLIN_NO2, ERLIN_NOx, ERLIN_PM10, ERLIN_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年二林站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年二林站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年二林站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年二林站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年二林站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年二林站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年二林站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年二林站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年二林站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年二林站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年二林站_20160318.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年二林站_20170217.xls')
# #
# # print(len(ERLIN_CO.index),len(ERLIN_NO.index),len(ERLIN_NO2.index),len(ERLIN_NOx.index),
# #    len(ERLIN_O3.index),len(ERLIN_PM10.index),len(ERLIN_SO2.index),len(ERLIN_TEMP.index))
ERLIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年二林站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年二林站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年二林站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年二林站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年二林站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年二林站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年二林站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年二林站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年二林站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年二林站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年二林站_20160318.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年二林站_20170217.xls']
# ## 南投 NANTOU
# #
# NANTOU_CO, NANTOU_TEMP, NANTOU_SO2, NANTOU_NO, NANTOU_NO2, NANTOU_NOx, NANTOU_PM10, NANTOU_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年南投站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年南投站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年南投站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年南投站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年南投站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年南投站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年南投站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年南投站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年南投站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年南投站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年南投站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年南投站_20170217.xls')
# #
# # print(len(NANTOU_CO.index),len(NANTOU_NO.index),len(NANTOU_NO2.index),len(NANTOU_NOx.index),
# #    len(NANTOU_O3.index),len(NANTOU_PM10.index),len(NANTOU_SO2.index),len(NANTOU_TEMP.index))
# #
NANTOU = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年南投站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年南投站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年南投站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年南投站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年南投站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年南投站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年南投站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年南投站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年南投站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年南投站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年南投站_20160318.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年南投站_20170217.xls']
# # ##埔里 POOLEE
# #
# POOLEE_CO, POOLEE_TEMP, POOLEE_SO2, POOLEE_NO, POOLEE_NO2, POOLEE_NOx, POOLEE_PM10, POOLEE_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年埔里站_20081006.csv',
#                           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年埔里站_20090901.csv',
#                           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年埔里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年埔里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年埔里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年大里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年埔里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年埔里站_20080801.csv',
#                           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年埔里站_20090301.xls',
#                           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年埔里站_20100331.csv',
#                           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年埔里站_20110329.csv',
#                           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年埔里站_20120409.csv',
#                           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年埔里站_20130424.xls',
#                           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年埔里站_20140417.xls',
#                           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年埔里站_20170317.xls',
#                           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年埔里站_20160323.xls',
#                           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年埔里站_20170217.xls')
# #
# # print(len(POOLEE_CO.index),len(POOLEE_NO.index),len(POOLEE_NO2.index),len(POOLEE_NOx.index),
# #    len(POOLEE_O3.index),len(POOLEE_PM10.index),len(POOLEE_SO2.index),len(POOLEE_TEMP.index))
POOLEE = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年埔里站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年埔里站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年埔里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年埔里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年埔里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年大里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年埔里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年埔里站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年埔里站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年埔里站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年埔里站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年埔里站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年埔里站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年埔里站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年埔里站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年埔里站_20160323.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年埔里站_20170217.xls']
# ##大里 DALI
#
#
# DALI_CO, DALI_TEMP, DALI_SO2, DALI_NO, DALI_NO2, DALI_NOx, DALI_PM10, DALI_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年大里站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年大里站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年大里站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年大里站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年大里站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年大里站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年大里站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年大里站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年大里站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年大里站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年大里站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年大里站_20170217.xls')

DALI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年大里站_20081006.csv',
        '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年大里站_20090901.csv',
        '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年大里站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年大里站_20090301.xls',
        '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年大里站_20100331.csv',
        '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年大里站_20110329.csv',
        '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年大里站_20120409.csv',
        '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年大里站_20130424.xls',
        '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年大里站_20140417.xls',
        '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年大里站_20170317.xls',
        '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年大里站_20160318.xls',
        '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年大里站_20170217.xls']
# # print(len(DALI_CO.index),len(DALI_NO.index),len(DALI_NO2.index),len(DALI_NOx.index),
# #    len(DALI_O3.index),len(DALI_PM10.index),len(DALI_SO2.index),len(DALI_TEMP.index))
# ##彰化  CHANHUA
# #
# CHANHUA_CO, CHANHUA_TEMP, CHANHUA_SO2, CHANHUA_NO, CHANHUA_NO2, CHANHUA_NOx, CHANHUA_PM10, CHANHUA_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年彰化站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年彰化站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年彰化站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年彰化站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年彰化站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年彰化站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年彰化站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年彰化站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年彰化站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年彰化站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年彰化站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年彰化站_20170217.xls')
#
# # print(len(CHANHUA_CO.index),len(CHANHUA_NO.index),len(CHANHUA_NO2.index),len(CHANHUA_NOx.index),
# #    len(CHANHUA_O3.index),len(CHANHUA_PM10.index),len(CHANHUA_SO2.index),len(CHANHUA_TEMP.index))
CHANHUA = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年彰化站_20081006.csv',
           '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年彰化站_20090901.csv',
           '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年彰化站_20080801.csv',
           '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年彰化站_20090301.xls',
           '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年彰化站_20100331.csv',
           '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年彰化站_20110329.csv',
           '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年彰化站_20120409.csv',
           '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年彰化站_20130424.xls',
           '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年彰化站_20140417.xls',
           '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年彰化站_20170317.xls',
           '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年彰化站_20160318.xls',
           '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年彰化站_20170217.xls']
# ## 忠明 CHONGMIN
#
# #
# CHONGMIN_CO, CHONGMIN_TEMP, CHONGMIN_SO2, CHONGMIN_NO, CHONGMIN_NO2, CHONGMIN_NOx, CHONGMIN_PM10, CHONGMIN_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年忠明站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年忠明站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年忠明站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年忠明站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年忠明站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年忠明站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年忠明站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年忠明站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年忠明站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年忠明站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年忠明站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年忠明站_20170217.xls')
#
# # print(len(CHONGMIN_CO.index),len(CHONGMIN_NO.index),len(CHONGMIN_NO2.index),len(CHONGMIN_NOx.index),
# #    len(CHONGMIN_O3.index),len(CHONGMIN_PM10.index),len(CHONGMIN_SO2.index),len(CHONGMIN_TEMP.index))
CHONGMIN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年忠明站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年忠明站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年忠明站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年忠明站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年忠明站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年忠明站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年忠明站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年忠明站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年忠明站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年忠明站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年忠明站_20160318.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年忠明站_20170217.xls']
# ##沙鹿SALU
#
# #
# SALU_CO, SALU_TEMP, SALU_SO2, SALU_NO, SALU_NO2, SALU_NOx, SALU_PM10, SALU_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年沙鹿站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年沙鹿站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年沙鹿站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年沙鹿站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年沙鹿站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年沙鹿站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年沙鹿站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年沙鹿站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年沙鹿站_20170217.xls')
# #
# # print(len(SALU_CO.index),len(SALU_NO.index),len(SALU_NO2.index),len(SALU_NOx.index),
# #    len(SALU_O3.index),len(SALU_PM10.index),len(SALU_SO2.index),len(SALU_TEMP.index))
SALU = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
        '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
        '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年沙鹿站_20080801.csv',
        '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年沙鹿站_20090301.xls',
        '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年沙鹿站_20100331.csv',
        '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年沙鹿站_20110329.csv',
        '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年沙鹿站_20120409.csv',
        '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年沙鹿站_20130424.xls',
        '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年沙鹿站_20140417.xls',
        '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年沙鹿站_20170317.xls',
        '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年沙鹿站_20160318.xls',
        '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年沙鹿站_20170217.xls']
# ##竹山 CHUSAN
# #
# #
# CHUSAN_CO, CHUSAN_TEMP, CHUSAN_SO2, CHUSAN_NO, CHUSAN_NO2, CHUSAN_NOx, CHUSAN_PM10, CHUSAN_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年竹山站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年竹山站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年竹山站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年竹山站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年竹山站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年竹山站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年竹山站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年竹山站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年竹山站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年竹山站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年竹山站_20160323.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年竹山站_20170217.xls')
# #
# # print(len(CHUSAN_CO.index),len(CHUSAN_NO.index),len(CHUSAN_NO2.index),len(CHUSAN_NOx.index),
# #    len(CHUSAN_O3.index),len(CHUSAN_PM10.index),len(CHUSAN_SO2.index),len(CHUSAN_TEMP.index))
CHUSAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年竹山站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年竹山站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年竹山站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年竹山站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年竹山站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年竹山站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年竹山站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年竹山站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年竹山站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年竹山站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年竹山站_20160323.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年竹山站_20170217.xls']
# ##線西 SHANSI
#
# #
# SHANSI_CO, SHANSI_TEMP, SHANSI_SO2, SHANSI_NO, SHANSI_NO2, SHANSI_NOx, SHANSI_PM10, SHANSI_O3 = alldataprepare(
#                            '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年線西站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年線西站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls')
SHANSI = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年線西站_20081006.csv',
          '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年線西站_20090901.csv',
          '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
          '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
          '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
          '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
          '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
          '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
          '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
          '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
          '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
          '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls']
# SHANSI_CO = dataframemerge("CO",
#                            '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls'
#                            )
SHANSICO = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls']
# SHANSI_O3 = dataframemerge("O3",
#                            '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls'
#                            )
SHANSIO3 = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年沙鹿站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年沙鹿站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年沙鹿站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年沙鹿站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年線西站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年線西站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年線西站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年線西站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年線西站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年線西站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年線西站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年線西站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年線西站_20160323.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年線西站_20170217.xls']
# # print(len(SHANSI_CO.index),len(SHANSI_NO.index),len(SHANSI_NO2.index),len(SHANSI_NOx.index),
# #    len(SHANSI_O3.index),len(SHANSI_PM10.index),len(SHANSI_SO2.index),len(SHANSI_TEMP.index))
# # ##西屯 SITUN
# SITUN_CO, SITUN_TEMP, SITUN_SO2, SITUN_NO, SITUN_NO2, SITUN_NOx, SITUN_PM10, SITUN_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年西屯站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年西屯站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年西屯站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年西屯站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年西屯站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年西屯站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年西屯站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年西屯站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年西屯站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年西屯站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年西屯站_20160323.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年西屯站_20170217.xls')
# #
# # print(len(SITUN_CO.index),len(SITUN_NO.index),len(SITUN_NO2.index),len(SITUN_NOx.index),
# #    len(SITUN_O3.index),len(SITUN_PM10.index),len(SITUN_SO2.index),len(SITUN_TEMP.index))
SITUN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年西屯站_20081006.csv',
         '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年西屯站_20090901.csv',
         '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年西屯站_20080801.csv',
         '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年西屯站_20090301.xls',
         '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年西屯站_20100331.csv',
         '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年西屯站_20110329.csv',
         '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年西屯站_20120409.csv',
         '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年西屯站_20130424.xls',
         '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年西屯站_20140417.xls',
         '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年西屯站_20170317.xls',
         '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年西屯站_20160323.xls',
         '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年西屯站_20170217.xls']
# ##豐原 FENGYUAN
#
# FENGYUAN_CO, FENGYUAN_TEMP, FENGYUAN_SO2, FENGYUAN_NO, FENGYUAN_NO2, FENGYUAN_NOx, FENGYUAN_PM10, FENGYUAN_O3 = alldataprepare(
#                             '/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年豐原站_20081006.csv',
#                            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年豐原站_20090901.csv',
#                            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年豐原站_20080801.csv',
#                            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年豐原站_20090301.xls',
#                            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年豐原站_20100331.csv',
#                            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年豐原站_20110329.csv',
#                            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年豐原站_20120409.csv',
#                            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年豐原站_20130424.xls',
#                            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年豐原站_20140417.xls',
#                            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年豐原站_20170317.xls',
#                            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年豐原站_20160318.xls',
#                            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年豐原站_20170217.xls')
# #

FENGYUAN = ['/Users/candacechou/Desktop/Airquality/89_HOUR_00_20130219/89年中部空品區/89年豐原站_20081006.csv',
            '/Users/candacechou/Desktop/Airquality/90_HOUR_00_20130219/90年中部空品區/90年豐原站_20090901.csv',
            '/Users/candacechou/Desktop/Airquality/91_HOUR_00_20130219/91年中部空品區/91年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/92_HOUR_00_20130219/92年中部空品區/92年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/93_HOUR_00_20130219/93年中部空品區/93年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/94_HOUR_00_20130219/94年中部空品區/94年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/95_HOUR_00_20081120/95年中部空品區/95年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/96_HOUR_00_20130219/96年中部空品區/96年豐原站_20080801.csv',
            '/Users/candacechou/Desktop/Airquality/097_HOUR_00_20160225/97年 中部空品區/97年豐原站_20090301.xls',
            '/Users/candacechou/Desktop/Airquality/98_HOUR_00_20130219/98年 中部空品區/98年豐原站_20100331.csv',
            '/Users/candacechou/Desktop/Airquality/99_HOUR_00_20130219/99年 中部空品區/99年豐原站_20110329.csv',
            '/Users/candacechou/Desktop/Airquality/100_HOUR_00_20120409/100年 中部空品區/100年豐原站_20120409.csv',
            '/Users/candacechou/Desktop/Airquality/101_HOUR_00_20160225/101年 中部空品區/101年豐原站_20130424.xls',
            '/Users/candacechou/Desktop/Airquality/102_HOUR_00_20160225/102年 中部空品區/102年豐原站_20140417.xls',
            '/Users/candacechou/Desktop/Airquality/103_HOUR_00_20170317/103年 中部空品區/103年豐原站_20170317.xls',
            '/Users/candacechou/Desktop/Airquality/104_HOUR_00_20160323/104年 中部空品區/104年豐原站_20160318.xls',
            '/Users/candacechou/Desktop/Airquality/105_HOUR_00_20170301/105年 中部空品區/105年豐原站_20170217.xls']
# # print(len(FENGYUAN_CO.index),len(FENGYUAN_NO.index),len(FENGYUAN_NO2.index),len(FENGYUAN_NOx.index),
# #    len(FENGYUAN_O3.index),len(FENGYUAN_PM10.index),len(FENGYUAN_SO2.index),len(FENGYUAN_TEMP.index))
# #-------------------中部結束---------------------------#
#
# ###   SHANCHUN HAS NO WIND DATA
# ### 2016 shanchun has no O3 DATA, replace it with tuchan station
# #崇崙站在104年以後沒有資料故不用
# #大同 not use
# ## det finns inte 9 år av temp på dantuzi
# ## Det finns inte data before 2000/9 in poolee
# ####關山前五年沒資料故不用
