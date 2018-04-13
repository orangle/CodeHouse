# coding:utf-8
"""
一个字节获取size
根据size 分片，最后合并所有size，生成主文件

简单的方式，串行下载，直接append
优化方式，下载重试，并行下载，md5校验
"""
import sys
import os.path
import urllib2
import shutil
import hashlib

import logging
import requests

logging.basicConfig(level=logging.INFO)


def main(url, filename):
    block_size = 1000 * 1000* 10 # 1MB
    if os.path.exists(filename):
        logging.error('file: {} exists'.format(filename))
        return
    
    rep = requests.get(url)
    try:
        file_size = int(rep.headers['Content-Length'])
        logging.info('File size is %s' % file_size) 
        first_byte = 0

        while first_byte < file_size:
            last_byte = first_byte + block_size \
                if first_byte + block_size < file_size \
                else file_size

            logging.info('Downloading byte range %d - %d' % (first_byte, last_byte))
            r = requests.get(url, 
                    headers={"Range": 'bytes=%s-%s' % (first_byte, last_byte)},
                    stream=True)
            data_chunk = r.raw.read()
            with open(filename, 'ab') as f:
                f.write(data_chunk)
            first_byte = last_byte + 1 

    except IOError as e:
        logging.error('IO Error - %s' % e)
    except Exception as e:
        logging.error('', exc_info=True) 
    finally:
        if file_size == os.path.getsize(filename): 
            logging.info('download success')
        else:
            logging.error('download fail file size: {}, down size: {}'.format(
                file_size, os.path.getsize(filename) 
            ))

if __name__ == "__main__":
    main('http://127.0.0.1:5000/download/chunked', 'chunk_down.log')