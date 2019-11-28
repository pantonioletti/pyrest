import falcon
import ora_tools.connection as otc

class DataFiles(object):

    def on_get(self, request, response):
        print('Reading GET request')
        response.status = falcon.HTTP_200
        if 'name' in request.params:
            s = '<body><h1>Hello '+request.params['name']+' world!</h1></body>\n'
        else:
            s='<body><h1>Hello world!</h1></body>\n'
        response.body = s

    def on_post(self, request, response):
        print('Processing POST request')
        fd = open('c:/dev/projects/pyrest/whatever.xlsx','wb')
        print('Destination file opened')
        fd.write(request.bounded_stream.read())
        print('Wrote POST content to file')
        fd.close()
        print('Ending')
        response.status = falcon.HTTP_200


class DBAccess(object):

    def __init__(self):
        self.pool = otc.get_pool({otc.P_USER:'pmm', otc.P_PASSWD:'pmm', otc.P_SID:'coronadev', otc.P_POOLMIN:1, otc.P_POOLMAX:5, otc.P_INCR:1, otc.P_ENC:'UTF-8'})

    def on_get(self, request, response):
        if 'sku' in request.params:
            sku = request.params['sku']
            stmt = "select * from prdmstee where prd_lvl_number ='{0}' and prd_lvl_id = 1".format(sku)
            conn  = self.pool.acquire()
            cur = conn.cursor()
            res = cur.execute(stmt)
            response.body = otc.resp2json(cur.description, res.fetchall())
            conn.close()


class Hello(object):

    def on_get(self,request, response):
        response.status = falcon.HTTP_200
        if 'name' in request.params:
            s = '<body><h1>Hello '+request.params['name']+' world!</h1></body>\n'
        else:
            s='<body><h1>Hello world!</h1></body>\n'
        response.body = s
        #if 'name' in  d:
        #    s.replace('world',d['name'])
        #return Response(s)

#def application(environ, start_response):
#    status = '200 OK'
#    output = b'Hello World!'
#
#    response_headers = [('Content-type', 'text/plain'),
#                        ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)

#    return [output]
application = falcon.API()
#application.req_options.auto_parse_form_urlencoded = True
#application.add_route('/hello', Hello())
#application.add_route('/dbaccess', DBAccess())
application.add_route('/file-upload', DataFiles())
