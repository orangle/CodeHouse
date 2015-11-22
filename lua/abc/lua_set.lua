--测试set类型的模拟和使用

ta = {}
ta["mac1"] = true
ta["mac2"] = true

print(type(ta))
print(ta["mac1"])


--这种方式的构造table ipairs不能遍历  pairs可以遍历
--pairs is for unordered iteration of table indices. ipairs is for ordered array indices.
for i,v in pairs(ta) do
    print(i)
end

