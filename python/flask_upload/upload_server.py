# coding:utf-8
import re
import os
import time
import tempfile
import mimetypes

import psutil
import werkzeug
import requests
from flask import Flask, jsonify, request
from flask import stream_with_context, send_file
from flask import Response

app = Flask(__name__)


def current_milli_time():
    return int(round(time.time() * 1000))


def int_with_commas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + int_with_commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


def measure_spent_time():
    start = current_milli_time()
    diff = { 'res' : None }
    def get_spent_time(raw=False):
        if diff['res'] == None:
            diff['res'] = current_milli_time() - start
        if raw:
            return diff['res']
        else:
            return int_with_commas(diff['res']) 
    return get_spent_time


@app.route('/upload', methods=['POST'])
def upload():
    def custom_stream_factory(total_content_length, filename, 
        content_type, content_length=None):
        tmpfile = tempfile.NamedTemporaryFile('wb+', prefix='flaskapp')
        return tmpfile

    ms = measure_spent_time()
    _, _, files = werkzeug.formparser.parse_form_data(
                              request.environ, 
                              stream_factory=custom_stream_factory)
    total_size = 0

    for fil in files.values():
        total_size += os.path.getsize(fil.stream.name)

    mb_per_s = "%.1f" % ((total_size / (1024.0*1024.0)) / ((1.0+ms(raw=True))/1000.0))
    res = " ".join([str(x) for x in ["handling POST request, spent", 
            ms(), "ms.", mb_per_s, "MB/s."]])
    process = psutil.Process(os.getpid())
    memery_str = "memory usage: %.1f MiB" % (process.memory_info().rss / (1024.0*1024.0))
    return jsonify({'code': 0, 'msg': res, 'memeory': memery_str}) 


@app.route("/upload2", methods=["POST"])
def upload2():
    ms = measure_spent_time()
    total_size = 0

    with open("stream_test.log", "wb") as f:
        chunk_size = 4096
        while True:
            chunk = request.stream.read(chunk_size)
            if len(chunk) == 0:
                break
            total_size += len(chunk)
            f.write(chunk)

    mb_per_s = "%.1f" % ((total_size / (1024.0*1024.0)) / ((1.0+ms(raw=True))/1000.0))
    res = 'speed %s MB/s' % mb_per_s
    process = psutil.Process(os.getpid())
    memery_str = "memory usage: %.1f MiB" % (process.memory_info().rss / (1024.0*1024.0))        
    return jsonify({'code': 0,
                    'memory': memery_str,
                    'msg': res})


@app.route("/upload/chunked", methods=["POST", "PUT"])
def upload_chunked():
    fullpath = 'chunk_test.log'

    if 'Content-Range' in request.headers:
        # extract starting byte from Content-Range header string
        range_str = request.headers['Content-Range']

        total_bytes = int(range_str.split(' ')[1].split('/')[1])
        tmp = range_str.split(' ')[1].split('/')[0] 
        start_bytes, end_bytes = [int(i) for i in tmp.split('-')]

        if start_bytes == 0:
            print 'upload start ..'
            try:
                os.remove(fullpath)
            except OSError:
                pass

        # append chunk to the file on disk, or create new
        with open(fullpath, 'ab') as f:
            f.seek(start_bytes)
            f.write(request.stream.read())
        
        if end_bytes == total_bytes:
            print 'upload end ..'
            return '', 200

    return '', 206


@app.route('/download/chunked')
def chunk_download():
    range_header = request.headers.get('Range', None)
    path = 'test.log'
    size = os.path.getsize(path)  

    if not range_header: 
        # return send_file(path)
        # send Content-Length
        rv = Response('', 200)
        rv.headers['Content-Length'] = str(size)
        return rv
    
    byte_start, byte_end = 0, None
    m = re.search(r"(\d+)-(\d*)", range_header)
    g = m.groups()
    
    if g[0]: byte_start = int(g[0])
    if g[1]: byte_end = int(g[1])

    length = size - byte_start
    if byte_end is not None:
        length = byte_end - byte_start + 1
    
    data = None
    with open(path, 'rb') as f:
        f.seek(byte_start)
        data = f.read(length)

    rv = Response(data, 
        206,
        mimetype=mimetypes.guess_type(path)[0], 
        direct_passthrough=True)
    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte_start, byte_start + length - 1, size))
    rv.headers.add('Accept-Ranges', 'bytes')
    return rv



@app.route('/proxy/download/<path:url>')
def download(url):
    req = requests.get(url, stream=True)
    return Response(stream_with_context(req.iter_content()), 
                    content_type=req.headers['content-type'])


@app.route("/proxy/upload", methods=["POST"])
def proxy():
    resp = requests.post('http://destination_host/upload_api', 
                         files={'file': request.stream})
    return resp.text, resp.status_code


if __name__ == "__main__":
    app.run(debug=True)