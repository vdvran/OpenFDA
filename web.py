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

class OpenFDAParser():
	def get_drugs(self, events):
		druglist=[]
		info= json.loads(events)
		results=info["results"]
		for event in results:
			med= event["patient"]["drug"][0]["medicinalproduct"]
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

class OpenFDAHTML():
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
		#caminos
					<h1>Error 404</h1>
					</header>
					<p>not found</p>
				</body>
		</html>
		'''
		return html

class OpenFDAClient():
	OPENFDA_API_URL='api.fda.gov'
	OPENFDA_API_EVENT='/drug/event.json'
	def get_events(self, company_name, drug_name,limit):
		conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
		if company_name!='':#da las drogas
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+company_name+'&limit='+limit)
		elif drug_name!='':#da las compañias
	     		conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drug_name+'&limit='+limit)
		else:
			conn.request("GET", self.OPENFDA_API_EVENT + '?limit='+limit)
		r1 = conn.getresponse()
		data1=r1.read()
		event= data1.decode('utf8')
		return event

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

	def execute(self,html):
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(bytes(html, "utf8"))
		return

	def content_drugs(self,limit,company_name,drug_name):

		HTML=OpenFDAHTML()
		client=OpenFDAClient()
		parser= OpenFDAParser()

		events=client.get_events(company_name,drug_name,limit)
		items=parser.get_drugs(events)
		html= HTML.get_list(items)
		return html

	def content_companies(self,limit,company_name,drug_name):

		HTML=OpenFDAHTML()
		client=OpenFDAClient()
		parser= OpenFDAParser()

		events=client.get_events(company_name,drug_name,limit)
		items=parser.get_companies(events)
		html=HTML.get_list(items)
		return html

	def content_gender(self,limit,company_name,drug_name):

		HTML=OpenFDAHTML()
		client=OpenFDAClient()
		parser= OpenFDAParser()

		events=client.get_events(company_name,drug_name,limit)
		items=parser.get_gender(events)
		html=HTML.get_list(items)
		return html
	def limit_empty(self,limit):
		if limit=='':
			return True
	def limit_error(self,limit):
		if limit!= input(limit):
			return True

	def do_GET(self):
		company_name=''
		drug_name=''
		limit= ''
		client=OpenFDAClient()
		HTML=OpenFDAHTML()
		parser= OpenFDAParser()

		#caminos
		if self.path == '/':
			self.send_response(200)
			html=HTML.get_main_page()
			self.execute(html)
		elif '/list'in self.path:
			limit=self.path.split('=')[-1]
			if self.limit_empty(limit):
				limit='10'
			if 'Drugs?limit=' in self.path:
				self.send_response(200)
				html=self.content_drugs(limit,company_name,drug_name)
				self.execute(html)
			elif 'Companies?limit=' in self.path:
				self.send_response(200)
				html=self.content_companies(limit,company_name,drug_name)
				self.execute(html)
			elif "Gender?limit=" in self.path:
				self.send_response(200)
				html=self.content_gender(limit,company_name,drug_name)
				self.execute(html)

		elif '/search'in self.path:
			print ('search')
			if '&' in self.path:
				aux=self.path.split('?')[-1].split('&')
				limit=aux[-1].split('=')[-1]
				if self.limit_empty(limit):
					limit='10'
				if "Drug?drug=" in self.path:
					print ('droga')
					self.send_response(200)
					drug_name=aux[0].split('=')[-1]
					html=self.content_companies(limit,company_name,drug_name)
					self.execute(html)
				elif "Company?company=" in self.path:
					self.send_response(200)
					company_name=aux[0].split('=')[-1]
					html=self.content_drugs(limit,company_name,drug_name)
					self.execute(html)
			elif '&' not in self.path:
				if "Drug?drug=" in self.path:
					self.send_response(200)
					drug_name=self.path.split('=')[-1]
					limit='10'
					html=self.content_companies(limit,company_name,drug_name)
					self.execute(html)
				elif "Company?company=" in self.path:
					self.send_response(200)
					company_name=self.path.split('=')[-1]
					limit='10'
					html=self.content_drugs(limit,company_name,drug_name)
					self.execute(html)
		else:
			self.send_response(404)
			html=HTML.get_error()
			self.execute(html)
		return
