import requests
import csv
import time
import re
import json
import os
from dotenv import load_dotenv

def generate_email_csv(input_file_path, apiKey):
    results = []
    with open(input_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name_data = row['organicResults/0/title'] if row['organicResults/0/title'] and len(row['organicResults/0/title']) > 0 else None
            domain = row['Domain'] if row['Domain'] and len(row['Domain']) > 0 else None

            if name_data == None and domain == None:
                continue

            first_name, last_name = extract_name(name_data)
            # print("result :", first_name, last_name, domain)
            # continue

            if first_name == None and last_name == None and domain == None:
                continue

            try:
                
                data = None
                if first_name and last_name and domain:
                    url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key={apiKey}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        # process the data as needed
                    else:
                        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={apiKey}"
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            # process the data as needed
                        # else:
                        #     print(f"Request failed with status code 1 : {response.status_code}")
                        #     continue
                elif domain:
                    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={apiKey}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                    # else:
                    #     print(f"Request failed with status code 2: {response.status_code}")
                    #     continue

             
            
                if data != None:
                    email = get_email_data(data)
                    results.append([first_name, last_name, domain, email])
                else:
                    results.append([first_name, last_name, domain, None])


            except requests.HTTPError as http_err:
                print(f"HTTP error occurred for domain: {domain}. Error: {http_err}")
            except Exception as err:
                print(f"Other error occurred for domain: {domain}. Error: {err}")

    #  save th data to csv file
    output_file_path = 'ceo_emails.csv'
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['first name', 'last name', 'Domain','email'])
        writer.writerows(results)



# extract name from string
def extract_name(text):
    words = re.findall(r'^[\w\s]+', text)
    
    if not words:
        return None, None

    name_parts = words[0].split()

    if len(name_parts) == 2 or len(name_parts) > 2:
        return name_parts[0], name_parts[1]
    elif len(name_parts) == 1:
        return name_parts[0], None
    else:
        return None, None

# extract email from request response data
def get_email_data(data):
    if 'data' in data and 'email' in data['data']:
        return  data['data']['email']
    elif data['data']:
        emails_list = data['data'].get("emails", [])
        email_addresses = []
        if len(emails_list) > 0 :
            # return emails_list[0]['value']
            for email_data in emails_list:
                if email_data.get("value", None) != None:
                    email_addresses.append(email_data.get("value", None))

        if len(email_addresses) > 0:
            return '\n'.join(email_addresses)
        else:
            return None 

    else:
        return None
    
# start the script
if __name__ == "__main__":
    load_dotenv()
    apiKey = os.getenv("API_KEY")
    input_file_path = "CEO_Name_and_Linkedin.csv"
    result = generate_email_csv(input_file_path, apiKey)
    # with open('domain_search.json', 'r') as file:
    #     data = json.load(file)

    # print(data)


    # result = extract_name("VedaOils - Company Profile")
    # print(result)


    # result = get_email_data(data)   
    # print("get_email_data : ", result)
    