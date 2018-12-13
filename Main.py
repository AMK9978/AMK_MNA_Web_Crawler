import re
import requests

def calc(link,counter):
    if counter == 4:
        return
    counter += 1
    try:
        r = requests.get(link)
        content = r.text
        key = '<a href=[\'\"](.*?)[\'\"]'
        list = set(re.findall(key,content))
        for i in list:
            print('link is:' ,end='')
            if len(i) <2 or i[0]+i[1] != 'ht':
                i = link + i
                print(i)
            else:
                print(i)
            calc(i,counter)
    except Exception as ex:
        print(str(ex))
# def main():
list = ()
counter = 0
link = input('please input your line:').strip()
calc(link,0)

# if __name__ == 'main':
#     main()



