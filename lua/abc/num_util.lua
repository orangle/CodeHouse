-- 数学数字相关的


local function round(num, dip)
      return tonumber(string.format("%."..(dip or 0).."f", num))
end

-- test
print(352598537/1024.0/1024.0)
print(round(352598537/1024.0/1024.0, 2))
