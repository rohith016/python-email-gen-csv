import requests
import csv
import time
import re

def generate_email_csv(input_file_path):
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
                    url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key=aa2dd96dd3108bdb40d01d366e767af438cc17d3"
                    response = requests.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        # process the data as needed
                    else:
                        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key=aa2dd96dd3108bdb40d01d366e767af438cc17d3"
                        response = requests.get(url)
                        if response.status_code == 200:
                            data = response.json()
                            # process the data as needed
                        # else:
                        #     print(f"Request failed with status code 1 : {response.status_code}")
                        #     continue
                elif domain:
                    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key=aa2dd96dd3108bdb40d01d366e767af438cc17d3"
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
    input_file_path = "CEO_Name_and_Linkedin.csv"
    generate_email_csv(input_file_path)
    # result = extract_name("VedaOils - Company Profile")
    # print(result)
    # dataNew = {
    #     "data": {
    #         "first_name": "Alexis",
    #         "last_name": "Ohanian",
    #         "email": "alexis@reddit.com",
    #         "score": 92,
    #         "domain": "reddit.com",
    #         "accept_all": True,
    #         "position": "Designer",
    #         "twitter": "null",
    #         "linkedin_url": "null",
    #         "phone_number": "null",
    #         "company": "Reddit",
    #         "sources": [
    #             {
    #                 "domain": "hunter.io",
    #                 "uri": "http://hunter.io/api",
    #                 "extracted_on": "2023-08-14",
    #                 "last_seen_on": "2023-08-23",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.com",
    #                 "uri": "http://redditblog.blogspot.com/2008/10",
    #                 "extracted_on": "2023-07-16",
    #                 "last_seen_on": "2023-07-16",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "hunter.io",
    #                 "uri": "http://hunter.io/fr/api/email-finder",
    #                 "extracted_on": "2023-05-21",
    #                 "last_seen_on": "2023-07-27",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "hunter.io",
    #                 "uri": "http://hunter.io/api/v2/docs",
    #                 "extracted_on": "2023-05-14",
    #                 "last_seen_on": "2023-08-15",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.com",
    #                 "uri": "http://redditblog.blogspot.com/2008_10_01_archive.html",
    #                 "extracted_on": "2023-05-11",
    #                 "last_seen_on": "2023-08-11",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "hunter.io",
    #                 "uri": "http://hunter.io/api/email-finder",
    #                 "extracted_on": "2022-06-18",
    #                 "last_seen_on": "2023-08-23",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "hunter.io",
    #                 "uri": "http://hunter.io/api-documentation/v2",
    #                 "extracted_on": "2022-03-17",
    #                 "last_seen_on": "2023-08-23",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.com",
    #                 "uri": "http://redditblog.blogspot.com/2008",
    #                 "extracted_on": "2021-08-07",
    #                 "last_seen_on": "2023-08-07",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.com",
    #                 "uri": "http://redditblog.blogspot.com/2008/12",
    #                 "extracted_on": "2020-01-12",
    #                 "last_seen_on": "2023-07-17",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.com",
    #                 "uri": "http://redditblog.blogspot.com/2007/10",
    #                 "extracted_on": "2019-10-13",
    #                 "last_seen_on": "2023-07-19",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com",
    #                 "uri": "http://reddit.blogspot.com/2008/10",
    #                 "extracted_on": "2018-12-24",
    #                 "last_seen_on": "2023-07-13",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com",
    #                 "uri": "http://reddit.blogspot.com/2007/08",
    #                 "extracted_on": "2018-11-02",
    #                 "last_seen_on": "2023-07-13",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com",
    #                 "uri": "http://reddit.blogspot.com/2007/10",
    #                 "extracted_on": "2018-11-02",
    #                 "last_seen_on": "2023-07-15",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com",
    #                 "uri": "http://reddit.blogspot.com/2008",
    #                 "extracted_on": "2018-11-02",
    #                 "last_seen_on": "2023-07-13",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com",
    #                 "uri": "http://reddit.blogspot.com/2008/06",
    #                 "extracted_on": "2018-09-02",
    #                 "last_seen_on": "2023-07-13",
    #                 "still_on_page": True
    #             },
    #             {
    #                 "domain": "whouses.io",
    #                 "uri": "http://whouses.io/domains/reddit.com/contacts",
    #                 "extracted_on": "2020-03-14",
    #                 "last_seen_on": "2020-06-14",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.com",
    #                 "uri": "http://redditblog.com/2007/10/20/draw-the-alien-get-24hrs-of-quasi-fame",
    #                 "extracted_on": "2018-10-19",
    #                 "last_seen_on": "2021-08-12",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.com",
    #                 "uri": "http://redditblog.com/2008/10/22/widgets-get-an-upgrade-and-a-firefox-extension-that-will-rock-your-world",
    #                 "extracted_on": "2018-10-19",
    #                 "last_seen_on": "2021-08-12",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.fr",
    #                 "uri": "http://redditblog.blogspot.fr/2007",
    #                 "extracted_on": "2017-09-21",
    #                 "last_seen_on": "2019-05-10",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.blogspot.fr",
    #                 "uri": "http://redditblog.blogspot.fr/2008",
    #                 "extracted_on": "2017-09-21",
    #                 "last_seen_on": "2019-05-07",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com.tr",
    #                 "uri": "http://reddit.blogspot.com.tr/2007_08_01_archive.html",
    #                 "extracted_on": "2017-09-20",
    #                 "last_seen_on": "2019-02-23",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.com.tr",
    #                 "uri": "http://reddit.blogspot.com.tr/2008_06_01_archive.html",
    #                 "extracted_on": "2017-08-26",
    #                 "last_seen_on": "2019-05-07",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.fr",
    #                 "uri": "http://reddit.blogspot.fr/2008/06/we-have-winner.html",
    #                 "extracted_on": "2017-07-12",
    #                 "last_seen_on": "2019-05-14",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.fr",
    #                 "uri": "http://reddit.blogspot.fr/2008/10/aliens-invading-ars-technica.html",
    #                 "extracted_on": "2017-05-29",
    #                 "last_seen_on": "2019-05-23",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.fr",
    #                 "uri": "http://reddit.blogspot.fr/2007/08/save-our-earth-and-drink-fiji-bottled.html",
    #                 "extracted_on": "2017-05-27",
    #                 "last_seen_on": "2019-05-23",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.fr",
    #                 "uri": "http://reddit.blogspot.fr/2008/10/will-real-reddit-please-stand-up.html",
    #                 "extracted_on": "2017-05-04",
    #                 "last_seen_on": "2019-05-04",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.com",
    #                 "uri": "http://redditblog.com/2008/12/01/vector-art-really-is-a-limiting-medium-for-reddit-alien-creation",
    #                 "extracted_on": "2016-10-25",
    #                 "last_seen_on": "2021-08-12",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "reddit.blogspot.fr",
    #                 "uri": "http://reddit.blogspot.fr/2007_08_01_archive.html",
    #                 "extracted_on": "2016-03-31",
    #                 "last_seen_on": "2019-05-10",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.com",
    #                 "uri": "http://redditblog.com/2007_10_01_archive.html",
    #                 "extracted_on": "2015-06-24",
    #                 "last_seen_on": "2016-06-11",
    #                 "still_on_page": False
    #             },
    #             {
    #                 "domain": "redditblog.com",
    #                 "uri": "http://redditblog.com/2008_12_01_archive.html",
    #                 "extracted_on": "2015-06-24",
    #                 "last_seen_on": "2016-06-07",
    #                 "still_on_page": False
    #             }
    #         ],
    #         "verification": {
    #             "date": "null",
    #             "status": "accept_all"
    #         }
    #     },
    #     "meta": {
    #         "params": {
    #             "first_name": "Alexis",
    #             "last_name": "Ohanian",
    #             "full_name": "null",
    #             "domain": "reddit.com",
    #             "company": "null",
    #             "max_duration": "null"
    #         }
    #     }
    # }

    # data = {
    #     "data": {
    #         "domain": "stripe.com",
    #         "disposable": False,
    #         "webmail": False,
    #         "accept_all": True,
    #         "pattern": "{first}",
    #         "organization": "Stripe",
    #         "description": "Stripe is a suite of APIs powering online payment processing and commerce solutions for internet businesses of all sizes. Accept payments and scale faster.",
    #         "industry": "Technology",
    #         "twitter": "https://twitter.com/stripe",
    #         "facebook": "https://facebook.com/175383762511776",
    #         "linkedin": "https://linkedin.com/company/stripe",
    #         "instagram": "null",
    #         "youtube": "https://youtube.com/stripe",
    #         "technologies": [
    #             "google-analytics",
    #             "google-tag-manager",
    #             "mixpanel",
    #             "nginx",
    #             "opencart",
    #             "php",
    #             "sentry",
    #             "shopify",
    #             "squarespace",
    #             "stripe",
    #             "twitter",
    #             "uservoice",
    #             "woocommerce",
    #             "wordpress"
    #         ],
    #         "country": "US",
    #         "state": "OR",
    #         "city": "null",
    #         "postal_code": "97712",
    #         "street": "1234) 27 Fredrick Ave",
    #         "emails": [
    #             {
    #                 "value": "karla@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "karla.io",
    #                         "uri": "http://karla.io/files/ichthyology-slides.pdf",
    #                         "extracted_on": "2023-05-23",
    #                         "last_seen_on": "2023-08-23",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "karla.io",
    #                         "uri": "http://karla.io/files/ichthyology-wp.pdf",
    #                         "extracted_on": "2023-05-23",
    #                         "last_seen_on": "2023-08-23",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "pdfslide.us",
    #                         "uri": "http://pdfslide.us/documents/characiformes-characidae-neotropical-ichthyology-162-e170073-2018.html",
    #                         "extracted_on": "2022-12-01",
    #                         "last_seen_on": "2023-08-29",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "pdfslide.us",
    #                         "uri": "http://pdfslide.us/documents/lake-malawi-fisheries-management-symposium-department-of-ichthyology-and-fisheries.html",
    #                         "extracted_on": "2022-11-28",
    #                         "last_seen_on": "2023-08-30",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "pdfslide.net",
    #                         "uri": "http://pdfslide.net/documents/ichthyology-phishing-as-a-science-black-hat-home-ichthyology-phishing.html",
    #                         "extracted_on": "2022-03-14",
    #                         "last_seen_on": "2023-06-22",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "pdfslide.us",
    #                         "uri": "http://pdfslide.us/documents/ichthyology-phishing-as-a-science-black-hat-home-ichthyology-phishing.html",
    #                         "extracted_on": "2021-07-28",
    #                         "last_seen_on": "2023-08-25",
    #                         "still_on_page": True
    #                     }
    #                 ],
    #                 "first_name": "Karla",
    #                 "last_name": "Burnett",
    #                 "position": "Security Engineer",
    #                 "seniority": "null",
    #                 "department": "it",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-21",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "sana@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "dev.auth0.com",
    #                         "uri": "http://dev.auth0.com/blog/jp-auth0-circleci-and-stripe-launch-go-saas-program-in-japan",
    #                         "extracted_on": "2023-04-10",
    #                         "last_seen_on": "2023-07-10",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "prtimes.jp",
    #                         "uri": "http://prtimes.jp/main/html/rd/p/000000003.000044999.html",
    #                         "extracted_on": "2020-04-24",
    #                         "last_seen_on": "2023-04-03",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "prtimes.jp",
    #                         "uri": "http://prtimes.jp/main/html/rd/p/000000006.000044999.html",
    #                         "extracted_on": "2019-12-26",
    #                         "last_seen_on": "2023-07-30",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "auth0.com",
    #                         "uri": "http://auth0.com/blog/jp-auth0-circleci-and-stripe-launch-go-saas-program-in-japan",
    #                         "extracted_on": "2019-07-18",
    #                         "last_seen_on": "2023-08-11",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "tv.prtimes.jp",
    #                         "uri": "http://tv.prtimes.jp/main/html/rd/p/000000006.000044999.html",
    #                         "extracted_on": "2019-12-25",
    #                         "last_seen_on": "2019-12-25",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "static-staging.circleci.com",
    #                         "uri": "http://static-staging.circleci.com/blog/auth0-circleci-and-stripe-launch-go-saas-supporting-growth-of-japan-s-subscription-sector",
    #                         "extracted_on": "2019-11-18",
    #                         "last_seen_on": "2021-01-14",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "jumpstartmag.com",
    #                         "uri": "http://jumpstartmag.com/stripe-launches-in-malaysia",
    #                         "extracted_on": "2019-11-16",
    #                         "last_seen_on": "2020-05-18",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "circleci.com",
    #                         "uri": "http://circleci.com/blog/auth0-circleci-and-stripe-launch-go-saas-supporting-growth-of-japan-s-subscription-sector",
    #                         "extracted_on": "2019-07-01",
    #                         "last_seen_on": "2022-04-29",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "re-how.net",
    #                         "uri": "http://re-how.net/press_releases/30230",
    #                         "extracted_on": "2019-06-22",
    #                         "last_seen_on": "2020-07-01",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Sana",
    #                 "last_name": "Rahman",
    #                 "position": "Communications News",
    #                 "seniority": "senior",
    #                 "department": "communication",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-30",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "lisa@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "h1bdata.com",
    #                         "uri": "http://h1bdata.com/page/2",
    #                         "extracted_on": "2021-09-25",
    #                         "last_seen_on": "2023-06-25",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "h1bdata.com",
    #                         "uri": "http://h1bdata.com",
    #                         "extracted_on": "2021-08-21",
    #                         "last_seen_on": "2023-07-17",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "fish4.co.uk",
    #                         "uri": "http://fish4.co.uk/job/8285816/emea-marketing-lead",
    #                         "extracted_on": "2019-01-25",
    #                         "last_seen_on": "2023-07-27",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "fish4.co.uk",
    #                         "uri": "http://fish4.co.uk/job/8355982/financial-partnerships-europe-partner-manager",
    #                         "extracted_on": "2018-12-20",
    #                         "last_seen_on": "2023-07-17",
    #                         "still_on_page": True
    #                     }
    #                 ],
    #                 "first_name": "Lisa",
    #                 "last_name": "Zieger",
    #                 "position": "Immigration Specialist",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-21",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "edwin@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "hackernews.ryansolid.workers.dev",
    #                         "uri": "http://hackernews.ryansolid.workers.dev/users/edwinwee",
    #                         "extracted_on": "2022-08-16",
    #                         "last_seen_on": "2023-08-26",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "betalist.com",
    #                         "uri": "http://betalist.com/@edwinwee",
    #                         "extracted_on": "2020-04-13",
    #                         "last_seen_on": "2023-07-14",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "llc-formation-services90112.verybigblog.com",
    #                         "uri": "http://llc-formation-services90112.verybigblog.com/2602328/the-5-second-trick-for-incorporation-services-for-startups",
    #                         "extracted_on": "2021-08-15",
    #                         "last_seen_on": "2023-05-30",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "thetopbusinessformationse56778.blogoscience.com",
    #                         "uri": "http://thetopbusinessformationse56778.blogoscience.com/3752573/about-clerky-reviews",
    #                         "extracted_on": "2021-04-26",
    #                         "last_seen_on": "2021-09-27",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nomadlist.com",
    #                         "uri": "http://nomadlist.com/@edwin778",
    #                         "extracted_on": "2020-07-04",
    #                         "last_seen_on": "2023-04-09",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nomadlist.com",
    #                         "uri": "http://nomadlist.com/@niv",
    #                         "extracted_on": "2019-06-03",
    #                         "last_seen_on": "2019-06-03",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nomadlist.com",
    #                         "uri": "http://nomadlist.com/@bentossell",
    #                         "extracted_on": "2019-06-02",
    #                         "last_seen_on": "2019-06-02",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nomadlist.com",
    #                         "uri": "http://nomadlist.com/@gabriel__lewis",
    #                         "extracted_on": "2019-05-14",
    #                         "last_seen_on": "2019-06-09",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nomadlist.com",
    #                         "uri": "http://nomadlist.com/@homsit",
    #                         "extracted_on": "2019-05-10",
    #                         "last_seen_on": "2019-05-10",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "hn.nuxtjs.org",
    #                         "uri": "http://hn.nuxtjs.org/item/18078640",
    #                         "extracted_on": "2019-01-30",
    #                         "last_seen_on": "2022-07-31",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "419v.com",
    #                         "uri": "http://419v.com/posts/stripe-connect-2",
    #                         "extracted_on": "2018-12-11",
    #                         "last_seen_on": "2019-03-11",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "viperhtml-164315.appspot.com",
    #                         "uri": "http://viperhtml-164315.appspot.com/item/18053297",
    #                         "extracted_on": "2018-09-24",
    #                         "last_seen_on": "2020-02-03",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "viperhtml-164315.appspot.com",
    #                         "uri": "http://viperhtml-164315.appspot.com/user/edwinwee",
    #                         "extracted_on": "2018-09-24",
    #                         "last_seen_on": "2019-08-03",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "assets.producthunt.com",
    #                         "uri": "http://assets.producthunt.com/posts/stripe-connect-2",
    #                         "extracted_on": "2018-03-19",
    #                         "last_seen_on": "2018-03-19",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "producthunt.com",
    #                         "uri": "http://producthunt.com/posts/stripe-connect-2",
    #                         "extracted_on": "2017-09-15",
    #                         "last_seen_on": "2021-01-15",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "producthunt-com-63333def4b09638c.sitemod.io",
    #                         "uri": "http://www-producthunt-com-63333def4b09638c.sitemod.io/posts/stripe-connect-2",
    #                         "extracted_on": "2017-07-04",
    #                         "last_seen_on": "2017-07-04",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Edwin",
    #                 "last_name": "Wee",
    #                 "position": "null",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "tara_seshan",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-09-05",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "govind.dandekar@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/es-419-se/blog/130-plus-currencies-in-canada",
    #                         "extracted_on": "2020-04-15",
    #                         "last_seen_on": "2023-07-25",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/au/blog/130-plus-currencies-in-canada",
    #                         "extracted_on": "2020-04-12",
    #                         "last_seen_on": "2023-07-26",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/blog/130-plus-currencies-in-canada",
    #                         "extracted_on": "2020-04-12",
    #                         "last_seen_on": "2023-07-01",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/it-ee/blog/130-plus-currencies-in-canada",
    #                         "extracted_on": "2020-03-05",
    #                         "last_seen_on": "2023-06-06",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/en-nl/blog/130-plus-currencies-in-canada",
    #                         "extracted_on": "2020-03-04",
    #                         "last_seen_on": "2023-06-13",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/7",
    #                         "extracted_on": "2019-01-25",
    #                         "last_seen_on": "2019-05-23",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/6",
    #                         "extracted_on": "2018-09-12",
    #                         "last_seen_on": "2018-09-19",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/4",
    #                         "extracted_on": "2017-12-15",
    #                         "last_seen_on": "2018-03-18",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/3",
    #                         "extracted_on": "2017-08-28",
    #                         "last_seen_on": "2017-11-21",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/2",
    #                         "extracted_on": "2017-06-29",
    #                         "last_seen_on": "2017-08-19",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Govind",
    #                 "last_name": "Dandekar",
    #                 "position": "null",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-07-03",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "charles.francis@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/it-fr/blog/get-ready-for-apple-pay-on-the-web",
    #                         "extracted_on": "2020-04-16",
    #                         "last_seen_on": "2023-07-24",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/es-419-it/blog/get-ready-for-apple-pay-on-the-web",
    #                         "extracted_on": "2020-04-15",
    #                         "last_seen_on": "2023-07-21",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/fr-sg/blog/get-ready-for-apple-pay-on-the-web",
    #                         "extracted_on": "2020-04-15",
    #                         "last_seen_on": "2023-07-28",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/au/blog/get-ready-for-apple-pay-on-the-web",
    #                         "extracted_on": "2020-04-12",
    #                         "last_seen_on": "2023-07-17",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "stripe.com",
    #                         "uri": "http://stripe.com/blog/get-ready-for-apple-pay-on-the-web",
    #                         "extracted_on": "2020-04-12",
    #                         "last_seen_on": "2023-07-20",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/4",
    #                         "extracted_on": "2017-06-29",
    #                         "last_seen_on": "2017-09-12",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/3",
    #                         "extracted_on": "2017-03-31",
    #                         "last_seen_on": "2017-06-02",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/2",
    #                         "extracted_on": "2016-11-22",
    #                         "last_seen_on": "2017-03-21",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog",
    #                         "extracted_on": "2016-10-05",
    #                         "last_seen_on": "2016-10-05",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "uploads.stripe.com",
    #                         "uri": "http://uploads.stripe.com/blog/page/1",
    #                         "extracted_on": "2016-09-16",
    #                         "last_seen_on": "2016-10-05",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Charles",
    #                 "last_name": "Francis",
    #                 "position": "null",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-06-18",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "carl@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "blog.carlmjohnson.net",
    #                         "uri": "http://blog.carlmjohnson.net/post/2016-11-27-how-to-use-go-generate",
    #                         "extracted_on": "2016-12-02",
    #                         "last_seen_on": "2023-06-27",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "go.googlesource.com",
    #                         "uri": "http://go.googlesource.com/crypto",
    #                         "extracted_on": "2016-03-25",
    #                         "last_seen_on": "2016-04-14",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "golang.org",
    #                         "uri": "http://golang.org/contributors",
    #                         "extracted_on": "2016-03-24",
    #                         "last_seen_on": "2016-07-21",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Carl",
    #                 "last_name": "Chatfield",
    #                 "position": "null",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-21",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "ludwig@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "dribbble.com",
    #                         "uri": "http://dribbble.com/shots/1197960-stripe-in-the-uk",
    #                         "extracted_on": "2017-07-21",
    #                         "last_seen_on": "2023-08-07",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "dribbble.com",
    #                         "uri": "http://dribbble.com/shots/581096-einhorn",
    #                         "extracted_on": "2016-12-12",
    #                         "last_seen_on": "2023-08-16",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "dribbble.com",
    #                         "uri": "http://dribbble.com/shots/736405-Stripe-Teams",
    #                         "extracted_on": "2015-05-06",
    #                         "last_seen_on": "2023-06-25",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "dribbble.com",
    #                         "uri": "http://dribbble.com/shots/736405-stripe-teams",
    #                         "extracted_on": "2014-04-21",
    #                         "last_seen_on": "2023-06-25",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "dribbble.com",
    #                         "uri": "http://dribbble.com/shots/736410-stripe-in-canada",
    #                         "extracted_on": "2014-04-18",
    #                         "last_seen_on": "2023-07-24",
    #                         "still_on_page": True
    #                     }
    #                 ],
    #                 "first_name": "Ludwig",
    #                 "last_name": "Pettersson",
    #                 "position": "Graphic Design",
    #                 "seniority": "null",
    #                 "department": "design",
    #                 "linkedin": "null",
    #                 "twitter": "ludwig",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-15",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "patrick@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 94,
    #                 "sources": [
    #                     {
    #                         "domain": "recap.app",
    #                         "uri": "http://recap.app/patrick-collison",
    #                         "extracted_on": "2023-09-05",
    #                         "last_seen_on": "2023-09-05",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "listofceo.com",
    #                         "uri": "http://listofceo.com/fintech/stripe-ceo-email-net-worth-patrick-collison",
    #                         "extracted_on": "2023-08-28",
    #                         "last_seen_on": "2023-08-28",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "hunter.io",
    #                         "uri": "http://hunter.io/api-documentation/v2",
    #                         "extracted_on": "2023-07-13",
    #                         "last_seen_on": "2023-08-23",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "hunter.io",
    #                         "uri": "http://hunter.io/api/email-verifier",
    #                         "extracted_on": "2023-07-13",
    #                         "last_seen_on": "2023-08-23",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "hunter.io",
    #                         "uri": "http://hunter.io/api",
    #                         "extracted_on": "2023-04-24",
    #                         "last_seen_on": "2023-08-23",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "icloudnewz.blogspot.com",
    #                         "uri": "http://icloudnewz.blogspot.com/2017/11/follow-patrick-collison-mike-birbiglia.html",
    #                         "extracted_on": "2020-03-25",
    #                         "last_seen_on": "2023-07-12",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "icloudnewz.blogspot.com",
    #                         "uri": "http://icloudnewz.blogspot.com/2018/03/follow-nathan-hubbard-josh-elman-and.html",
    #                         "extracted_on": "2020-03-25",
    #                         "last_seen_on": "2023-06-30",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "icloudnewz.blogspot.com",
    #                         "uri": "http://icloudnewz.blogspot.com/2017/12/follow-nathan-hubbard-josh-elman-and.html",
    #                         "extracted_on": "2019-11-30",
    #                         "last_seen_on": "2023-07-09",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "icloudnewz.blogspot.com",
    #                         "uri": "http://icloudnewz.blogspot.com/2018/01/follow-nathan-hubbard-josh-elman-and.html",
    #                         "extracted_on": "2019-11-30",
    #                         "last_seen_on": "2023-07-14",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "icloudnewz.blogspot.com",
    #                         "uri": "http://icloudnewz.blogspot.com/2018/02/follow-patrick-collison-mike-birbiglia.html",
    #                         "extracted_on": "2019-11-30",
    #                         "last_seen_on": "2023-07-09",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "microconf.gen.co",
    #                         "uri": "http://microconf.gen.co/patrick-collison",
    #                         "extracted_on": "2019-01-07",
    #                         "last_seen_on": "2023-06-29",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "github.com",
    #                         "uri": "http://github.com/stripe/stripe-python/blob/master/stripe/__init__.py",
    #                         "extracted_on": "2017-09-30",
    #                         "last_seen_on": "2022-12-20",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "patrickcollison.com",
    #                         "uri": "http://patrickcollison.com/bookshelf",
    #                         "extracted_on": "2016-02-11",
    #                         "last_seen_on": "2023-08-16",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "patrickcollison.com",
    #                         "uri": "http://patrickcollison.com/svhistory",
    #                         "extracted_on": "2015-10-13",
    #                         "last_seen_on": "2023-07-20",
    #                         "still_on_page": True
    #                     },
    #                     {
    #                         "domain": "nutter.life",
    #                         "uri": "http://nutter.life/patrickc",
    #                         "extracted_on": "2022-06-04",
    #                         "last_seen_on": "2022-06-04",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nitter.poast.org",
    #                         "uri": "http://nitter.poast.org/patrickc",
    #                         "extracted_on": "2022-01-21",
    #                         "last_seen_on": "2022-07-21",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nitter.moooi.jp",
    #                         "uri": "http://nitter.moooi.jp/patrickc",
    #                         "extracted_on": "2021-07-12",
    #                         "last_seen_on": "2022-07-12",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nitter.fdn.fr",
    #                         "uri": "http://nitter.fdn.fr/patrickc",
    #                         "extracted_on": "2021-06-08",
    #                         "last_seen_on": "2023-03-09",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "nitter.securitypraxis.eu",
    #                         "uri": "http://nitter.securitypraxis.eu/patrickc",
    #                         "extracted_on": "2021-06-07",
    #                         "last_seen_on": "2021-06-07",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "bird.trom.tf",
    #                         "uri": "http://bird.trom.tf/patrickc",
    #                         "extracted_on": "2021-06-05",
    #                         "last_seen_on": "2022-06-07",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "beta.paganresearch.io",
    #                         "uri": "http://beta.paganresearch.io/details/stripe",
    #                         "extracted_on": "2020-06-17",
    #                         "last_seen_on": "2021-01-16",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "peerreach.com",
    #                         "uri": "http://peerreach.com/patrickc",
    #                         "extracted_on": "2019-11-07",
    #                         "last_seen_on": "2021-01-21",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "apify.com",
    #                         "uri": "http://apify.com/vdrmota/twitter-scraper",
    #                         "extracted_on": "2019-08-28",
    #                         "last_seen_on": "2021-01-13",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "paganresearch.io",
    #                         "uri": "http://paganresearch.io/details/stripe",
    #                         "extracted_on": "2019-05-08",
    #                         "last_seen_on": "2021-02-08",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "indiehackers.com",
    #                         "uri": "http://indiehackers.com/forum/stripe-forum-e701f4b334",
    #                         "extracted_on": "2018-12-25",
    #                         "last_seen_on": "2018-12-25",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "patrickcollison.com",
    #                         "uri": "http://patrickcollison.com/culture",
    #                         "extracted_on": "2018-09-13",
    #                         "last_seen_on": "2018-11-09",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "medium.com",
    #                         "uri": "http://medium.com/cs183c-blitzscaling-class-collection/cs183c-session-11-patrick-collison-stripe-84057f358ecb",
    #                         "extracted_on": "2017-09-05",
    #                         "last_seen_on": "2021-08-27",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "fetch.amplemarket.com",
    #                         "uri": "http://fetch.amplemarket.com/midas",
    #                         "extracted_on": "2017-08-30",
    #                         "last_seen_on": "2023-04-25",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "venturenews.co",
    #                         "uri": "http://venturenews.co",
    #                         "extracted_on": "2017-08-10",
    #                         "last_seen_on": "2017-08-10",
    #                         "still_on_page": False
    #                     },
    #                     {
    #                         "domain": "github.com",
    #                         "uri": "http://github.com/stripe/stripe-python/commit/40814b421daf66ca45ff44af3cde00ede4e2ee13",
    #                         "extracted_on": "2016-11-01",
    #                         "last_seen_on": "2018-02-25",
    #                         "still_on_page": False
    #                     }
    #                 ],
    #                 "first_name": "Patrick",
    #                 "last_name": "Collison",
    #                 "position": "CEO",
    #                 "seniority": "executive",
    #                 "department": "executive",
    #                 "linkedin": "https://www.linkedin.com/in/johnbcollison/",
    #                 "twitter": "patrickc",
    #                 "phone_number": "+1 301 322 2777",
    #                 "verification": {
    #                     "date": "2023-09-05",
    #                     "status": "accept_all"
    #                 }
    #             },
    #             {
    #                 "value": "anamaria@stripe.com",
    #                 "type": "personal",
    #                 "confidence": 93,
    #                 "sources": [
    #                     {
    #                         "domain": "siepr.stanford.edu",
    #                         "uri": "http://siepr.stanford.edu/research/projects/stanford-stripe-study-internet-entrepreneurship",
    #                         "extracted_on": "2023-01-08",
    #                         "last_seen_on": "2023-07-09",
    #                         "still_on_page": True
    #                     }
    #                 ],
    #                 "first_name": "Anamaria",
    #                 "last_name": "Mocanu",
    #                 "position": "null",
    #                 "seniority": "null",
    #                 "department": "null",
    #                 "linkedin": "null",
    #                 "twitter": "null",
    #                 "phone_number": "null",
    #                 "verification": {
    #                     "date": "2023-08-28",
    #                     "status": "accept_all"
    #                 }
    #             }
    #         ],
    #         "linked_domains": []
    #     },
    #     "meta": {
    #         "results": 252,
    #         "limit": 10,
    #         "offset": 0,
    #         "params": {
    #             "domain": "stripe.com",
    #             "company": "null",
    #             "type": "null",
    #             "seniority": "null",
    #             "department": "null"
    #         }
    #     }
    # }
    # result = get_email_data(data)   
    # print("get_email_data : ", result)
    