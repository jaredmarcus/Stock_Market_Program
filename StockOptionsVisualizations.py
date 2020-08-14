#!/usr/bin/python
import builtins, sys, requests, array, re, time, json, csv
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup
from datetime import date, timedelta
symbols = []


def Main():
	selection = input("Selection: ")
	if selection == '1':
		print("\n")
		Prompt1()
	elif selection == '2':
		print("\n")
		News()
	elif selection == '3':
		print("\n")
		WatchlistCreation()
	elif selection == '4':
		print("\n")
		StockInfo()
	elif selection == '5':
		print("\n")
		LiveStockInfo()
	elif selection == '6':
		print("\n")
		Settings()
	else:
		print ("INVALID SELECTION! Please enter a valid choice\n")
		return Main()

def Prompt1():
	OptionPayout = open('OptionPayout.txt', 'r')
	print (OptionPayout.read())
	OptionPayout.close()
	number = input("Pick a number for an Option Stategy for Analysis: \n1: Call \t2: Put\n")

	if number == '1': #Calls
		Call()
			
	elif number == '2': #Puts
		Put()

	elif number != '1' and number != '2':
		print ("INVALID SELECTION! Please enter a valid choice\n")
		return Prompt1()

def Call():
	Opt1 = input("Pick a number for a type of Call Option: \n1: BEAR Call Spread (Call CREDIT Spread) \t2: BULL Call Spread (Call DEBIT Spread)\n")
	option = '1' #Option 1 is for Calls
	if Opt1 == '1': #Bear Call Spread
		String = 'B'
		Type = 'C'
		Bear(option, String, Type)
	
	elif Opt1 == '2': #Bull Call Spread
		String = 'U'
		Type = 'D'
		Bull(option, String, Type)
		
	elif Opt1 != '1' and Opt1 != '2':
			print ("INVALID SELECTION! Please enter a valid choice\n")
			return Call()	

def Put():
	Opt2 = input("Pick a number for a type of Call Option: \n1: BEAR Put Spread (Put DEBIT Spread) \t2: BULL Put Spread (Call CREDIT Spread)\n")
	option = '2' #Option 2 is for Puts
	if Opt2 == '1': #Bear Call Spread
		String = 'B'
		Type = 'D'
		Bear(option, String, Type)
		
	elif Opt2 == '2': #Bull Call Spread
		String = 'U'
		Type = 'C'
		BullPut(option, String, Type)
		
	elif Opt2 != '1' and Opt2 != '2':
		print ("INVALID SELECTION! Please enter a valid choice\n")
		return Put()	

def Bear(option, String, Type):
		StockAbv = input("Enter Stock Abbreviation\n")
		StockAbv = StockAbv.lower()
		#print (StockAbv)
		symbols.append(StockAbv)
		#print (symbols)
		run = '1'
		CurrentStock = Calc(run)
		StockAbv = StockAbv.upper()
		run = '2'
		coName = Calc(run)
		print("\nCompany: ",coName)
		print ("Current Price of", StockAbv, "is: $", CurrentStock)
		HighStrike = input("Enter High Strike Price\n")
		LowStrike = input("Enter Low Strike Price\n")
		if Type.upper() == 'C':
			ContractPrice = input("Enter Credit Price\n")
		else:
			ContractPrice = input("Enter Contract Price\n")
		Contract = input("Enter how many Contracts\n")
		Date1 = date.today()
		Year = input ("What is the Exp Year?\n")
		Month = input("What is the Exp Month?\n")
		Day = input("What is the Exp Day?\n")
		Date2 = date(int(Year), int(Month), int(Day))
		Delta = Date2 - Date1
		BearChecker(StockAbv, CurrentStock, LowStrike, HighStrike, ContractPrice, Contract, option, String, Type, Delta)

def Bull(option, String, Type):
		StockAbv = input("Enter Stock Abbreviation\n")
		StockAbv = StockAbv.lower()
		#print (StockAbv)
		symbols.append(StockAbv)
		#print (symbols)
		run = '1'
		CurrentStock = Calc(run)
		StockAbv = StockAbv.upper()
		run = '2'
		coName = Calc(run)
		print("\nCompany: ",coName)
		print ("Current Price of", StockAbv, "is: $", CurrentStock)
		CurrentStock = input("Enter Current Stock Price")
		HighStrike = input("Enter High Strike Price\n")
		LowStrike = input("Enter Low Strike Price\n")
		if Type.upper() == 'C':
			ContractPrice = input("Enter Credit Price\n")
		else:
			ContractPrice = input("Enter Contract Price\n")
		Contract = input("Enter how many Contracts\n")
		Date1 = date.today()
		Year = input ("What is the Exp Year?\n")
		Month = input("What is the Exp Month?\n")
		Day = input("What is the Exp Day?\n")
		Date2 = date(int(Year), int(Month), int(Day))
		Delta = Date2 - Date1
		BullChecker(StockAbv, CurrentStock, LowStrike, HighStrike, ContractPrice, Contract, option, String, Type, Delta)

def BearChecker(StockAbv, CurrentStock, LowStrike, HighStrike, ContractPrice, Contract, option, String, Type, Delta):
	if LowStrike > HighStrike: 
		print("Low Strike Price can not be higher than the High Strike Price!")
		return Bear(option, String)
		
	#elif HighStrike < LowStrike: 			#DEADCODE
		#print("High Strike Price can not be lower than the Low Strike Price!")
		#return Bear(option, String)
		
	elif Contract == '0':
		print("Quantity of contracts can not be less than zero!")
		return Bear(option, String)
		
	if option == '1':
		Calculation(HighStrike, LowStrike, ContractPrice, Contract, option, CurrentStock, StockAbv, String, Type, Delta)
	elif option == '2':
		Calculation(HighStrike, LowStrike, ContractPrice, Contract, option, CurrentStock, StockAbv, String, Type, Delta)
	
def BullChecker(StockAbv, CurrentStock, LowStrike, HighStrike, ContractPrice, Contract, option, String, Type, Delta):
	if LowStrike > HighStrike: 
		print("Low Strike Price can not be higher than the High Strike Price!")
		return Bull(option)
	
	elif CurrentStock < '0':
		print("Current Stock Price can not be less than zero!")
		return Bull(option)
		
	#elif HighStrike < LowStrike: 			#DEADCODE
		#print("High Strike Price can not be lower than the Low Strike Price!")
		#return Bull(option)
		
	elif ContractPrice == '0' or ContractPrice < '0':
		print("Contract Price can not be less than zero!")
		return Bull(option)
		
	elif Contract == '0' or Contract < '0':
		print("Quantity of contracts can not be less than zero!")
		return Bull(option)
		
	if option == '1':
		CallsCalculation(HighStrike, LowStrike, ContractPrice, Contract, option, CurrentStock, StockAbv, String, Type, Delta)
	elif option == '2':
		PutsCalculation(HighStrike, LowStrike, ContractPrice, Contract, option, CurrentStock, StockAbv, String, Type, Delta)

def Calculation(HighStrike, LowStrike, ContractPrice, Contract, option, CurrentStock, StockAbv, String, Type, Delta): # 1 for Calls, 2 for Puts
		Width = (int(HighStrike) - int(LowStrike))
		Loss = '0'
		Gain = '0'
		
		if String.upper() == 'B':
			Loss = (int(Width) - float(ContractPrice)) * 100
			Loss = round(Loss, 2)
			Gain = (int(Width) * 100) - int(Loss)
			
		elif String.upper() == 'U':
			Gain = (int(Width) - float(ContractPrice)) * 100
			Loss = (int(Width) * 100) - int(Gain)
		
		B_E_Price = int(LowStrike) + float(ContractPrice)
		HighStrike = float(HighStrike)
		LowStrike = float(LowStrike)
		Loss = float(Loss)
		B_E_Price = float(B_E_Price)
		Gain = float(Gain)
		Collateral =(int(Width)*100)
		run = '2'
		coName = Calc(run)
		print("\nCompany: ",coName)
		print("Stock Abv:", StockAbv, "currently at: $", CurrentStock)
		
		if Type.upper() == 'C':
			print("Collateral Due is: $", Collateral)
			
		print ("Max Loss: -$", Loss)
		print ("Break Even Price: $", B_E_Price)
		print ("Max Gain: $", Gain)
		print ("Option expires in :", Delta.days, "days")
		
def Calc(run):
	for s in symbols:
		vals = {}
		url = ("https://finance.yahoo.com/quote/{}?p={}".format(s,s))
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')
		#print(soup)
		if run == '1':
			price = soup.find_all('div', {'class':'D(ib) Mend(20px)'})[0].find('span').text
			#print(price)
			return price
		elif run == '2':
			title = soup.find("title")
			tmp = title.get_text()
			rxTitle = re.compile(r'\(.*$')
			coName = rxTitle.sub("", tmp)
			return coName
			

def News(): #Program option 2
	News = open('News.txt', 'r')
	print (News.read())
	News.close()
	
def WatchlistCreation(): #Program option 3
	WatchlistCreation = open('WatchlistCreation.txt', 'r')
	print (WatchlistCreation.read())
	WatchlistCreation.close()

def StockInfo(): #Program option 4
	StockInfo = open('StockInfo.txt', 'r')
	print (StockInfo.read())
	StockInfo.close()
	
	api_key = 'N2KM217DEK4NJRPI'
	ts = TimeSeries(key=api_key, output_format='pandas')
	ans = input("Do you know the Stock Abbreviation? \n1.)Yes \t 2.)No\nSelection: ")
	if(ans == '1'):
		StockAbv = input("Enter Stock Abbreviation\n")
		StockAbv = StockAbv.lower()
		#print (StockAbv)
		symbols.append(StockAbv)
	elif (ans == '2'):
		Find()
		exit()
	run = '1'
	CurrentStock = Calc(run)
	StockAbv = StockAbv.upper()
	run = '2'
	CoName = Calc(run)
	print("\nCompany: ",CoName, "or", StockAbv)
	
	answer = input("Enter a number for a type of Stock Time Series: \n1.)Intraday \t\t 2.)Daily \n3.)Daily Adjusted \t 4.)Weekly \n5.)Weekly Adjusted \t 6.)Monthly \n7.)Monthly Adjusted \t 8.)Quote Endpoint\nSelection: ")
	if(answer == '1'): #intraday
		data, meta_data = ts.get_intraday(symbol=symbols, interval = '60min', outputsize = 'compact')
		print(data)
	elif (answer == '2'): #daily
		data, meta_data = ts.get_daily(symbol=symbols, outputsize = 'compact')
		print(data)
	elif (answer == '3'): #daily adj
		data, meta_data = ts.get_daily_adjusted(symbol=symbols, outputsize = 'compact')
		print(data)
	elif (answer == '4'): #weekly
		data, meta_data = ts.get_weekly(symbol=symbols)
		print(data)
	elif (answer == '5'): #weekly adj
		data, meta_data = ts.get_weekly_adjusted(symbol=symbols)
		print(data)
	elif (answer == '6'): #monthly
		data, meta_data = ts.get_monthly(symbol=symbols)
		print(data)
	elif (answer == '7'): #monthly adj
		data, meta_data = ts.get_monthly_adjusted(symbol=symbols)
		print(data)
	elif (answer == '8'): #quote endpoint
		data, meta_data = ts.get_quote_endpoint(symbol=symbols)
		print(data)
		
		
def Find():	
	api_key = 'N2KM217DEK4NJRPI'
	ts = TimeSeries(key=api_key, output_format='csv')
	key = input("Enter keywords to find desired stock\nSelection: ")
	print("List of stocks that may match your keywords will be outputted to a .csv file in the directory you have this file at.")
	StockFinder_csvreader, meta = ts.get_symbol_search(keywords = key)
	with open('Stock_Finder.csv', 'w') as write_csvfile:
		writer = csv.writer(write_csvfile, dialect='excel')
		for row in StockFinder_csvreader:
			writer.writerow(row)
	
		
def LiveStockInfo(): #Program option 5
	LiveStockInfo = open('LiveStockInfo.txt', 'r')
	print (LiveStockInfo.read())
	LiveStockInfo.close()
	
def Settings(): #Program option 6
	Settings = open('Settings.txt', 'r')
	print (Settings.read())
	Settings.close()	


art = open('AsciiArt.txt', 'r')
print (art.read())
art.close()

menu = open('Menu.txt', 'r')
print (menu.read())
menu.close()

Main()