"""
Scrapes ward details from https://www.elections.org.za/pw/StatsData/List-Of-Current-Ward-Councillors and stores in /ward_details/data.json
"""

from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json 

current_ward_councillor_list_url="https://www.elections.org.za/pw/StatsData/List-Of-Current-Ward-Councillors"

def get_provinces(session:requests.Session)->list:
    """
    Gets all provinces found on website
    """
    response=session.get(current_ward_councillor_list_url)
    if response.status_code!=200:
        raise Exception(response.reason)
    soup = BeautifulSoup(response.text, 'html.parser')
    provinces=soup.select(selector="#MainContent_ddlProvinces option")[1:]
    provinces=[(province.get("value"),province.text) for province in provinces]
    return provinces

def format_form(inputs:list)->dict:
    """
    Creates a dict from form inputs.\n
    Example: `{"input.name":"input.value", ...}`
    """
    form={}
    for element in inputs:
        form[element.get('name')]=element.get("value")
    return form

def get_municipalities(province:tuple,session:requests.Session)->list:
    """
    Returns a list of municipalities found on website when province is chosen
    """
    res=session.get(current_ward_councillor_list_url,headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
    if res.status_code!=200:
        raise Exception(res.reason)
    htmlpage=res.text
    soup = BeautifulSoup(htmlpage, 'html.parser')
    inputs=soup.select_one("form#ctl01").select("input,select")
    form=format_form(inputs)
    form["ctl00$MainContent$ddlProvinces"]=province[0]
    form["ctl00$MainContent$ddlMunicipalities"]=-1
    form["ctl00$MainContent$ddlWards"]=-1
    form["__ASYNCPOST"]=True
    form["ctl00$ctl13"]="ctl00$MainContent$MainUpdatePanel|ctl00$MainContent$ddlProvinces"
    form["__EVENTTARGET"]="ctl00$MainContent$ddlProvinces"
    response=session.post(current_ward_councillor_list_url,data=form,cookies=res.cookies,headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
    new_soup = BeautifulSoup(response.text, 'html.parser')
    municipalities=new_soup.select("#MainContent_ddlMunicipalities option")[1:]
    municipalities=[(municipality.get("value"),municipality.text) for municipality in municipalities]
    return municipalities


def get_wards_from_html(htmlpage:str)->list:
    """
    Returns a list of wards from raw htmlpage
    """
    soup=BeautifulSoup(htmlpage,"html.parser")
    wards=soup.select("#MainContent_ddlWards option")[1:]
    wards=[(ward.get("value"),ward.text) for ward in wards]
    return wards

def get_municipality_wards(driver:webdriver.Chrome,selector:str, municipality:tuple):
    """
    Returns a list of wards found in webpage when municipality is chosen
    """
    municipalities_dropdown=driver.find_element(By.CSS_SELECTOR,selector)
    municipalities_dropdown.click()
    time.sleep(3)
    municipalities_dropdown=driver.find_element(By.CSS_SELECTOR,selector)
    municipalities_dropdown.find_element(By.CSS_SELECTOR,f"option[value='{municipality[0]}']").click()
    time.sleep(2)
    wards=get_wards_from_html(driver.page_source)
    return wards

def get_ward_detail(driver:webdriver.Chrome,selector:str,ward:tuple)->dict:
    """
    Returns the ward details of a specific ward
    """
    councillor={
        "Name":"",
        "Affiliation":"",
        "party":{
            "logo":"",
            "representative":"",
            "telephone":"",
            "fax":"",
            "postal_address":"",
            "website":"",
        }
    }
    wards_dropdown=driver.find_element(By.CSS_SELECTOR,selector)
    wards_dropdown.click()
    try:
        #click ward numer in dropdown
        wards_dropdown.find_element(By.CSS_SELECTOR,f"option[value='{ward[0]}']").click()
        time.sleep(4)
        soup=BeautifulSoup(driver.page_source,"html.parser")

        councillor["Name"]=soup.select_one("#MainContent_uxWCNameDataField").text.strip()
        councillor["Affiliation"]=soup.select_one("#MainContent_uxWCAffiliationDataField").text.strip()
        councillor["party"]["logo"]=soup.select_one("#MainContent_uxPartyLogo").get("src").strip()
        councillor["party"]["representative"]=soup.select_one("#MainContent_uxWCPartyNameDataField").text.strip()
        councillor["party"]["telephone"]=soup.select_one("#MainContent_uxWCPartyTelephoneDataField").text.strip()
        councillor["party"]["fax"]=soup.select_one("#MainContent_uxWCPartyFaxDataField").text.strip()
        councillor["party"]["postal_address"]=soup.select_one("#MainContent_uxWCPartyAddressDataField").text.strip()
        councillor["party"]["website"]=soup.select_one("#MainContent_uxWCPartyWebsiteDataField").text.strip()
    except:
        pass
    return {"councillor":councillor}


def get_ward_details(driver:webdriver.Chrome,province:tuple,session:requests.Session)->dict:
    """
    Returns all municipalities, ward and ward details found in province\n
    Format:\n 
    {
        municipality:
        {
            ward:{
                # ward details
            }
        }
    }
    """
    municipalities_dropdown_selector="#MainContent_ddlMunicipalities"
    provinces_dropdown_selector="#MainContent_ddlProvinces"
    wards_dropdown_selector="#MainContent_ddlWards"
    municipalities=get_municipalities(province,session)
    province_dropdown=driver.find_element(By.CSS_SELECTOR,provinces_dropdown_selector)
    
    province_dropdown.click()
    province_dropdown.find_element(By.CSS_SELECTOR,f"option[value='{province[0]}']").click()
    data={}
    time.sleep(3)
    for municipality in municipalities:
        data[municipality[1]]={}
        wards=get_municipality_wards(driver,municipalities_dropdown_selector,municipality)
        for ward in wards:
            data[municipality[1]][ward[1]]=get_ward_detail(driver,wards_dropdown_selector,ward)
    return data



if __name__=="__main__":
    with requests.session() as session:
        session.headers.update({"origin":"https://www.elections.org.za","referer":"https://www.elections.org.za/pw/StatsData/List-Of-Current-Ward-Councillors","ec-ch-ua": "\"Google Chrome\";v=\"105\", \"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"105\"",
            "sec-ch-ua-mobile": "?0","sec-ch-ua-platform": "macOS","sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors","sec-fetch-site": "same-origin","user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
        provinces=get_provinces(session)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(executable_path="./chromedriver",options=options)
        driver.get(current_ward_councillor_list_url)
        time.sleep(7)
        data={}
        for province in provinces:
            data[province[1]]=get_ward_details(driver,province,session)
            with open("ward_details/data.json","w+") as f:
                f.write(json.dumps(data))
                f.close()
        


