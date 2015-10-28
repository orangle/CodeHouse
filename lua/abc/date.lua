--日期时间操作
--


print(os.time())

t = { year=1999, month=1, day=1, hour=1, min=1} 
print(os.time(t))

t2 = t
t1 = { year=1999, month=1, day=1, hour=1, min=2} 
print(os.difftime(os.time(t2), os.time(t1)))

print(os.date("%Y-%m-%d %X"))
