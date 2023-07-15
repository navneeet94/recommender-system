import requests
import json
import ast
import pandas as pd
import os
autorization = {"accept": "application/json", "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZDI2ZmZiNWNiZmM0OWNiNzdmNmFkYjFlMmE5MzRkMSIsInN1YiI6IjYyMGE5N2Q4MjZkYWMxMDBiODc1ZmU0OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZKQXGcGF5FkrHUW0jqcNjHXTCYS56Rlh4JToRmp2A7Q"}


# # Functions Code

# In[3]:


def extractor(category,data_kind,detail):
    if data_kind == "ids":
        url = f"https://api.themoviedb.org/3/discover/{category}?page={detail}"
    else:
        url = f"https://api.themoviedb.org/3/{category}/{detail}?api_key=8277ae593821f15114e4b063f6ff057b&append_to_response=credits"
    
    response = requests.get(url, headers=autorization)
    jsonic = response.text
    json_dump = json.dumps(jsonic)
    another_dump = json.loads(json_dump)
    data = json.loads(another_dump)
    if data_kind == 'ids':
        id_lst = []
        for i in data['results']:
            id_lst.append(i['id'])
        total_pages = data['total_pages']
        total_results = data['total_results']
        return {'pages':total_pages,'ids':id_lst,"results":total_results}
    else:
        if category == 'movie':
            return {"category":"movies","data":data}
        elif category == 'tv':
            return {"category":"tv","data":data}
    page_execution+=1


# In[4]:


def info(record):
    category = record['category']
    its_data = record['data']
    for its in its_data:
        temp_dict[its].append(its_data[its])


# In[5]:


def emptyDict(record):
    key_names = record['data'].keys()
    its_data = record['data']
    for its in key_names:
        temp_dict[its] = []
        temp_dict[its].append(its_data[its])


# In[6]:


def extract_new_record(identity):
    movie_data = extractor(extractFor,"",identity)
    if len(temp_dict) != 0:
        info(movie_data)
    else:
        emptyDict(movie_data)


# # Extract Key Value Vals

# In[7]:


def extractValues(value,name):
    value_type = type(value)
    if value_type == list:
        #print("list")
        e_val = []
        for i in value:
            e_val.append(i[name])
        return ", ".join(e_val)
    if value_type == dict:
        #print("dict")
        return value[name]
    else:
        #print("other")
        return value


# In[8]:


def extractSubValues(value,category):
    for i in value:
        if i == category:
            sub_data = value[i]
            return extractValues(sub_data,'name')


# In[9]:


def extractSubValuesCondition(value,category,job):
    for i in value:
        if i == category:
            for j in value[i]:
                if j['job'] == job:
                    return extractValues(j,'name')


# In[10]:


temp_dict = {}


# In[11]:


def addData(data):
    if len(temp_dict) != 0:
        info(data)
    else:
        emptyDict(data)


# In[12]:


def adding_new_data(page_nos,ext_name,response):
    count = 0
    for num in range(page_nos):
        record = extractor(ext_name,"ids",num+1)
        #print(f"{num} => {record}")
        if count <= response - 1:
            for data in record['ids']:
                if count <= response - 1:
                    #print(f"{count+1} => {data}")
                    movie_data = extractor(ext_name,"",data)
                    addData(movie_data)
                    count+=1
        else:
            break


# In[13]:


def updated_new_data(df,page_nos,ext_name,response):
    count = 0
    #print(df)
    for num in range(page_nos):
        record = extractor(ext_name,"ids",num+1)
        #print(f"{record}")
        if count <= response - 1:
            for data in record['ids']:
                found = df[(df['id'] == data)]
                if(found.shape[0] > 0):
                    #print(f"yes ({data})")
                    pass
                else:
                    if count <= response - 1:
                        #print(f"{count+1} => No ({data})")
                        movie_data = extractor(ext_name,"",data)
                        addData(movie_data)
                        count+=1
                    else:
                        break
        else:
            break


# In[14]:


def temporaryRec(maxRec='',extractFor=''):
    pages = extractor(extractFor,"ids",1)['pages']
    total_res = extractor(extractFor,"ids",1)['results']
    if maxRec == '':
        maxRec = total_res
        adding_new_data(pages,extractFor,maxRec)
    else:
        adding_new_data(pages,extractFor,maxRec)


# In[15]:


temporaryRec(10000,"movie")


# In[16]:


def dataconversion():
    temp_df['belongs_to_collection'] = temp_df['belongs_to_collection'].apply(lambda x: extractValues(x,'name'))
    temp_df['genres'] = temp_df['genres'].apply(lambda x: extractValues(x,'name'))
    temp_df['production_companies'] = temp_df['production_companies'].apply(lambda x: extractValues(x,'name'))
    temp_df['production_countries'] = temp_df['production_countries'].apply(lambda x: extractValues(x,'name'))
    temp_df['spoken_languages'] = temp_df['spoken_languages'].apply(lambda x: extractValues(x,'name'))
    temp_df['cast'] = temp_df['credits'].apply(lambda x: extractSubValues(x,'cast'))
    temp_df['director'] = temp_df['credits'].apply(lambda x: extractSubValuesCondition(x,'crew','Director'))


# In[17]:


temp_df = pd.DataFrame(temp_dict)
dataconversion()


# In[18]:


wanted_cols = ['adult','backdrop_path','belongs_to_collection','budget','genres','homepage','id','imdb_id','original_language',
               'original_title','overview','popularity','poster_path','production_companies','production_countries',
               'release_date','revenue','runtime','spoken_languages','status','tagline','title','video','vote_average',
               'vote_count','credits','cast','director']


# In[19]:


temp_df = temp_df[wanted_cols]


# In[20]:


print(temp_df)

