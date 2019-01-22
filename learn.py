import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import make_classification
from getData import compile_data_oneStock

# back-testing potential profit of a stock
def testStock(ticker):
    df = compile_data_oneStock(ticker)
    df = df.reset_index()

    moneySpent, moneyEarned = 0,0

    for index, row in df.iterrows():
        if index >= 120:
            continue
        
        test = [[row["10D_SMA"], row["20D_SMA"], row["30D_SMA"]]]
        result = (neigh.predict(test))

        if result == [1]:
            moneySpent = 100 * row['close']
            moneyEarned = 100 * df.at[index + 10, 'close']

    if moneySpent == 0:
        earningPercentage = 0
    else:
        earningPercentage = (moneyEarned - moneySpent) / moneySpent * 100
        
    print("{}: {}".format(ticker, earningPercentage))

df = pd.read_csv("compiledData.csv", index_col=0)
clf = RandomForestClassifier(n_estimators=200, max_depth=4, random_state=0)
neigh = KNeighborsClassifier(n_neighbors=3)

yTrain = (df.iloc[0:80000])["RESULT"].values.tolist()
xTrain = (df.iloc[0:80000]).drop(columns = ["RESULT", "close"]).values.tolist()

neigh.fit(xTrain, yTrain)
clf.fit(xTrain, yTrain)

# #To view the distribution of buys/holds/sells and accuracy of classifier
# correctDistribution = [0,0,0] #number of buys, holds, sells
# distributionRF = [0,0,0] # number of buys, holds, sells for Random Forest
# distributionKN = [0,0,0] # number of buys, holds, sells for KNN
# correctRF, incorrectRF = 0,0 # to test for accuracy for RF
# correctKN, incorrectKN = 0,0 # to test for accuracy for KNN

# yTest = (df.iloc[80001:])["RESULT"].values.tolist()
# xTest = (df.iloc[80001:]).drop(columns = ["RESULT", "close"]).values.tolist()

# for i in range(len(yTest)):
#     correct = yTest[i]
#     predictRF = (clf.predict([xTest[i]]))[0]
#     predictKN = (neigh.predict([xTest[i]]))[0]

#     if correct == predictRF:
#         correctRF += 1
#     else:
#         incorrectRF +=1

#     if correct == predictKN:
#         correctKN += 1
#     else:
#         incorrectKN += 1

#     if correct == 1:
#         correctDistribution[0] += 1
#     elif correct == 0:
#         correctDistribution[1] += 1
#     else:
#         correctDistribution[2] += 1

#     if predictRF == 1:
#         distributionRF[0] += 1
#     elif predictRF == 0:
#         distributionRF[1] += 1
#     else:
#         distributionRF[2] += 1

#     if predictKN == 1:
#         distributionKN[0] += 1
#     elif predictKN == 0:
#         distributionKN[1] += 1
#     else:
#         distributionKN[2] += 1

# print(correctDistribution)
# print(distributionRF)
# print(distributionKN)
# print(correctRF/(correctRF + incorrectRF) * 100)
# print(correctKN/(correctKN + incorrectKN) * 100)

testList = ['ZTS', 'ZION', 'ZBH', 'YUM', 'XYL', 'XRX', 'XRAY', 'XOM', 'XLNX']
for ticker in testList:
    testStock(ticker)