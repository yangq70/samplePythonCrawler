#
# Author: Qidong Yang
# Flyer crawler
# 2019-09-10
#
import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import datetime

#
# Retrive info from Single store page
# urlNxt: url for next sotre; path:path to store files downloaded; linkList:list store site links; curcount: current list index;
# outterPath: path for specific store; updated:store updated; unUpdated:store not updated; updateNum:number of store updated
#
def digPageTillEnd(urlNxt, path,linkList,curcount,outterPath,updated,unUpdated,updateNum):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    strhtml = requests.get(urlNxt, headers=headers)
    soup = BeautifulSoup(strhtml.text, 'lxml')
    img = soup.select('#pageImage')
    if len(img) > 0:
        img_url = img[0].get('data-src')
        temp = img_url.split('/')
        temp = temp[len(temp)-1].split('.jpg')[0] + ".jpg"
        file_name = path + temp
        print(file_name)
        urllib.request.urlretrieve(img_url, filename=file_name)
    nextUrl = soup.select('.btn-next')
    if len(nextUrl) > 0:
        print("https://www.flyerbox.ca" + nextUrl[0].get('href'))
        digPageTillEnd("https://www.flyerbox.ca" + nextUrl[0].get('href'),path,linkList,curcount,outterPath,updated,unUpdated,updateNum)
    else:
        digIndexEndOrSpec(linkList,curcount,outterPath,updated,unUpdated,updateNum)


#
# iterate throgh prepared store list
# linkList: prepared store list; curcount: current list index; outterPath: path for specific store;
# updated:store updated; unUpdated:store not updated; updateNum:number of store updated
#
def digIndexEndOrSpec(linkList,curcount,outterPath,updated,unUpdated,updateNum):
    if curcount < len(linkList):
        storeName = linkList[curcount].get('storeName')
        if not os.path.exists(outterPath + storeName):
            os.makedirs(outterPath + storeName)
        pathtosave = outterPath + storeName + '/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        strhtml = requests.get(linkList[curcount].get('url'), headers=headers)
        soup = BeautifulSoup(strhtml.text, 'lxml')
        storeLogo = soup.select('.shop-logo img')[0].get('data-src')
        if not os.path.exists(pathtosave + "logo"):
            os.makedirs(pathtosave + "logo")
            urllib.request.urlretrieve(storeLogo, filename=pathtosave + "logo/storeLogo.jpg")
        nextPg = soup.select('.grid-item > a')
        curcount += 1
        print(storeName)
        if len(nextPg) > 0:
            date = soup.select('.grid-item')[0].select('small')[0].text
            path = pathtosave + date + "/"
            if not os.path.exists(path):
                updateNum += 1
                updated += storeName+", "
                os.makedirs(pathtosave + date)
                link = "https://www.flyerbox.ca" + nextPg[0].get('href')
                digPageTillEnd(link, path, linkList, curcount, outterPath, updated, unUpdated, updateNum)
            else:
                unUpdated += storeName+", "
                digIndexEndOrSpec(linkList, curcount, outterPath, updated, unUpdated, updateNum)
    else:
        dateToday = datetime.datetime.now()
        print(dateToday.strftime("%Y %B %d,%A %X"))
        print("Store with updates: "+updated)
        f.writelines(dateToday.strftime("%Y %B %d, %A %X"))
        f.writelines("\n")
        f.writelines("Store with updates: "+updated+"\n")
        print("Store with no updates: "+unUpdated)
        f.writelines("Store with no updates: "+unUpdated+"\n")
        print("Total number of store: ", len(linkList))
        f.writelines("Total number of store: ")
        f.writelines(str(len(linkList)))
        f.writelines("\n")
        print("Store updated: ", updateNum)
        f.writelines("Store updated: ")
        f.writelines(str(updateNum))
        f.writelines("\n\n\n")

storeList = [
{'url':'https://www.flyerbox.ca/costco/','storeName':'Costco'},
{'url':'https://www.flyerbox.ca/walmart/','storeName':'Walmart'},
{'url':'https://www.flyerbox.ca/loblaws/','storeName':'Loblaws'},
{'url':'https://www.flyerbox.ca/no-frills/','storeName':'Nofrills'},
{'url':'https://www.flyerbox.ca/real-canadian-superstore/','storeName':'Real Canadian Superstore'},
{'url':'https://www.flyerbox.ca/metro/','storeName':'Metro'},
{'url':'https://www.flyerbox.ca/food-basics/','storeName':'Food Basics'},
{'url':'https://www.flyerbox.ca/tt-supermarket/','storeName':'TNT supermarket（大统华）'},
{'url':'https://www.flyerbox.ca/ikea/','storeName':'IKEA '},
{'url':'https://www.flyerbox.ca/lowes/','storeName':'Lowe’s  Home Improvement'},
{'url':'https://www.flyerbox.ca/home-depot/','storeName':'The Home Depot'},
{'url':'https://www.flyerbox.ca/sleep-country/','storeName':'SleepyCountry'},
{'url':'https://www.flyerbox.ca/the-brick/','storeName':'The Brick'},
{'url':'https://www.flyerbox.ca/home-hardware/','storeName':'Home Hardware'},
{'url':'https://www.flyerbox.ca/jysk/','storeName':'JYSK'},
{'url':'https://www.flyerbox.ca/michaels/','storeName':'Michaels'},
{'url':'https://www.flyerbox.ca/best-buy/','storeName':'Best-buy'},
{'url':'https://www.flyerbox.ca/staples/','storeName':'Staples'},
{'url':'https://www.flyerbox.ca/canada-computers/','storeName':'Canada Computers'},
{'url':'https://www.flyerbox.ca/eb-games/','storeName':'EB Games'},
{'url':'https://www.flyerbox.ca/the-source/','storeName':'The Source'},
{'url':'https://www.flyerbox.ca/visions/','storeName':'Visions Electronics'},
{'url':'https://www.flyerbox.ca/henrys/','storeName':'Henry’s'},
{'url':'https://www.flyerbox.ca/2001-audio-video/','storeName':'2001 Audio Video'},
{'url':'https://www.flyerbox.ca/factory-direct/','storeName':'Factory direct'},
{'url':'https://www.flyerbox.ca/canadian-tire/','storeName':'Canadian Tire'},
{'url':'https://www.flyerbox.ca/princess-auto/','storeName':'Princess Auto'},
{'url':'https://www.flyerbox.ca/napa-auto-parts/','storeName':'NAPA Auto Patrs'},
{'url':'https://www.flyerbox.ca/toysrus/','storeName':'Toy R Us'},
{'url':'https://www.flyerbox.ca/babiesrus/','storeName':'Babies R Us'},
{'url':'https://www.flyerbox.ca/walmart/','storeName':'Walmart Toy Shop'},
{'url':'https://www.flyerbox.ca/walmart/','storeName':'Walmart Gift Book'},
{'url':'https://www.flyerbox.ca/longos/','storeName':'Longos Baby'},
{'url':'https://www.flyerbox.ca/rexall/','storeName':'Rexall'},
{'url':'https://www.flyerbox.ca/showcase/','storeName':'Showcase'},
{'url':'https://www.flyerbox.ca/shoppers/','storeName':'Shoppers Drug Mart'},
{'url':'https://www.flyerbox.ca/hudsons-bay/','storeName':'The Bay'},
{'url':'https://www.flyerbox.ca/sephora/','storeName':'Sephora'},
{'url':'https://www.flyerbox.ca/bass-pro/','storeName':'Bass Prop Shop'},
{'url':'https://www.flyerbox.ca/national-sports/','storeName':'Nathional Sports'},
{'url':'https://www.flyerbox.ca/sport-chek/','storeName':'Sport Chek'},
{'url':'https://www.flyerbox.ca/petsmart/','storeName':'PetSmart'},
{'url':'https://www.flyerbox.ca/pet-valu/','storeName':'Pet Valu'},
{'url':'https://www.flyerbox.ca/marks/','storeName':"Mark's"},
{'url':'https://www.flyerbox.ca/tsc-stores/','storeName':'TSC'},
{'url':'https://www.flyerbox.ca/hm/','storeName':'H&M'}
]
f= open("/Users/jake.yang_reao/Desktop/templateApp/imgSave/updateStatus.txt","a+")
digIndexEndOrSpec(storeList,0,"/Users/jake.yang_reao/Desktop/templateApp/imgSave/","","",0)
