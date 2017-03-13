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

    def get_event(self):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data= data1.decode('utf8')
        event=data
        return event

    def get_event_search_med(self,drugname):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct='+drugname+'&limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data= data1.decode('utf8')
        event_drug_search=data
        return event_drug_search

    def get_event_search_companies(self,companyname):
        conn= http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + '?search=companynumb='+companyname+'&limit=10')
        r1 = conn.getresponse()
        data1=r1.read()
        data= data1.decode('utf8')
        event_companies_search=data
        return event_companies_search

    def get_listmed_search(self,companyname):
        medlist=[]
        events= self.get_event_search_companies(companyname)
        info= json.loads(events)
        results=info["results"]
        for event in results:
            patient= event["patient"]
            drug=patient["drug"]
            med=drug[0]["medicinalproduct"]
            medlist.append(med)
        return medlist

    def get_listcompanies_search(self,drugname):
        companylist=[]
        events= self.get_event_search_med(drugname)
        info= json.loads(events)
        results=info["results"]
        for event in results:
            company=event["companynumb"]
            companylist.append(company)
        return companylist

    def get_drugs_list(self):
        medlist=[]
        events=self.get_event()
        info= json.loads(events)
        results=info["results"]
        for event in results:
            patient= event["patient"]
            drug=patient["drug"]
            med=drug[0]["medicinalproduct"]
            medlist.append(med)
        return medlist

    def get_companies_list(self):
        companylist=[]
        data1=self.get_event()
        info= json.loads(data1)
        results=info["results"]
        for event in results:
            company=event["companynumb"]
            companylist.append(company)
        return companylist

    def get_main_page(self):
            html='''
            <html>
                <head>
                    <title>OpenFDA</title>
                </head>
                <body>
                    <h1> OpenFDA Client</h1>
                    <form method= "get" action="receivedrug">
                        </input>
                            <input type="submit" value= "List of drugs">
                    </form>
                    <form method= "get" action="receivecompany">
                        </input>
                            <input type="submit" value= "List of compamies">
                    </form>
                        </input>
                    <form method= "get" action="searchdrug">
                        <input type="text" name= "drug">
                        <input type="submit" value= "Search companies">
                    </form>
                    <form method= "get" action="searchcompany">
                        <input type="text" name= "company">
                        <input type="submit" value= "Search drugs">
                    </form>
                    </body>
                </html>
                '''
            return html

    def cod_list_of_meds(self):
        medlist=self.get_drugs_list()
        html='''
        <html>
        <head></head>
        <body>
            <ul>
            '''
        for drug in medlist:
            html +=" <li>"+drug+"</li>\n"
        html+='''
            </ul>
        </body>
        </html>
        '''
        return html

    def cod_list_of_companies(self):
        companylist=self.get_companies_list()
        html='''
        <html>
        <head></head>
        <body>
            <ul>
            '''
        for company in companylist:
            html +=" <li>"+company+"</li>\n"
        html+='''
            </ul>
        </body>
        </html>
        '''
        return html

    def cod_companies_search(self,drugname):
        companylist=self.get_listcompanies_search(drugname)
        html='''
   			<html>
   				<head></head>
   				<body>
   	 	   			<ul>
  	    				'''
        for company in companylist:
            html +=" <li>"+company+"</li>\n"
        html+='''
        		</ul>
    				</body>
    			</html>
    		'''
        return html

    def cod_med_search(self,companyname):
        medlist=self.get_listmed_search(companyname)
        html='''
   			<html>
   				<head></head>
   				<body>
   	 	   			<ul>
  	    				'''
        for med in medlist:
            html +=" <li>"+med+"</li>\n"
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

        #caminos
        if self.path == "/":
            html=self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif self.path=="/receivedrug?":
            html= self.cod_list_of_meds()
            self.wfile.write(bytes(html, "utf8"))
        elif self.path =="/receivecompany?":
            html=self.cod_list_of_companies()
            self.wfile.write(bytes(html,"utf8"))
        elif "/searchdrug?" in self.path:
            url= self.path
            drugname=url.split('=')[-1]
            html= self.cod_companies_search(drugname)
            self.wfile.write(bytes(html, "utf8"))
        elif "/searchcompany?" in self.path:
            url= self.path
            companyname=url.split('=')[-1]
            html= self.cod_med_search(companyname)
            self.wfile.write(bytes(html, "utf8"))
        return
#<3<3<3<3<3<3<3<3
