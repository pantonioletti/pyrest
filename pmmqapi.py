import os
import json


SQLPLUS_SETTINGS="set linesize 1000\nset colsep #\nset heading off\nset recsep off\nset feedback off\nspool sqlplus.log append\n"


def getPMMDate(connStr, denv):
    try:
        resp, errmsg = xs.run_query(connStr,SQLPLUS_SETTINGS+'select caldat from caldayee;\n',denv)
    except :
        resp = {'error':'ERROR'}
    if 'ERROR' in resp or 'ORA-' in resp or 'SP2' in resp:
        resp={'error':'ERROR'}
    else:
        resp={'Date':resp.replace('\n')}


class PMM_API(object):
    def __init__(self):
        self.connStr = 'unipmm/Fr3ch2017@unipmm_test'
        self.denv = dict(os.environ)

    def on_get(self,req,resp):
        resp.status=falcon.HTTP_200
        if 'action' in req.params:
            if req.params['action'] == 'currentdate':
                resp.body=getPMMDate(self.connStr(), self.denv)#json.JSONEncoder().encode(getPMMDate(self.connStr(), self.denv))
        else:
            resp.body=json.JSONEncoder().encode(['Wrong request'])


api = application = falcon.API()
# Resources are represented by long-lived class instances
pmmapi = PMM_API()
# things will handle all requests to the '/things' URL path
api.add_route('/pmmdate', pmmapi)
