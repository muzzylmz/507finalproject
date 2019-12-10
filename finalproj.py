import sqlite3 as sqlite
import sqlite3
import requests
import json
from bs4 import BeautifulSoup
import plotly.offline as py
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
# import MySQLdb
import csv
import matplotlib
# import matplotlib.pyplot as plt
import numpy as np

from matplotlib import pyplot as plt

# ----------------------Set up caching-------------------------------
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

class UX_company_list():
    def __init__ (self,company_name= '', city='', country='', lat='', lng='', companylink=''):

        self.company_name= company_name
        self.city= city
        self.country= country
        self.lat= lat
        self.lng= lng
        self.companylink= companylink
    def __repr__(self):
        return "{} is located in {} {}: {} {}, please check {}".format(self.company_name, self.city,self.country,self.lat,self.lng,self.companylink)

class UX_jobs_list():
    def __init__ (self,title='', employ_type='', company_name='', city='', country='', post_date=''):
        self.title=title
        self.employ_type= employ_type
        self.company_name= company_name
        self.city= city
        self.country= country
        self.post_date= post_date
    def __repr__(self):
        return "{} is looking for {} {} in {} ,{} on {}!".format(self.company_name, self.employ_type,self.title,self.city,self.country,self.post_date)

# ----------------------Cache------------------------------------

def make_request_using_cache(url):
    unique_ident =  get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new datad
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

# Get job data
#
def get_uxjobs_data():
    url = 'https://www.uxjobsboard.com/'
    page_data = make_request_using_cache(url)
    page_soup = BeautifulSoup(page_data, 'html.parser')
    items = page_soup.find_all('li',class_='job-item')
    # print(len(items))
    job_details = []
    company_details = []
    for num in range(50):
    # for item in items:
        link= items[num].find('a',class_='title-link title')['href']
    #     print(link)
        detail_page_data = make_request_using_cache(link)
        detail_soup = BeautifulSoup(detail_page_data, 'html.parser')
        company_name= detail_soup.find(id='job_author_name').text.strip()
#         print(company_name)
        title= detail_soup.find(id='job_title').text.strip().split('\t')[0]
#         print(title)
        location= detail_soup.find(id='job_location').text.strip().split(',')
#         print(location)

        if len(location)==1:
            city= 'Anywhere'
            country = location[0]
        else:
            city = location[0]
            country = location[-1]
        employ_type= detail_soup.find('div',id='job_type').text.strip()
#         print(employ_type)
        post_date= detail_soup.find('div',class_='date').text.strip()
#         print(date)
        companylink= detail_soup.find('a', id='job_author_url')['href']
#         print(companylink)

        # get job location (lat lgn)
        lat = detail_soup.find('input', {'name': 'jobLocLat'}).get('value')
#         print(lat)
        lng = detail_soup.find('input', {'name': 'jobLocLng'}).get('value')

        job_list= (title, employ_type, company_name,post_date)
        company_list=(company_name, city, country, lat, lng, companylink)
        job_details.append(job_list)
        # print(job_details)
        company_details.append(company_list)
        # print(company_details)

    return job_details,company_details


def getstring():
    url = 'https://www.uxjobsboard.com/'
    page_data = make_request_using_cache(url)
    page_soup = BeautifulSoup(page_data, 'html.parser')
    items = page_soup.find_all('li',class_='job-item')
    # print(len(items))
    job_details2 = []
    company_details2 = []
    for num in range(50):
    # for item in items:
        link= items[num].find('a',class_='title-link title')['href']
    #     print(link)
        detail_page_data = make_request_using_cache(link)
        detail_soup = BeautifulSoup(detail_page_data, 'html.parser')
        company_name= detail_soup.find(id='job_author_name').text.strip()
#         print(company_name)
        title= detail_soup.find(id='job_title').text.strip().split('\t')[0]
        # print(title)
        location= detail_soup.find(id='job_location').text.strip().split(',')
        # print(location)

        if len(location)==1:
            city= 'Anywhere'
            country = location[0]
        else:
            city = location[0]
            country = location[-1]

        employ_type= detail_soup.find('div',id='job_type').text.strip()
#         print(employ_type)
        post_date= detail_soup.find('div',class_='date').text.strip()
#         print(date)
        companylink= detail_soup.find('a', id='job_author_url')['href']
        lat = detail_soup.find('input', {'name': 'jobLocLat'}).get('value')
#         print(lat)
        lng = detail_soup.find('input', {'name': 'jobLocLng'}).get('value')

        job_details2.append(UX_jobs_list(title, employ_type, company_name, city, country, post_date))

        # print(job_details2)
        company_details2.append(UX_company_list(company_name, city, country, lat, lng, companylink))

        # print(company_details2)
    return job_details2, company_details2

# i= getstring()
# for k in i:
#     print('Job list:', *k, sep='\n- ')



####### create a database############
DBNAME = 'ux-job.db'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

def insert_database():
# Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Jobs';
    '''
    cur.execute(statement)

    statement = """
        CREATE TABLE 'Jobs' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Title' Text NOT NULL,
        'JobType' Text NOT NULL,
        'CompanyName' Text NOT NULL,
        'CompanyId' Integer,
        'PostDate' Text
    );
        """
    cur.execute(statement)
    conn.commit()
# Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Companies';
    '''
    cur.execute(statement)

    statement = """
        CREATE TABLE 'Companies' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' Text NOT NULL,
        'City' Text NOT NULL,
        'Country' Text NOT NULL,
        'Lat' Text NOT NULL,
        'Lon' Text NOT NULL,
        'CompanySite' Text NOT NULL
    );
        """
    cur.execute(statement)
    conn.commit()

def update_database(results):
    job_details = results[0]
    company_details = results[1]
    for result in job_details:
        statement = """
        INSERT INTO Jobs (Id, Title, JobType, CompanyName, PostDate)
        VALUES (NULL,?,?,?,?)
        """
        cur.execute(statement, result)
        conn.commit()
    for result in company_details:
        statement = """
        INSERT INTO Companies (Id, Name, City, Country, Lat, Lon, CompanySite)
        VALUES (NULL,?,?,?,?,?,?)
        """
        cur.execute(statement, result)
        conn.commit()

    statement = '''
    UPDATE Jobs
    SET CompanyId = (SELECT Id
    FROM Companies
    WHERE Jobs.CompanyName= Companies.Name)
    '''
    cur.execute(statement)
    conn.commit()

#### visualization

## histgram
# import matplotlib
# from matplotlib import pyplot as plt
# bins= [0,5,10,15,20,25,30,35,40,45,50]
# df = pd.read_csv('Jobs.csv')
# plt.hist(df.CompanyId)
# plt.xlabel('CompanyID')
# plt.ylabel('Number of UX jobs posted')
# plt.title('Distribution of UX jobs posted by companies')
# plt.xticks(bins)
# plt.show()
# plt.savefig("hist.png")
#
# ###
# bins= [0,5,10,15,20,25,30,35,40,45,50]
# plt.plot(df.CompanyId,df.PostDate)
# plt.xlabel('CompanyID')
# plt.ylabel('Job Posted Date')
# plt.title('Illustration of dates companies posted jobs')
# plt.show()
# plt.savefig("plot2.png")
# # ##
# plt.style.use('seaborn')
# dc = pd.read_csv('Companies.csv')
# plt.scatter(x=dc.Lat,y=dc.Lon,s=100,edgecolor='black',linewidth=1,alpha=1)
# plt.xlabel('latitude of the company')
# plt.ylabel('longitude of the company')
# plt.title('Scatter plot to display lat and lon of the companies')
# plt.show()
# plt.savefig("scatter.png")
##
# import numpy as np
# import seaborn as sns
# df = pd.read_csv('Jobs.csv')
# sns.countplot(x=df.JobType,data=df)
# sns.savefig("count.png")
# ##
#
# df = pd.read_csv('Jobs.csv')
# sns.countplot(x=df.Title,data=df)

# visualization 1

def all_job_titles():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    job_titles_1 = []
    job_ct_1 = []
    job_ct_data = '''
        SELECT Title, COUNT(Title)
        FROM Jobs
        GROUP BY Title
        ORDER BY Count(Title) DESC
        '''
    cur.execute(job_ct_data)
    for title in cur:
        job_titles_1.append(title[0])
        job_ct_1.append(title[1])
    conn.close()

    trace = [go.Bar(
                x=job_titles_1,
                y=job_ct_1)]

    data = trace
    layout = go.Layout(
    title='Overall view of number of jobs posted',)
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='text-hover-bar')



## visualization 2
def all_job_titles2():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #Alphabettically ordred top users to prep for loading into a bar chart in plotly
    job_titles_2 = []
    num_threads_2 = []


    hours_posted_threads = '''
        SELECT JobType, COUNT(JobType)
        FROM Jobs
        GROUP BY JobType
        ORDER BY COUNT(JobType)
        '''
    cur.execute(hours_posted_threads)
    for i in cur:
        job_titles_2.append(i[0])
        num_threads_2.append(i[1])

    conn.close()

    data = [go.Bar(x=job_titles_2,
                         y= num_threads_2)]

    layout = go.Layout(title='Number of different job types')

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic historgram')

# all_job_titles2()

def all_job_titles3():
    import matplotlib
    from matplotlib import pyplot as plt
    df = pd.read_csv('Jobs.csv')
    bins= [0,5,10,15,20,25,30,35,40,45,50]
    plt.plot(df.CompanyId,df.PostDate)
    plt.xlabel('CompanyID')
    plt.ylabel('Job Posted Date')
    plt.title('Illustration for dates companies posted jobs')
    plt.show()
# plt.savefig("plot2.png")
def all_job_titles4():

    plt.style.use('seaborn')
    dc = pd.read_csv('Companies.csv')
    plt.scatter(x=dc.Lat,y=dc.Lon,s=100,edgecolor='black',linewidth=1,alpha=1)
    plt.xlabel('latitude of the company')
    plt.ylabel('longitude of the company')
    plt.title('Scatter plot to display lat and lon of the companies')
    plt.show()
    plt.savefig("scatter.png")

### try to see if it works


results = get_uxjobs_data()
insert_database()
update_database(results)



#VISUALIZATION________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
def viz_help():
    print("\n\n\n\n\n")
    print("-----------------------------")
    print("1 = Displays Overall view of number of jobs posted")
    print("2 = Displays Number of different job types")
    print("3 = Displays the dates companies posted jobs")
    print("4 = Scatter plot to display lat and lon of the companies\n\n")
    print("'all' = Runs all of the above visualizations")
    print("---------------------------------")
    print("'stop' = Returns user to main menu.")
    print("\n\n")


def visual_menu():
    #Be sure to build at least four visualizations
    print("********\nWELCOME TO THE VISUALIZATION MENU\n*********")
    visualization = ""
    while visualization != "exit":
        viz_help()
        visualization = input("\nPlease enter a visualization # for your data to display.\n\nEnter visualization: ")
        if visualization == "exit":
            print("Exiting Visualization Menu...\n\n-------")
            return
        elif visualization == "1":
            print(visualization)
            all_job_titles()
        elif visualization == "2":
            print(visualization)
            all_job_titles2()
        elif visualization == "3":
            print(visualization)
            all_job_titles3()
        elif visualization == "4":
            print(visualization)
            all_job_titles4()
        elif visualization == "all":
            print(visualization)
            all_job_titles() #Run plot 1
            all_job_titles2() #Run plot 2
            all_job_titles3() #Run plot 3
            all_job_titles4() #Run plot 4
        elif visualization == 'exit':
            break
        else:
            print("ERROR. Invalid Command, Try again.")

#####interaction
def menu_prompt():
    response = ''
    while response != 'exit':
        print('\nPlease pick a command or enter "help" to see commands.')
        response = input('Enter a command: ')
        if response == 'exit':
            break
        elif response=='help':
            viz_help()
            visual_menu()
        elif response=='plots':
            visual_menu()
        elif response== 'list':
            i=getstring()
            for k in i:
                print('Job list:', *k, sep='\n- ')
        else:
            print("Command Not recognized" + response)

menu_prompt()
# menu_prompt()

if __name__ == "__main__":

    results = get_uxjobs_data()
    insert_database()
    update_database(results)


    #write out file
    d_dict = json.dumps(results, indent=4)
    fw = open('directory_dict.json', 'w')
    fw.write(d_dict)
    fw.close()
