from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
import matplotlib.pyplot as plt

def run(trainData, testData):
    # Generate counts from text using a vectorizer.
    # This performs our step of computing word counts.
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    inp = []
    for t in trainData:
        for p in t["phrases"]:
            inp.append(p[0])
    train_features = vectorizer.fit_transform(inp)
    test_features = vectorizer.transform([t["sentence"] for t in testData])
    actual = [t["label"] for t in testData]

    # Fit a naive bayes model to the training data.
    nb = MultinomialNB()
    labels = []
    for t in trainData:
        for p in t["phrases"]:
            labels.append(p[1])
    nb.fit(train_features, labels)

    predictions = nb.predict(test_features)

    fpr, tpr, thresholds = metrics.roc_curve(actual, predictions)
    print("Multinomial naive bayes AUC: {0}".format(metrics.auc(fpr, tpr))," fpr and tpr:", fpr, tpr)
    roc_auc = metrics.auc(fpr, tpr)
    return roc_auc, fpr, tpr

def generate_plot(roc_auc, fpr, tpr):
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b',
    label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()
