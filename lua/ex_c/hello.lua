print("test")
foo = 10
name = "lzz"


background = "GREEN"

WHITE = {r=1, g=1, b=1}

print(GREEN)

function f1()
	print("function1")
end

function f2(x, y)
	print("x:"..x.." y:"..y)
	return x+y
end

function f3(str)
	print("lua: f3 start..")
	if bar == nil then
		print('lua: function bar is nil')
		return 99, nil
	end

	local s, len = bar(str)
	print("lua: s "..s)
	print("lua: len "..len)
	return 99, len
end

f1()
f2(1,2)
f3("lzz")
