#!/usr/bin/python
import builtins
import sys
import requests
import array
from bs4 import BeautifulSoup
from datetime import date, timedelta
symbols = []

def Prompt1():
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
		CurrentStock = Calc()
		StockAbv = StockAbv.upper()
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
		CurrentStock = Calc()
		StockAbv = StockAbv.upper()
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
		print("\nStock:", StockAbv, "currently at: $", CurrentStock)
		
		if Type.upper() == 'C':
			print("Collateral Due is: $", Collateral)
			
		print ("Max Loss: -$", Loss)
		print ("Break Even Price: $", B_E_Price)
		print ("Max Gain: $", Gain)
		print ("Option expires in :", Delta.days, "days")
		
def Calc():
	for s in symbols:
		vals = {}
		url = ("https://finance.yahoo.com/quote/{}?p={}".format(s,s))
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')
		#print(soup)
		price = soup.find_all('div', {'class':'D(ib) Mend(20px)'})[0].find('span').text
		#print(price)
		return price			


art = open('AsciiArt.txt', 'r')
print (art.read())
art.close()

Prompt1()