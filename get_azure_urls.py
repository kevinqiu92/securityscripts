#!/usr/bin/env python
import adal, requests, json, yaml, lxml, sys, os, base64
import xml.etree.ElementTree as ET
from urlparse import urljoin

TENANT_ID = os.environ['TENANT_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
AUTHENTICATION_ENDPOINT = "https://login.microsoftonline.com/"
AUTHENTICATION_RESOURCE = "https://management.core.windows.net/"
SUBSCRIPTIONS_URL = "https://management.azure.com/subscriptions?api-version=2014-04-01"
RESOURCE = "https://management.azure.com/"
CLASSIC_API = "https://management.core.windows.net/"
certificate_path = "PATH TO CERTIFICATE FOR CLASSIC API"

data = {"grant_type" : "client_credentials", "client_id" : CLIENT_ID, "client_secret" : CLIENT_SECRET, "resource" : RESOURCE}
headers = {"Content-Type" : "application/x-www-form-urlencoded"}

azure_urls = []

# store all the azure domains in a file
url_file = open("FILE TO WRITE TO", "w")

# get an azure access token for non vault stuff
r = requests.post("https://login.windows.net/{}/oauth2/token".format(TENANT_ID), data=data, headers=headers)
access_token = r.json()['access_token']

# get all domains associated with Azure
headers2 = {"Authorization" : "Bearer " + access_token}
r2 = requests.get(SUBSCRIPTIONS_URL, headers=headers2)
sub_json = r2.json()["value"]
for subscription in sub_json:
    subscription_id = subscription["id"]

    # get all hostnames associated with azure web apps
    web_app_url = RESOURCE + subscription_id + "/providers/Microsoft.Web/sites?api-version=2016-08-01"
    try:
        r3 = requests.get(web_app_url, headers=headers2)
        sub_web_apps = r3.json()["value"]
        for web_app in sub_web_apps:
            hostNames = web_app["properties"]["hostNames"]
            for hostName in hostNames:
                url_file.write(hostName + "\n")
                azure_urls.append(hostName)

            try:
                slots_url = RESOURCE + web_app["id"] + "/slots?api-version=2016-08-01"
                r5 = requests.get(slots_url, headers=headers2)
                slots_json = r5.json()["value"]
                for slot in slots_json:
                    for hostName in slot["properties"]["hostNames"]:
                        if hostName not in azure_urls:
                            url_file.write(hostName + "\n")
                            azure_urls.append(hostName)
            except Exception as excpt:
                print("Exception: " + str(excpt) + " happened in slot checking for " + subscription_id)
                continue
    except Exception as excpt:
        print("Exception: " + str(excpt) + " happened in app service checking for " + subscription_id)
        continue

    # get all hostnames associated with app service environment apps
    app_service_env_url = RESOURCE + subscription_id + "/providers/Microsoft.Web/hostingEnvironments?api-version=2016-09-01"
    try:
        r4 = requests.get(app_service_env_url, headers=headers2)
        sub_ase = r4.json()["value"]
        for ase in sub_ase:
            ase_name = ase["name"]
            ase_apps_url = RESOURCE + subscription_id + "/resourceGroups/" + ase["properties"]["resourceGroup"] + "/providers/Microsoft.Web/hostingEnvironments/" + ase_name + "/sites?api-version=2016-09-01"
            r5 = requests.get(ase_apps_url, headers=headers2)
            ase_apps_json = r5.json()["value"]
            for ase_app in ase_apps_json:
                enabled_host_names = ase_app["properties"]["enabledHostNames"]
                for enabled_host_name in enabled_host_names:
                    if enabled_host_name not in azure_urls:
                        url_file.write(enabled_host_name + "\n")
                        azure_urls.append(enabled_host_name)
    except Exception as excpt:
        print("Exception: " + str(excpt) + " happened in ASE checking for " + subscription_id)
        continue

    # get all hostnames associated with cloud services
    subscription_id_alone = subscription_id[15:]
    headers4 = {"x-ms-version" : "2014-04-01"}
    try:
        r5 = requests.get(CLASSIC_API + subscription_id_alone + "/services/hostedservices", cert=certificate_path, headers=headers4)
        r5_response = r5.content
        tree = ET.fromstring(r5_response)
        for hosted_service in tree:
            for element in hosted_service:
                if element.tag == "{http://schemas.microsoft.com/windowsazure}ServiceName":
                    element_url = str(element.text).lower() + ".cloudapp.net"
                    if element_url not in azure_urls:
                        url_file.write(element_url + "\n")
                        azure_urls.append(element_url)
    except Exception as excpt:
        print("Exception: " + str(excpt) + " happened in cloud service checking for " + subscription_id)
        continue

    # now get all hostnames associated with a public ip
    public_ip_url = RESOURCE + subscription_id + "/providers/Microsoft.Network/publicIPAddresses?api-version=2016-09-01"
    try:
        r6 = requests.get(public_ip_url, headers=headers2)
        sub_public_ips = r6.json()["value"]
        for public_ip in sub_public_ips:
            if "fqdn" in str(public_ip):
                fqdn_url = public_ip["properties"]["dnsSettings"]["fqdn"]
                if fqdn_url not in azure_urls:
                    url_file.write(fqdn_url + "\n")
                    azure_urls.append(fqdn_url)
    except Exception as excpt:
        print("Exception: " + str(excpt) + " happened in public IP checking for " + subscription_id)
        continue

    # now get all hostnames associated with traffic manager profiles
    resource_group_url = RESOURCE + subscription_id + "/resourcegroups?api-version=2016-09-01"
    try:
        r3 = requests.get(resource_group_url, headers=headers2)
        resource_group_json = r3.json()["value"]
        for resource_group in resource_group_json:
            tm_profiles_url = RESOURCE + resource_group["id"] + "/providers/Microsoft.Network/trafficManagerProfiles?api-version=2015-11-01"
            r4 = requests.get(tm_profiles_url, headers=headers2)
            tm_json = r4.json()["value"]
            for tm in tm_json:
                fqdn_url = tm["properties"]["dnsConfig"]["fqdn"]
                if fqdn_url not in azure_urls:
                    url_file.write(fqdn_url + "\n")
                    azure_urls.append(fqdn_url)
    except Exception as excpt:
        print("Exception: " + str(excpt) + " happened in traffic manager profile checking for " + subscription_id)
        continue
