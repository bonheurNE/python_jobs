# importing necessary buildin modules
import os
import json

# importing necessary external modules
import requests
import lxml
from bs4 import BeautifulSoup


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


# function  to run the main function code
if __name__ == "__main__":
    # the url link to the oficial python available jobs
    url_link = ""
    
    # the main function 
    get_jobs(url=url_link)
