from bs4 import BeautifulSoup
import urllib.request as rq
import json
import re
import os


domain = 'https://www.thegioididong.com'
#Lay duong link cua cac loai Laptop
laptop_category = rq.urlopen('https://www.thegioididong.com/laptop').read()
soup_laptop_category = BeautifulSoup(laptop_category, 'html.parser')
# Tim tag div co class = 'manu manu9'
ls_link = soup_laptop_category.find_all('div', class_ = 'manu manu9')
# Tim link cua cac loai Laptop trong tag a
ls_a_tag = ls_link[0].find_all('a')

# Duyet cac tag a tim duoc
for i in range(len(ls_a_tag)):
##for i in range(1, 2):

    # Lay cac tag a co text bang None
    if ls_a_tag[i].text == '':
        
        link_laptop_category = ls_a_tag[i].attrs['href']
        crawl_laptops = rq.urlopen(domain + link_laptop_category).read()
        soup_crawl_laptops = BeautifulSoup(crawl_laptops, 'html.parser')
        ls_laptop = soup_crawl_laptops.find_all('li',class_="item laptop")
        

        for i in range(len(ls_laptop)):
##        for i in range(1):
            
            create_json = {} # Tao 1 dict de luu file json
            
            create_json['Name'] = ls_laptop[i].h3.text
            create_json['ProductId'] = ls_laptop[i].attrs['data-productid']
            # Lay link anh trong attribute 'data-original' va 'src' cua tag img
            key = 'data-original'
            if key in ls_laptop[i].img.attrs.keys() :
                create_json['Image'] = ls_laptop[i].img.attrs['data-original']
            else:
                create_json['Image'] = ls_laptop[i].img.attrs['src']
                
            create_json['Price'] = ls_laptop[i].find('input', class_='spInfo').attrs['data-price']

            productid = ls_laptop[i].attrs['data-productid']
##            link = ls_laptop[0].a['href'] 
            brand = ls_laptop[i].input.attrs['data-brand']
##            name = ls_laptop[i].h3.text
##            img = ls_laptop[i].img['src']
##            price = ls_laptop[i].find('input', class_='spInfo').attrs['data-price']

            # Lay bang thuoc tinh day du cua Laptop. Full Specs
            data = rq.urlopen('https://www.thegioididong.com/aj/ProductV4/GetFullSpec?productID=' + productid).read()

            soup_data = BeautifulSoup(data, 'html.parser')
            j = json.loads(soup_data.text)
            soup_ts = BeautifulSoup(j['spec'], 'html.parser')

            li = soup_ts.find_all('li')
            a = []
            b = []
            c = {}
            for l in li:
                if l.label != None:
                    a.append(l.label.text)
                    if len(c) != 0:
                        b.append(c)
                    c = {}
                elif l.label == None :
                    desc = l.div.text
                    new_desc = re.sub('\n|\r', '', desc)    #Loai bo ky tu \n \r
                    c[l.span.text] = new_desc.strip()
                    
            spec = {}
            for item, detail in zip(a,b):
                spec[item] = detail
            create_json['Spec'] = spec

            # Tao ham save file json
            def save_json(json_path):
                f = open(json_path, 'w', encoding = 'utf-8')
                json.dump(create_json, f, indent = 4, ensure_ascii = False)
                f.close()
                print('\n' + '*'*20 + '--' + create_json['Name'] + ' : WRITE FILE COMPLETED--' + '*'*20 + '\n')
                
            # Luu file json
            try:
                folder_path = 'f_json/' + brand + '/'
                if os.path.exists(folder_path):
                    json_path = folder_path + productid + '.json'
                    save_json(json_path)
                else:
                    os.mkdir(folder_path)
                    print('\n' + '-'*20 + folder_path + ' : CREATED' + '-'*20 + '\n')
                    json_path = folder_path + productid + '.json'
                    save_json(json_path)
            except:
                print('FAILED !!!')

print('\n' + '**'*10 + ' FINISH ' + '**'*10)

