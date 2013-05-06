#-*- coding:utf-8 -*-
#Author kenny @ 2013.5.5
import Skype4Py
import GetTweet
import datetime, re, httplib,sys,time
from urllib import urlencode

#欲Post Message過去的SkypeChannel
SkypeChannelName = "Input your SkypeChannelName"   #ex: SkypeChannelName = "#SkypeAccount/$4fafddddee297d1c"

#Recheck Time(秒)
CheckTime = 60

#存取Tweets數目
TweetNum = 5

#TwitterAccount-填入欲Follow的帳號
TwitterAccount = ['qweasdHHHH','CCCVV5555']


def GetActiveSkypeChannelName():
  #獲得目前Skype正在對話的ChatName
	print skype.ActiveChats[0]


def Usage():
	print u'1.開啟Skype點選欲列出訊息之Skype Channel'
	print u'2.複製下方的SkypeChannelName(包含#號)'
	GetActiveSkypeChannelName()
	print u'3.取代Twitter2Skype.py內的SkypeChannelName變數'
	print u'EX: SkypeChannelName = \'#SkypeAccount/$4fafddddee297d1c\''
	print u'4.修改TwitterAccount列表，新增欲Follow之User'

def main():
	
	if SkypeChannelName == "Input your SkypeChannelName":
		Usage()
		sys.exit()

	TwitterArrayLen = len(TwitterAccount)#帳號總數
	StoredTweetList =[[0 for x in range(TweetNum)] for y in range(TwitterArrayLen)]#2維List

	while True:
		
		#抓取TwitterTimeLine內容,放進List中
		for i,user in enumerate(TwitterAccount): 
			print '%d:[%s]' % (i+1,user)
			TmpList = []
			Post2SkypeList = []

			GettweetsList =  GetTweet.read_tweets(user, TweetNum) #抓取最新Twtte

			for x in GettweetsList:
				print '%s' % ( x.html_text.encode('utf8') )
				TmpList.append(x.html_text.encode('utf8'))
			
			#比對留言是否新增
			if StoredTweetList[i][0] == 0:#第一次執行
				print 'FirstStart!!'
				StoredTweetList[i] = TmpList[:] #複製List
				continue

			#print 'TmpList:%s' % TmpList
			#print 'StoredTweetList[i]:%s' % StoredTweetList[i]
			Post2SkypeList = filter( lambda x: x not in StoredTweetList[i] , TmpList) #去掉重複


			if Post2SkypeList == []:#沒有多出來的新Tweet,繼續下一帳號
				continue
			

			#控制Skype發送Twitter留言
			for Message in Post2SkypeList:
				print 'Post2Skype:%s' % Message
				skype.Chat(SkypeChannelName).SendMessage( Message )
				
			#把Tweet放入List中保存
			StoredTweetList[i] = TmpList[:]

		time.sleep( CheckTime )#重新檢查時間



if __name__ == '__main__':
	try:
		skype = Skype4Py.Skype()
		skype.Attach()
	except:
		print 'Attach Skype Error!!  Please check...'
		sys.exit(0)
	main()


