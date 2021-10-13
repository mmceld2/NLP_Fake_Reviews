import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, plot_confusion_matrix , accuracy_score,recall_score,f1_score,precision_score
import re

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

def gs_mean_scores(results):
    '''Return Train and Test Scores from a grid search'''
    return print(f'''Mean Train Score: {results.cv_results_['mean_train_score'].mean()}'
Mean Test Score: {results.cv_results_['mean_test_score'].mean()}''')

def total_val_count(df,column):
    '''Creates a dictionary with all value counts in column'''
    data= df[column]
    counts = {}
    for i in data:
        counts[i] = counts.get(i, 0) + 1
    counts_sorted = dict(sorted(counts.items(), key=lambda item: item[1],reverse=True))
    return counts_sorted

def val_count_nf(df,column):
    '''Creates a dictionary from a dataframe that has columns
    as keys and their total count of values that do not have functioning pumps'''
    df_val = df.loc[df['status_group'] == 1]
    counts = {}
    for i in df_val[column]:
        counts[i] = counts.get(i, 0) + 1
    counts_sorted = dict(sorted(counts.items(), key=lambda item: item[1],reverse=True))
    return counts_sorted


def addlabels(x,y,left,up):
    '''Add labels on top of each bar on bar graph'''
    for i in range(len(x)):
        plt.text(i-left,y[i]+up,y[i])

def addlabelsbig(x,y,left,up):
    '''Add BIGGER labels on top of each bar on bar graph'''
    for i in range(len(x)):
        plt.text(i-left,y[i]+up,f'{y[i]}%',fontsize=20,color='black')

def percent_dict(df,column):
    '''Creates a dictionary that has highest percent of non functioning pumps'''
    percent= []
    lst = list(df[column].unique())
    for val in lst:
        num_pumps = len(df1.loc[df[column] == val])
        fail_pumps = len(df1.loc[(df['status_group'] == 1) & (df[column] == val)])
        percent.append(round((fail_pumps/num_pumps*100),2))
    d = dict(zip(lst,percent))
    d_sorted = dict(sorted(d.items(), key=lambda item: item[1],reverse=True))
    return d_sorted

def visualize(dictionary,title=None):
    '''Creates Seaborn Barplot from Dictionary'''
    nums = list(dictionary.values())
    fig , ax = plt.subplots(figsize=(12,10))
    sns.barplot(x=list(dictionary.keys()),y=nums)
    ax.set_title(title,fontsize=15)
    ax.set_ylabel('Percent Non Functioning',fontsize=15);

def stack_it(df,column,title=None,addlabels=False):
    '''Returns Barplot showing total count of catgory type with percent of failure '''

    fig , ax= plt.subplots(nrows=1,ncols=1,figsize=(12,8))
    
    
    column_count = total_val_count(df,column)
    nums = list(column_count.values())[:5]
    top_5 = list(column_count.keys())[:5]
    transform = val_count_nf(df,column)
    num_failed = []
    for x in top_5:
        for y in transform.keys():
            if x == y:
                num_failed.append(transform[y])
    percent_failed = [round((i / j)*100,1) for i, j in zip(num_failed, nums)]
    
    ax.set_title(title,fontsize=15)
    sns.barplot(x=top_5,y=nums,alpha=.4,label='Total Count',color='orange')
    ax.set_ylabel('Total Count',fontsize=15)
    sns.barplot(x=top_5, y=num_failed,label='Amount Failed',color='orange')
    plt.xticks(rotation=45,fontsize=15)
    plt.yticks(fontsize=15)
    if addlabels:        
        addlabelsbig(top_5,percent_failed,.2,100);
        

        

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
        
        
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
