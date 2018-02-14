import rawdata as rd
import statsmodels.api as stam
import matplotlib.pyplot as plt
import itertools
import warnings
##### ARIMA : CO, SO2, NO, NO2,NOx ,PM10, O3
###################################################################################################
#     The statsmodels library provides the capability to fit an ARIMA model.                      #
#                                                                                                 #
#     An ARIMA model can be created using the statsmodels library as follows:                     #
#                                                                                                 #
#     Define the model by calling ARIMA() and passing in the p, d, and q parameters.              #
#     The model is prepared on the training data by calling the fit() function.                   #
#     Predictions can be made by calling the predict() function and specifying the                #
#     index of the time or times to be predicted.                                                 #
###################################################################################################
###training set

# CO
taoyuan = rd.dataframemerge("CO",rd.TAOYUAN)
taoyuan['2000-01-09'].plot()
plt.show()
# Define the p, d and q parameters to take any value between 0 and 2
# p = d = q = range(0, 2)

# # Generate all different combinations of p, q and q triplets
# pdq = list(itertools.product(p, d, q))
#
# # Generate all different combinations of seasonal p, q and q triplets
# seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
#
# print('Examples of parameter combinations for Seasonal ARIMA...')
# print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
# print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
# print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
# print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
# warnings.filterwarnings("ignore") # specify to ignore warning messages
#
# for param in pdq:
#     for param_seasonal in seasonal_pdq:
#         try:
#             mod = stam.tsa.statespace.SARIMAX(dataframemerge('CO', rd.TAOYUAN),
#                                             order=param,
#                                             seasonal_order=param_seasonal,
#                                             enforce_stationarity=False,
#                                             enforce_invertibility=False)
#
#             results = mod.fit()
#
#             print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
#         except:
#             print("error")