--实验下lua table的作用域
--怎样情况 lua中的全局变量

local t = {}

function cleart()  --这里没有传t 那么全局的t就被清空 t的声明一定要在函数之前
    t = {}
end

t['1'] = 2
print(t['1'])
cleart(t)
print(t['1'])

t['1'] = 1
print(t['1'])

