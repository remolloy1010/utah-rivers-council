#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 20 17:40:40 2022

@author: remolloy101
"""

import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import numpy as np

################# Initialize Beautiful Soup Instance #########################
# def initialize_bs_instance(url, county_name):
#   URL = ''.join([url, county_name])
#   page = requests.get(URL)
  
#   soup = BeautifulSoup(page.content, "html.parser")
#   print(soup.find("h2", class_=False, id=False).find_next_sibling(text=True))
  
#   table = soup.findAll("table")[0].find("table") # finds table inside table

################# Create table of water rights data by scraping web via url #################
def initialize_bs_table(url, county_name):

  URL = ''.join([url, county_name])
  page = requests.get(URL)
  
  soup = BeautifulSoup(page.content, "html.parser")
  print(soup.find("h2", class_=False, id=False).find_next_sibling(text=True))
  
  table = soup.findAll("table")[0].find("table") # finds table inside table
  
  # Define dataframe
  df = pd.DataFrame(columns=['RowId', 'Water Right', 'Priority Year', 'Priority Month', 'Priority Day', 'Diversion (acft)', 'Depletion (acft)', 'Cumulative Diversion (acft)', 'Cumulative Depletion (acft)', 'County', 'Source', 'Status', 'Owner Name'])

  # Collecting data
  for row in table.find_all('tr')[2:]:  #skip first two rows which are headers   
      # Find all data for each column
      columns = row.find_all('td')
      
      row_id = columns[0].text
      water_right = columns[1].text
      year = columns[2].get_text(strip=True)
      month = columns[3].get_text(strip=True)
      day = columns[4].get_text(strip=True)
      diversion = columns[5].text
      depletion = columns[6].text
      cum_diversion = columns[7].text
      cum_depletion = columns[8].text
      county = columns[9].text
      source = columns[10].text
      status = columns[11].text
      
      if columns[12].find('br'):
          ls = columns[12].contents
          for i in ls:
              if isinstance(i, Tag):
                  i.extract()
          owner = columns[12].contents
      else:
          owner = columns[12].text

      df = df.append({
          'RowId': row_id,  
          'Water Right': water_right, 
          'Priority Year': year, 
          'Priority Month': month, 
          'Priority Day': day, 
          'Diversion (acft)': diversion,
          'Depletion (acft)': depletion,
          'Cumulative Diversion (acft)': cum_diversion,
          'Cumulative Depletion (acft)': cum_depletion,
          'County': county,
          'Source': source,
          'Status': status,
          'Owner Name': owner
          }, ignore_index=True)
  print(df.head())
  return(df)


initialize_bs_table("https://www.waterrights.utah.gov/distinfo/colorado/WRPriorityDDview.asp?county=", "CN")