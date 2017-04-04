# securityscripts

This repo contains various scripts that I've written to assist me during work. 

get_azure_admins.ps1 - fetches a list of all azure admins for all your azure subscriptions and puts them in a separate text file for each subscription

get_azure_urls.py - fetches a list of all domain names in all azure subscriptions that are associated with app services (including slots), app service environments, cloud services, public IPs, and traffic manager profiles and saves it to a text file

get_nsg_rules.ps1 - creates a csv file containing a list of all NSG rules for all subscriptions in azure and includes the following fields: subscription, nsg, rule name, protocol, source port, destination port, source address, destination address, and direction

get_sql_server_firewall_rules.ps1 - creates a csv file with all azure sql firewall rules for all subscriptions. fields include: subscription, resource group, server name, start ip address, end ip address, firewall rule name

get_sql_servers.ps1 - creates a csv file with all azure sql servers and databases for all subscriptions. fields include: subscription, resource group, server name, database name
