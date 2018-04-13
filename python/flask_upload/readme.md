# flask http 上传下载demo

* python2.7.x 

产生文件 
```
make build
```

清除测试文件
```
make clean
```


`multipart/form-data` 模式上传(成功)

```
curl -v -F "data=@test.log" "http://localhost:5000/upload" 

curl -v -F "data=@test.log" "http://localhost:5000/upload2"
```


有关 [range-request的文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)


`chunk` 上传文件
```
python chunk_upload.py
```


`chunk` 下载文件
```

```


# thks 
* https://gist.github.com/mjohnsullivan/9322154
* https://gist.github.com/lizhiwei/7885684
* https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py