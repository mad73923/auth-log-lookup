import re

ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

def main():
    fil = open("auth.log", "r")

    for line in fil.readlines():
        ip = re.search(ip_regex, line)
        if(ip):
            print(ip.group())

if __name__ == "__main__":
    main()
