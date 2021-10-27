import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, plot_confusion_matrix , accuracy_score,recall_score,f1_score,precision_score
import re
from nltk.tokenize import regexp_tokenize, word_tokenize, sent_tokenize
from nltk.stem import SnowballStemmer
import seaborn as sns

# Some functions that may provide to be useful
def mean_scores(results):
    '''Return Train/Test Mean Score from a Cross Val'''
    return print(f'''Mean Train Score: {results['train_score'].mean()}
Mean Test Score: {results['test_score'].mean()}''')

def metrics(y_true,y_preds):
    '''Gives recall,precision,accuracy,F1 score and confusion matrix'''
    return print(f'''Recall Score: {recall_score(y_true,y_preds)}
Precision Score: {precision_score(y_true,y_preds)}
Accuracy Score:{accuracy_score(y_true,y_preds)}
F1 Score: {f1_score(y_true,y_preds)}
Confusion Matrix: 
{confusion_matrix(y_true,y_preds)}''')

def transform(df,review_col):
    '''Returns a DataFrame transformed and ready to be tested. Returns the df with 
    Tokens, Number of words, Char Review Count, Sentences and Sentence Count'''
    df_engineered = df.copy()
    # Make a column to split words up, puncuation is included
    df_engineered['Tokens'] = df[review_col].str.split(' ')
    # Find the number of words in each review
    df_engineered['Number of Words'] = df_engineered['Tokens'].map(lambda x: len(x))
    # Find number of characters used in Reviews
    df_engineered['Character Review Length'] = df_engineered[review_col].map(lambda x: len(x))
    # Find Number of Sentences in Each Review
    df_engineered['Sentences'] = df_engineered[review_col].map(lambda x:sent_tokenize(x))
    df_engineered['Sentence Count'] = df_engineered['Sentences'].map(lambda x : len(x))
    df_engineered['Avg Words Per Sentence'] = df_engineered['Number of Words'] / df_engineered['Sentence Count']
    return df_engineered


def test_df(df,review_col):
    X = df.copy()
    X = df[[review_col,'Number of Words','Character Review Length','Sentence Count','Avg Words Per Sentence']]
    # Remove all numbers
    X[review_col] = X[review_col].str.replace('\d+', '')
    # Make a tokenize column
    X['token'] = X[review_col].map(lambda x: word_tokenize(x))
    # Stem words in the tokenized column then create a column where they are joined
    X['stem'] = X['token'].apply(lambda x: [SnowballStemmer('english').stem(y) for y in x])
    X['sentence'] = X['stem'].apply(lambda x : ' '.join(x))
    # Add all of our extra features in
    X = X[['sentence','Number of Words','Character Review Length','Sentence Count','Avg Words Per Sentence']]
    return X

def gs_mean_scores(results):
    '''Return Train and Test Scores from a grid search'''
    return print(f'''Mean Train Score: {results.cv_results_['mean_train_score'].mean()}'
Mean Test Score: {results.cv_results_['mean_test_score'].mean()}''')


def addlabels(x,y,left,up,font=12):
    '''Add labels on top of each bar on bar graph'''
    for i in range(len(x)):
        plt.text(i-left,y[i]+up,y[i],fontsize=font)


def word_stats(df,col_name,xlabel,ylabel,title,left_right,up_down):
    avg_review_length = df[col_name].mean()
    avg_fake_length = df.loc[df['Label'] == -1][col_name].mean()
    avg_real_length = df.loc[df['Label'] == 1][col_name].mean()
    
    fig , ax = plt.subplots(figsize=(10,8))

    x= ['All Reviews', 'Fake Reviews','Real Reviews']
    y=[round(avg_review_length,2),round(avg_fake_length,2),round(avg_real_length,2)]

    sns.barplot(x=['All Reviews', 'Fake Reviews','Real Reviews'],y=[avg_review_length,avg_fake_length,avg_real_length],palette=['lightblue','red','green'])
    ax.set_title(title,fontsize=20)
    addlabels(x,y,left_right,up_down,font=15)
    ax.set_ylabel(ylabel,fontsize=17)
    ax.set_xlabel(xlabel,fontsize=17)
    plt.xticks(fontsize=15);

    
    return print(f'''Avg Review: {round(avg_review_length,2)}
Avg Fake Review: {round(avg_fake_length,2)}
Avg Real Review: {round(avg_real_length,2)}''')

             

