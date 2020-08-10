##from sklearn.datasets import load_iris
##from sklearn.linear_model import LogisticRegression
##
##X, y = load_iris(return_X_y=True)
##print X,y



import sqlite3,numpy
from sklearn import datasets, linear_model, metrics


logistic = linear_model.LogisticRegression(max_iter=1000)

column = "Sentiment"
predField = "Positive"
features = ["I", "my", "uh", "$"]

xtrain = []
ytrain = []
xtest = []
ytest = []

posCountTrain = 0
posCountTest = 0

##GET TOTAL ROW COUNT
CONN = sqlite3.connect("Database\\Corpus.db")

Q = 'SELECT COUNT(ID) FROM "AnnotationMaster"'

CURSOR = CONN.cursor()
CURSOR.execute(Q)

alldem = CURSOR.fetchall()

CONN.close()

## IF ANY ROWS EXIST, MOVE ON
if len(alldem) > 0:

    ## GET TOTAL ROWS, DIVIDE BY TWO FOR TRAIN/TEST SETS
    rowCount = int(alldem[0][0])
    rowCountHalf = int(alldem[0][0])/2
    
    print "Count = ", rowCount, rowCountHalf

    CONN = sqlite3.connect("Database\\Corpus.db")
    ## GET TOP "rowCountHalf" ROWS FROM DB
    Q = 'SELECT {}, Sentence FROM "AnnotationMaster" ORDER BY ID ASC LIMIT {}'.format(str(column), str(rowCountHalf))

    CURSOR = CONN.cursor()
    CURSOR.execute(Q)

    alldem = CURSOR.fetchall()

    CONN.close()

    if len(alldem) > 0:

        # LOOP ALL RETURNED ROWS FOR TRAINING
        for i in alldem:

            # CONVERT PREDICTEDFIELD TO 1 OR 0
            if str(i[0]) == str(predField):
                ytrain.append([1])
                posCountTrain += 1
            else:
                ytrain.append([0])

            # CONVERT FEATURES TO 1 OR 0 (1 = IN SENTENCE; 0 = NOT IN SENTENCE)
            featureScore = []
            for j in features:
        
                if j in i[1]:
                    featureScore.append(1)
                else:
                    featureScore.append(0)

            xtrain.append(featureScore)
            
          #  print "xt", xtrain


############ GET TEST DATA
    CONN = sqlite3.connect("Database\\Corpus.db")

    ### GET BOTTOM "rowCountHalf" FROM THE DATABASE
    Q = 'SELECT {}, Sentence FROM "AnnotationMaster" ORDER BY ID DESC LIMIT {}'.format(str(column), str(rowCountHalf))

    CURSOR = CONN.cursor()
    CURSOR.execute(Q)

    alldem = CURSOR.fetchall()

    CONN.close()

    if len(alldem) > 0:

        for i in alldem:

            if str(i[0]) == str(predField):
                ytest.append([1])
                posCountTest += 1
            else:
                ytest.append([0])

            featureScore = []
            for j in features:
        
                if j in i[1]:
                    featureScore.append(1)
                else:
                    featureScore.append(0)

            xtest.append(featureScore)
            
    ## Y SETS NEED TO BE FLATTENED FOR THE FUNCTION TO WORK
    ytrain = numpy.ravel(ytrain)
    ytest = numpy.ravel(ytest)

    ## GET FIT AND SCORE
    lf = logistic.fit(xtrain,ytrain,sample_weight=[[1,2]])
    probs = lf.predict_proba(xtrain)
    print probs
    class1_1 = [pr[0] for pr in probs]
    print class1_1
    score = lf.score(xtest,ytest)
####
    # PRINT THE SCORE..
    print score
    print posCountTrain, "/", rowCountHalf, "Positives in Training Data"
    print posCountTest, "/", rowCountHalf, "Positives in Testing Data"

    #fpr, tpr, thresholds = metrics.roc_curve(ytest, score, pos_label=2)

    
