# flask http 上传下载demo

### 说明

http 上传通常有两种模式 

* 利用 enctype 为 `multipart/form-data`的表单上传，通常我们上传图片等小文件都是用这种方式. 参考MDN的文档 [Using FormData Objects](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects)。一般的web框架支持都还不错，注意稍大一些文件写到disk就好，否则可能内存用的比较多，常见的问题还有多文件批量上传。

* 使用 Range 模式上传，思路就是把大文件拆分成很多chunk上传，请求的 header中会带有 `Content-Range`字段，服务端接收所有chunk之后在合并，校验完整性，告诉客户端完成了上传。难点是，并行上传，文件压缩，完整性校验，服务端合并等，一般web框架可能没有提供方案，需要自己来设计和完成协议交互。

大文件下载一般都是支持断点续传，细节请参考MDN的文档 [range-request的文档](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)，主要通过 `Content-Range: bytes start-end/total_size` 这个header来控制，难点是并行下载，完整性校验等问题。

### 测试

写了一个基于flask的demo，这几种情况都包含了，但是实现的很简陋，可以了解协议交互和服务端处理的大概流程，学习之用。

* python2.7.x 

测试流程, 新建python virtualenv
```
pip install -r requirements.txt
```

产生文件, 1GB 的测试文件
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

`chunk` 上传文件
```
python chunk_upload.py
```

`chunk` 下载文件
```
python chunk_download.py
```


### thks 

* https://gist.github.com/mjohnsullivan/9322154
* https://gist.github.com/lizhiwei/7885684
* https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py