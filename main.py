
# another crt.sh cli tool

import argparse
from bs4 import BeautifulSoup as bs4
import requests

    
def get_arguments():
    parser = argparse.ArgumentParser(description="searches subdomains from crt.sh")
    parser.add_argument("-i", "--identity", dest="identity", help="identity to search(domain name, company, etc.)")
    #parser.add_argument("-e", "--exclude-expired", dest="exclude_expired", action=argparse.BooleanOptionalAction)
    parser.add_argument("-o", "--output", dest="output_file", help='file to save output')
    args = parser.parse_args()
    return args


def save_output(output_file, subdomains_found):
    with open(user_arguments.output_file, 'w') as file:
        file.write('\n'.join(subdomains_found)+'\n')


def get_subdomains(identity):
    subdomains_found = []

    response = requests.get(url = 'https://crt.sh/?q=' + identity)
    soup = bs4(response.content, "html.parser")

    big_table = soup.find_all('table')[1]
    data_table = big_table.table
    tr_tags = data_table.find_all('tr')

    # data located between first 4 td tags and last 1 td tag

    for tr in tr_tags[1:]:
        table_cell = tr.find_all('td')[5]

        #print(table_cell.contents[1])

        for subdomain in table_cell.contents:
            subdomain = subdomain.text.strip()
            if subdomain != '' and subdomain not in subdomains_found:
                subdomains_found.append(subdomain)
                #print(subdomain)

    return subdomains_found


# parsing user arguments
user_arguments = get_arguments()
if user_arguments.identity:
    identity = user_arguments.identity
else:
    print('[-] identity is not defined! use --help for more info.')
    exit()

subdomains_found = get_subdomains(identity)


print('[+] subdomains found:\n'+'-'*20)
print("\n".join(subdomains_found))

if user_arguments.output_file:
    output_file = user_arguments.output_file
    save_output(output_file, subdomains_found)
    print('\n[+] output is written to:', output_file)
            




