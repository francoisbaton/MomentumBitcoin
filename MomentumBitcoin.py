import urllib.request
import re
import time

with urllib.request.urlopen('https://poloniex.com/public?command=returnTicker') as response:
   html = response.read()

def switch(i,j,input):
	#switch first column in matrix
	tmp1=input[i][0]
	input[i][0]=input[j][0]
	input[j][0]=tmp1
	#switch second column in matrix
	tmp1=input[i][1]
	input[i][1]=input[j][1]
	input[j][1]=tmp1
  
def bubbleSort(input):
	for i in range(len(input)):
		for j in range(len(input)):
			if(float(input[i][1])>float(input[j][1])):
				switch(i,j,input)   
  
def findPerf(array,key):
	for i in range(len(array)):
		if(array[i][0]==key):
			return array[i][1]
  
data=html.decode("utf-8")
tickerPos=[m.start() for m in re.finditer('":{"id":', data)]
perfPos=[m.start() for m in re.finditer('"percentChange":"', data)]
assert (len(tickerPos)==len(perfPos))
offsetPerfPosMin=17
offsetPerfPosMax=25
tickerValue = [[0 for x in range(2)] for y in range(len(tickerPos))] 
for i in range(len(tickerPos)-1):
	offsetTickerPos = (2 if i==0 else data.rfind(',', 0, tickerPos[i])+2)
	tickerValue[i][0]=data[offsetTickerPos:tickerPos[i]]
	tickerValue[i][1]=data[perfPos[i]+offsetPerfPosMin:perfPos[i]+offsetPerfPosMax]
  
bubbleSort(tickerValue)
filePath='D:/resultsMomentumBitcoin.txt'
numberBestAsset=5

with open(filePath) as file:
	last_line=file.readlines()[-1]
	file.close()
	
if last_line!='Data Recording\n':
	previousPerf=last_line.split(';')
	with open(filePath, "a") as myfile:
		myfile.write(time.strftime("%d/%m/%Y")+';')
		for i in range(numberBestAsset):
			myfile.write(findPerf(tickerValue,previousPerf[i+1])+';')
			if i==numberBestAsset-1:
				myfile.write('\n')
				myfile.close()
		
with open(filePath, "a") as myfile:
	myfile.write(time.strftime("%d/%m/%Y")+';')
	for i in range(numberBestAsset):
		myfile.write(tickerValue[i][0]+';')
		if i==numberBestAsset-1:
			myfile.write('\n')
			myfile.close()

