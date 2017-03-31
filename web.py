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
	def get_events(self, company_name, drug_name,limit):
		conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
		if company_name!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+company_name+'&limit='+limit)
		elif drug_name!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drug_name+'&limit='+limit)
		else:
			conn.request("GET", self.OPENFDA_API_EVENT + '?limit='+limit)
		r1 = conn.getresponse()
		data1=r1.read()
		event= data1.decode('utf8')
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

	def get_gender(self,events):
		genderlist=[]
		item=''
		info= json.loads(events)
		results=info["results"]
		for event in results:
			patient= event["patient"]
			gender=patient["patientsex"]
			if gender=='1':
				item='Female'
			elif gender=='2':
				item='Male'
			genderlist.append(item)
		return genderlist

	def get_main_page(self):
		html='''
		<html>
			<head>
				<link rel="shortcut icon" href="http://www.infohep.org/Favicon.ashx?url=http://www.fda.gov:">
				<title>OpenFDA</title>
			<style>
				header {
								font-size:150%;
								font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif;
    							padding: 1em;
    							color: white;
    							background-color: #87CEFA;
    							text-align: center;
				}
				footer{
						font-size:80%;
						font-family:verdana;
						padding: 1em;
						color: white;
						background-color: #87CEFA;
						text-align: center;
				}
				.bottom {
				 		background-color: #ADD8E6;
    					border: 3px solid #000000;
				}
			</style>
			</head>
			<body>
				<header>
				<h1> OpenFDA</h1>
				</header>
				<form method= "get" action="listDrugs">
					<input class= "bottom" type="submit" value= "List of drugs"></input>
					Limit:<input type="text" size="4" name= "limit" ></input>
				</form>
				<form method= "get" action="listCompanies">
					<input class= "bottom" type="submit" value= "List of compamies"></input>
					Limit:<input type="text"size="4" name= "limit" ></input>
				</form>
				<form method= "get" action="searchDrug">
					Drug name:<input type="text" name= "drug"></input>
					<input type="submit" value= "Search companies" ></input>
					Limit:<input type="text" size="4" name= "limit" ></input>
				</form>
				<form method= "get" action="searchCompany">
					Company name:<input type="text" name= "company"></input>
					<input type="submit" value= "Search drugs"></input>

				</form>
				<form method= "get" action="gender">
					<input class= "bottom" type="submit" value= "gender"></input>
					Limit:<input type="text" size="4" name= "limit" ></input>
				</form>
				<footer>Copyright &copy; vduran</footer>
			</body>
		</html>
		'''
		return html

	def get_list(self, items):
		html='''
		<html>
			<head></head>
			<body>
				<ol>
		'''
		for item in items:
			html +=" <li>"+item+"</li>\n"
		html+='''
				</ol>
			</body>
		</html>
		'''
		return html
	def get_error(self):
		html='''
		<html>
				<body>
					<header>
					<h1>Error 404</h1>
					</header>
					<p>not found</p>
				</body>
		</html>
		'''
		return html
	def execute(self,html):
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(html, "utf8"))
		return

	def do_GET(self):
		company_name=''
		drug_name=''
		limit=''
		#caminos
		if self.path == '/':
			self.send_response(200)
			html=self.get_main_page()
			self.execute(html)
		elif "/listDrugs" in self.path:
			self.send_response(200)
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
import html
import json

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	OPENFDA_API_URL='api.fda.gov'
	OPENFDA_API_EVENT='/drug/event.json'
	def get_events(self, company_name, drug_name,limit):
		conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
		if company_name!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+company_name+'&limit='+limit)
		elif drug_name!='':
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drug_name+'&limit='+limit)
		else:
			conn.request("GET", self.OPENFDA_API_EVENT + '?limit='+limit)
		r1 = conn.getresponse()
		data1=r1.read()
		event= data1.decode('utf8')
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

	def get_gender(self,events):
		genderlist=[]
		item=''
		info= json.loads(events)
		results=info["results"]
		for event in results:
			patient= event["patient"]
			gender=patient["patientsex"]
			if gender=='1':
				item='Female'
			elif gender=='2':
				item='Male'
			genderlist.append(item)
		return genderlist

	def get_main_page(self):
		html=''
		with open('codigo.html') as f:
			for line in f:
				html+= line
		return html

	def get_list(self, items):
		html='''
		<html>
			<head></head>
			<body>
				<ol>
		'''
		for item in items:
			html +=" <li>"+item+"</li>\n"
		html+='''
				</ol>
			</body>
		</html>
		'''
		return html
	def get_error(self):
		html='''
		<html>
				<body>
					<header>
					<h1>Error 404</h1>
					</header>
					<p>not found</p>
				</body>
		</html>
		'''
		return html
	def execute(self,html):
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(html, "utf8"))
		return

	def do_GET(self):
		company_name=''
		drug_name=''
		limit=''
		#caminos
		if self.path == '/':
			self.send_response(200)
			html=self.get_main_page()
			self.execute(html)
		elif "/listDrugs?limit=" in self.path:
			self.send_response(200)
			limit=self.path.split('=')[-1]
			events=self.get_events(company_name,drug_name,limit)
			items=self.get_drugs(events)
			html= self.get_list(items)
			self.execute(html)
		elif "/listCompanies?list=" in self.path:
			self.send_response(200)
			limit=self.path.split('=')[-1]
			events=self.get_events(company_name,drug_name,limit)
			items=self.get_companies(events)
			html=self.get_list(items)
			self.execute(html)
		elif "/searchDrug?drug=" in self.path:
			self.send_response(200)
			drug_name=self.path.split('=')[-1]
			'''
			aux=self.path.split('?')[-1]
			aux2=aux.split('&')
			limit=aux2[0].split('=')[-1]
			drug_name=aux2[-1].split('=')[-1]
			'''
			#print (drug_name)
			#print (limit)
			events=self.get_events(drug_name,company_name,limit)
			items=self.get_companies(events)
			html= self.get_list(items)
			self.execute(html)
		elif "/searchCompany?company=" in self.path:
			self.send_response(200)
			company_name= self.path.split('=')[-1]
			'''
			aux=self.path.split('?')[-1]
			aux2=aux.split('&')
			limit=aux2[0].split('=')[-1]
			company_name=aux2[-1].split('=')[-1]
			'''
			events=self.get_events(company_name,drug_name,limit)
			items=self.get_drugs(events)
			html= self.get_list(items)
			self.execute(html)
		elif "/gender?limit=" in self.path:
			self.send_response(200)
			limit=self.path.split('=')[-1]
			events=self.get_events(company_name,drug_name,limit)
			items=self.get_gender(events)
			html=self.get_list(items)
			self.execute(html)
		else:
			self.send_response(404)
			html=self.get_error()
			self.execute(html)
		return

#<3<3<3<3
#font-family:"Lucida Sans Unicode", "Lucida Grande", sans-serif
