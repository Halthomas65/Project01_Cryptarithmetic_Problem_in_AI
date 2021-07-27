from utility import removeBrackets

bind = "just + a + rather - (very - inteligent) + machine"

i=0
while bind[i] != '(':
    i += 1    
# j = i
# while bind[j] != ')':
#     j += 1
# sub = bind[i:j]
# new_sub = sub.replace("(","")
# new_sub = new_sub.replace(")","")
# bind = bind[:i] + new_sub + bind[j+1:]

bind = removeBrackets(bind,i)
print(bind)
# for inp in read_input():
#         # solve(inp[0], inp[1])
#         print(inp)