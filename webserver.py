##!/usr/bin/python
#
#<FDAcoolapp>
#Copyright (C) <2017>  <Practica4, Violeta Duran Olivares>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#<Authors: Violeta Duran Olivares>

import http.server
import http.client
import json

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	OPENFDA_API_URL='api.fda.gov'
	OPENFDA_API_EVENT='/drug/event.json'
	def get_events(self, companyname, drugname):
		conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
		if companyname!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+companyname+'&limit=10')
		elif drugname!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drugname+'&limit=10')
		else:
			conn.request("GET", self.OPENFDA_API_EVENT + '?limit=10')
		r1 = conn.getresponse()
		data1=r1.read()
		data= data1.decode('utf8')
		event=data
		return event
	
	def get_drugs(self, events):
		druglist=[]
		info= json.loads(events)
		results=info["results"]
		for event in results:
			patient= event["patient"]
			drug=patient["drug"]
			med=drug[0]["medicinalproduct"]
			druglist.append(med)
		return druglist

	def get_companies(self, events):
		companylist=[]
		info= json.loads(events)
		results=info["results"]
		for event in results:
			company=event["companynumb"]
			companylist.append(company)
		return companylist

	def get_main_page(self):
		html='''
			<html>
			<head>
				<link rel="shortcut icon" href="http://www.infohep.org/Favicon.ashx?url=http://www.fda.gov:">
				<title>OpenFDA</title>
			</head>
			<body>
				<h1> OpenFDA Client</h1>
				<form method= "get" action="receivedrug">
					<input type="submit" value= "List of drugs">
					</input>
				</form>
				<form method= "get" action="receivecompany">
					<input type="submit" value= "List of compamies">
					</input>
				</form>
				<form method= "get" action="searchdrug">
					<input type="text" name= "drug"></input>
					<input type="submit" value= "Search companies"></input>
				</form>
				<form method= "get" action="searchcompany">
					<input type="text" name= "company"></input>
					<input type="submit" value= "Search drugs"></input>
				</form>
			</body>
			</html>
		'''
		return html

	def get_list_of_drugs(self, drugs):
		html='''
		<html>
			<head></head>
			<body>
				<ul>
		'''
		for drug in drugs:
			html +=" <li>"+drug+"</li>\n"
		html+='''
				</ul>
			</body>
		</html>
		'''
		return html

	def get_list_of_companies(self,companies):
		html='''
			<html>
			<head></head>
			<body>
				<ul>
		'''
		for company in companies:
			html +=" <li>"+company+"</li>\n"
		html+='''
				</ul>
			</body>
			</html>
		'''
		return html

	def do_GET(self):
		self.send_response(101)
		self.send_header('Content-type','text/html')
		self.end_headers()
		companyname=''
		drugname=''
		#caminos
		if self.path == "/":
			html=self.get_main_page()
		elif self.path=="/receivedrug?":
			events=self.get_events(companyname,drugname)
			drugs=self.get_drugs(events)
			html= self.get_list_of_drugs(drugs)
		elif self.path =="/receivecompany?":
			events=self.get_events(companyname,drugname)
			companies=self.get_companies(events)
			html=self.get_list_of_companies(companies)
		elif "/searchdrug?" in self.path:
			drugname=self.path.split('=')[-1]
			events=self.get_events(drugname,companyname)
			companies=self.get_companies(events)
			html= self.get_list_of_companies(companies)
		elif "/searchcompany?" in self.path:
			companyname= self.path.split('=')[-1]
			events=self.get_events(companyname,drugname)
			drugs=self.get_drugs(events)
			html= self.get_list_of_drugs(drugs)
		self.wfile.write(bytes(html, "utf8"))
		return
#<3<3<3<3

