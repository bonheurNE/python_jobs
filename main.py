# importing necessary buildin modules
import os
import json

# importing necessary external modules
import requests
import lxml
from bs4 import BeautifulSoup

data = {}

def get_jobs(url:str) -> None:
    # get the url to use 
    url = url
    
    # get the first response to request to the provided url
    response = requests.get(url)

    # get the base url we'll use into the rest of the code
    base_url = response.url
    
    # get extacted data 
    soup = BeautifulSoup(response.content, 'lxml')

    # find all <ul> tags with "pagination menu" as class attr
    page_ul_tag = soup.find('ul', class_="pagination menu")
    
    # find all <a> tag in all founded <ul> with class attr "pagination menu"
    page_a_tag = page_ul_tag.find_all('a')

    # list to contain all available pages hrefs
    available_hrefs = []

    for i in page_a_tag:
        # get all available pages href from each <a> tag
        i = i.get('href')
        
        # if the href is nnot empty than append the $available_hrefs list
        if i != '':
            available_hrefs.append(i)

    # generate new urls responses for each available page
    for i in range(1, len(available_hrefs)):
        # define data to put on the request url querry
        data = {"page": f"{i}"}

        #get the response to request to all the provided urls
        response = requests.get(url, data)
        
        # if the status code for the request is 200 of OK
        # we create a tuple that will contain the response and the base url trans_data
        if response.status_code == 200:
            trans_data = (response, base_url)
            
            # get the jobs data and store them on a json file 
            get_job_names_href(trans_data)
        else:
            pass
    pass


def get_job_names_href(tuple_data: tuple) -> None:
    # get response and base url from the tuple
    response = tuple_data[0]
    base_url = tuple_data[1]

    # Parse the HTML content using BeautifulSoup
    html_data = BeautifulSoup(response.content, 'lxml')

    # find all html code inside the section tag with "main-content with-right-sidebar" as class attr
    result = html_data.find(
        'section', class_="main-content with-right-sidebar")
    
    # list all <span> tag elements with "listing-company-name" as class attr
    elements = result.find_all('span', class_="listing-company-name")

    if os.path.exists('python_jobs.json'):
        # open the json file and load it's data -> dict
        with open('python_jobs.json', 'r') as f:
            json_d = json.load(f)
            f.close()

        # write the json data dict by adding data to the dict than write it
        for a_tag in elements:
            a = a_tag.find('a')
            job_title = a.text

            job_ref = a.get('href')
            job_ref = job_ref.split('/')
            job_ref = job_ref[2]

            json_d[job_title] = {'job title': job_title,
                                 'job ref web site': job_ref}

        # serializing json
        json_data = json.dumps(json_d, indent=4)
        # write on the json file
        with open('python_jobs.json', 'w') as json_file:
            json_file.write(json_data)
            json_file.close()
            print(f"file python_jobs.json created succefully ")
    else:
        for a_tag in i:
            a = a_tag.find('a')
            job_title = a.text

            job_ref = a.get('href')
            job_ref = job_ref.split('/')
            job_ref = job_ref[2]

            data[job_title] = {'job title': job_title,
                               'job ref web site': job_ref}

        # serializing json
        json_data = json.dumps(data, indent=4)
        # write on the json file
        with open('python_jobs.json', 'w') as json_file:
            json_file.write(json_data)
            json_file.close()
            print(f"file python_jobs.json created  for the first time ")


# function  to run the main function code
if __name__ == "__main__":
    # the url link to the oficial python available jobs
    url_link = "https://www.python.org/jobs"
    
    # the main function 
    get_jobs(url=url_link)
