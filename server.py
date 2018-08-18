# -*- coding:utf-8 -*-
from flask import Flask, session, redirect, url_for, render_template,request
from optparse import OptionParser
import re
import mysqlspi
app = Flask(__name__)

@app.route('/')
def hello_world():
    pageNo = request.args.get('page', '')
    qstr = request.args.get('q', '')
    cotegory = request.args.get('c', '')
    if(not pageNo):
        pageNo=1
    booklist=mysqlspi.query_booklist(int(pageNo),qstr,cotegory)
    return   render_template('index.html',booklist=booklist,page='index')

@app.route('/about')
def about():
    booklist=mysqlspi.query_random()
    return   render_template('about.html',page='about')

@app.route('/meetup')
def meet_up():
    booklist=mysqlspi.query_random()
    return   render_template('meet.html',booklist=booklist,page='meet')



@app.route('/tags')
def route_tags():
    return   render_template('tags.html')


if __name__ == '__main__':
    parser = OptionParser(usage='Usage: %prog [options]')

    parser.add_option('-d', '--debug', dest='DEBUG', action='store_true',
                help='run in debugging mode (insecure)')
    parser.add_option('-l', '--listen', metavar='ADDRESS', dest='host',
                default='127.0.0.1',
                help='address to listen on [127.0.0.1]')
    parser.add_option('-p', '--port', metavar='PORT', dest='port',
                type='int', default=8088,
                help='port to listen on [8088]')
    (opts, args) = parser.parse_args()
    # Load config file if specified

    # Overwrite only those settings specified on the command line
    for k in dir(opts):
        if not k.startswith('_') and getattr(opts, k) is None:
            delattr(opts, k)
    app.config.from_object(opts)

    app.debug = True
    app.run(host=opts.host, port=opts.port, threaded=True)