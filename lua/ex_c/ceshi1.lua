-- 执行整个lua文件，lua当作配置文件
print("test1")

hostname = "lzz.com"
port = 8080
urls = {
	['/'] = "home.lua",
	["/login"] = "login.lua"
}
