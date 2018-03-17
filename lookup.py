import re
import requests

ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

ip_occurrence = {}

def main():
    fil = open("auth.log", "r")

    for line in fil.readlines():
        match_obj = re.search(ip_regex, line)
        if(match_obj):
            ip = match_obj.group()
            if ip in ip_occurrence:
                ip_occurrence[ip]['occurrence'] += 1
            else:
                ip_occurrence[ip] = {'occurrence': 1}

    for ip_address in ip_occurrence:
        location = requests.get('http://ipinfo.io/'+ip_address).json()
        location.pop('ip')
        ip_occurrence[ip_address].update(location)
        pass
    
    print ip_occurrence


if __name__ == "__main__":
    main()
