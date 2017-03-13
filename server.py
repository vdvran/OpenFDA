import socketserver
import webserver

PORT=8000


#webserver
#Handler = pruebawebserver.testHTTPRequestHandler
Handler = webserver.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler) #creas un objeto httpd a partir de la clase TCPSERVER

print ("serving at port", PORT)
httpd.serve_forever()
