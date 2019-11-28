import subprocess as sp

def str_to_byte(s):
    b = bytearray()
    b.extend(map(ord, s))
    return b

def run_query(connStr, sqlStmt, denv):
    #conStr should be in the for: <user>/<passwd>@<tns name>
    cp = sp.Popen(["sqlplus", "-S", connStr], stdout=sp.PIPE, env=denv, stdin=sp.PIPE)
    cp.stdin.write(str_to_byte(sqlStmt))
    return cp.communicate()


def data_to_list(data, sep):
    lines = data.splitlines(False)
    lst = list()
    for l in lines:
        if l.rfind(sep) != -1:
            cols = l.split(sep)
            for i in range(len(cols)):
                cols[i]=cols[i].strip('\t ')
            lst.append(cols)
    return (lst)


'''
deirectivas de sqlplus
set linesize 1000 : define el largo de una linea
set colsep # : define caracter que usara para separar datos de columnas
set heading off : habilita/deshabilita el encabezado de fila con el nombre de columnas
set recsep off : habilita/deshabilita separador entre filas
set feedback off : habilita/deshabilita mensaje con la cantidad de filas
set verify off : habilita/deshabilita mensaje de sustitucion de parametros
'''

