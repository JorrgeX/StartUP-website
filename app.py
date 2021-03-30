from flask import Flask, render_template, url_for,request

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/about', methods=["GET"])
def about():
    return render_template('about.html')

@app.route('/contact', methods=["GET"])
def contact():
    return  render_template('contact.html')



## Code added here by @umar

@app.route('/getresults', methods=['POST'])
def getresults():
  #print ('data submitted')
  #my_list = ['p', 'r', 'o', 'b', 'e']
  #my_tuple = (1, 2, 3)
  zipcode_input = request.form['zipcode']
  
  fund_desc = request.form['funding']
  fund_desc = fund_desc.replace(',','') # in order to handle 5,000 as 5000.. other wises messesup!!
  import pandas as pd
  import numpy as np
  import regex as re
  df=pd.read_csv('Startup_Data.csv')
  #zipcode_input = "Our company would like to build a brand new company in Melbourne,FL there is one office in 35242 and one office in 99301"
  Zipcodes = re.findall('[0-9]+', zipcode_input)
  ###
  
  # if the zipcodes list is empty.. No user entry... Then set national zipcode as default
  if (len(Zipcodes) < 1):
      Zipcodes = ['National'] # this zipcode for national/.. We have to update data as well.
      index = df['Zip_Code'] == str(Zipcodes[0])
      zip_filtered = df[index]
  else:
      for a in range(len(Zipcodes)):
    #print(a)
          Zipcodes[a] = sortnotfoundzipCode(int(Zipcodes[a]))


  index = df['Zip_Code'] == str(Zipcodes[0])
  zip_filtered = df[index]
#print('debugger')
# if we have multiple zipcodes then append to the results

  if (len(Zipcodes)>1):
  #print('debugger') 
      for a in range(1,len(Zipcodes)):
    #print('debugger')
          index = df['Zip_Code'] == str(Zipcodes[a])
    #print(Zipcodes[a])  
    #print(len(df[index]))
          temp = df[index]
          #print('a')
          zip_filtered.append(temp)
  
  
  ## #
  
  import sys
  #fund_desc = "my company would require a funding amount of $2000 to $500000"
#fund_desc = "my company would require a funding amount of  "
  fund_req = re.findall('[0-9]+', fund_desc)

  if len(fund_req) == 0:
      
      min_req = 0
      #max_req = sys.maxsize # if the user enters only details without requirements of fund
      max_req = 100000
  elif len(fund_req) == 1:
      max_req = int(fund_req[0]) # if enters only single amount.. considering that as max requiremenmts by default..

  #TODO: we can try to handel this as special case in future.. using NLP to find either it is min or max requirement.
      min_req = 0
  else:
      min_req = int(fund_req[0])
      max_req = int(fund_req[1])
      
# index = ((zip_filtered['min funding'] >= min_req) & (zip_filtered['max funding'] >= min_req) )
# index = ((zip_filtered['max funding']) >= min_req)
# this needs discussion
# TODO: how to handle the cases here.. I think we have to ask for single input for funding only!!!
# i am not sure.. As there is a lot of ambiguity if we ask for min and max funding requirements in filtering
  index = ((zip_filtered['max_funding']) >= max_req)
  fund_filtered = zip_filtered[index]
  #fund_filtered      
  #print(str(len(fund_filtered[0])))
  #print(str(len(fund_filtered[0])))

# TODO we have to change the code which we return here... 
  # for testing pourpose returning the length.. @michael work on returning the data frame here
  #return 'umar testing the code'
  #result = fund_filtered.iloc[0]
  
  
  if('Minorities' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("Minorities")]
      
  if('Veterans' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("Veterans")]
      
  if('Disabilities' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("Disabilities")]
      
  if('Women' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("Women")]
      
  if('American Indian' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("American Indian")]
      
  if('Economically Disadvantaged' in fund_desc):
      fund_filtered = fund_filtered[fund_filtered['Targeted_Applicants'].str.contains("Economically Disadvantaged")]
      
      
  #my_objects  = fund_filtered.to_dict(orient='dict')
  #my_objects = [fund_filtered.columns.values.tolist()] + fund_filtered.values.tolist()
  my_objects = fund_filtered.values.tolist()
  #my_objects  = fund_filtered
 #return fund_filtered.to_html(index_names='false', justify='center', render_links='true')
  return render_template('results.html', my_objects=my_objects)
  #return render_template('contact.html')
  #return my_tuple
  
  
#def findZipCode(x):
  #print(df[df['Zip Code'].astype(str).str.contains(x)])
  
def sortnotfoundzipCode(zipcode):
  if (zipcode>=99500 and zipcode<=99999):#Alaska
    return 99504
  elif (zipcode>=96700 and zipcode<=96899):#Hawaii
    return 96797
  elif (zipcode>=90000 and zipcode<=96199):#California
    return 90011
  elif (zipcode>=97000 and zipcode<=97999):#Oregon
    return 97006
  elif (zipcode>=98000 and zipcode<=99499):#Washington
    return 99301
  elif (zipcode>=83200 and zipcode<=83999):#Idaho
    return 83949
  elif (zipcode>=88900 and zipcode<=89999):#Nevada
    return 89108
  elif (zipcode>=85000 and zipcode<=86999):#Arizona
    return 85364
  elif (zipcode>=84000 and zipcode<=84999):#Utah
    return 84111
  elif (zipcode>=82000 and zipcode<=83199):#Wyoming
    return 82001
  elif (zipcode>=59000 and zipcode<=59999):#Montana
    return 59901
  elif (zipcode>=58000 and zipcode<=58999):#North Dakota
    return 58103
  elif (zipcode>=57000 and zipcode<=57999):#South Dakota
    return 57106
  elif (zipcode>=68000 and zipcode<=69999):#Nebraska
    return 68516
  elif (zipcode>=66000 and zipcode<=67999):#Kansas
    return 66062
  elif (zipcode>=73000 and zipcode<=74999):#Oklahoma
    return 73099
  elif (zipcode>=75000 and zipcode<=79999):#Texas
    return 77449
  elif (zipcode>=70000 and zipcode<=71599):#Louisiana
    return 70726
  elif (zipcode>=71600 and zipcode<=72999):#Arkansas
    return 72401
  elif (zipcode>=63000 and zipcode<=65999):#Missouri
    return 63376
  elif (zipcode>=50000 and zipcode<=52999):#Iowa
    return 50613
  elif (zipcode>=55000 and zipcode<=56799):#Minnesota
    return 55106
  elif (zipcode>=53000 and zipcode<=54999):#Wisconsin
    return 53703
  elif (zipcode>=60000 and zipcode<=62999):#Illinois
    return 60629
  elif (zipcode>=40000 and zipcode<=42999):#Kentucky
    return 40475
  elif (zipcode>=37000 and zipcode<=38599):#Tennessee
    return 37013
  elif (zipcode>=38600 and zipcode<=39799):#Mississippi
    return 39503
  elif (zipcode>=35000 and zipcode<=36999):#Alabama
    return 35242
  elif (zipcode>=30000 and zipcode<=31999):#Georgia
    return 30043
  elif (zipcode>=39800 and zipcode<=39999):#Georgia
    return 30043
  elif (zipcode>=32000 and zipcode<=34999):#Florida
    return 33012
  elif (zipcode>=29000 and zipcode<=29999):#South Carolina
    return 29483
  elif (zipcode>=27000 and zipcode<=28999):#North Carolina
    return 28269
  elif (zipcode>=20100 and zipcode<=20199):#Virginia
    return 23219
  elif (zipcode>=22000 and zipcode<=24699):#Virginia
    return 23219
  elif (zipcode>=24700 and zipcode<=26999):#West Virginia
    return 25301
  elif (zipcode>=20600 and zipcode<=21999):#Maryland
    return 20906
  elif (zipcode>=19700 and zipcode<=19999):#Delaware
    return 19720
  elif (zipcode>=15000 and zipcode<=19699):#Pennsylvania
    return 19120
  elif (zipcode>=7000 and zipcode<=8999):#New Jersey
    return 8701
  elif (zipcode>=10000 and zipcode<=14999):#New York
    return 11368
  elif (zipcode>=6000 and zipcode<=6999):#Connecticut
    return 6902
  elif (zipcode>=2800 and zipcode<=2999):#Rhode Island
    return 2860
  elif (zipcode>=1000 and zipcode<=2799):#Massachusetts
    return 2301
  elif (zipcode>=5000 and zipcode<=5999):#Vermont
    return 5602
  elif (zipcode>=3000 and zipcode<=3899):#New Hampshire
    return 3103
  elif (zipcode>=3900 and zipcode<=4999):#Maine
    return 4401
  elif (zipcode>=600 and zipcode<=999):#Puerto Rico
    return 913
  elif (zipcode>=20000 and zipcode<=20099):#District of Columbia
    return 20011
  else:
    return 00000



## @umar added code ends here
if __name__ == '__main__':
    app.run(debug=True)