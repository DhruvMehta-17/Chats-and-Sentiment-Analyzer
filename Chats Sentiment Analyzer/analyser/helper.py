from collections import Counter
import os
import numpy as np
import pandas as pd
from textblob import TextBlob
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()

negative_user_name = []
negative_user_score=[]

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def find_positive(df):
    ans = []
    prac_df = df
    for k in df['message']: 
        analysis = TextBlob(k)
        ans.append(analysis.sentiment[0]) 
    sentiment = pd.Series(ans)  
    prac_df=pd.concat([prac_df, sentiment],axis=1)
    prac_df.rename(columns={prac_df.columns[12]:'sentiment'},inplace=True)
    df = prac_df
    def total_unique_sentimental_score(df):
        sentimental_sum = {}
        total_count = df.count().user
        for i in range(0, total_count):
          user_name = df['user'][i]
          if (user_name in sentimental_sum):
            prev_sentimental_val = sentimental_sum[user_name]
            new_sentimental_val = df['sentiment'][i]
            sentimental_sum[user_name] = prev_sentimental_val + new_sentimental_val
          else:
            sentimental_sum[user_name] = df['sentiment'][i]
        return sentimental_sum

    sentimental_sum = total_unique_sentimental_score(df)
    def total_unique_sentimental_count(df):
      sentimental_count = {}
    
      total_count = df.count().user
      for i in range(0, total_count):
        user_name = df['user'][i]
        if (user_name in sentimental_count):
          sentimental_count[user_name] += 1
        else:
          sentimental_count[user_name] = 1
      return sentimental_count

    sentimental_count = total_unique_sentimental_count(df)
    def average_sentimental_score(sentimental_count, sentimental_sum):
  
        Average_sentimental_score = {}
        arr1 = []
        arr2 = []
        average_senti = []
        count = 0
        
        for i in sentimental_sum:
          arr1.append(sentimental_sum[i])
        
        for i in sentimental_count:
          arr2.append(sentimental_count[i])
        
        average_score = list(np.array(arr1) / np.array(arr2))
        
        for i in sentimental_count:
          Average_sentimental_score[i] = average_score[count]
          count += 1
        
        return Average_sentimental_score
        
        
    x = average_sentimental_score(sentimental_count, sentimental_sum)
    positive_user_name =[]
    positive_user_score = []
    
    for i in x:
        if x[i]>0:
            positive_user_name.append(i)
        if x[i]<0:
            negative_user_name.append(i)
    for i in x:
        if x[i]>0:
            positive_user_score.append(x[i])
        if x[i]<0:
            negative_user_score.append(x[i])
    positive_datafram = pd.DataFrame(list(zip(positive_user_name, positive_user_score)),
               columns =['Name', 'sentiment'])
   
    return positive_datafram

def find_negative(df):
    negative_datafram = pd.DataFrame(list(zip(negative_user_name, negative_user_score)),
               columns =['Name', 'sentiment'])
    return negative_datafram


def create_wordcloud(selected_user,df):

   

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "analyser\stopword.txt"
    stop_words = os.path.join(script_dir, rel_path)
    # f = open("stopword.txt", 'r')
    # stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "analyser\stopword.txt"
    stop_words = os.path.join(script_dir, rel_path)

    # f = os.open("stopword.txt",os.O_RDONLY)
    # hi = os.read(f,7063)
    # stop_words=hi.decode("UTF-8")
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
