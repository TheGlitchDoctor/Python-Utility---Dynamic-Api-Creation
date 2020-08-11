from inspect import getmembers, isfunction
import functions

#?Add functions to be exposed as a service in this functions_list
functions_list=[]
functions_list += [o for o in getmembers(functions) if isfunction(o[1])]

functions_lookup={}
for i in functions_list:
    functions_lookup[i[0]]=i[1]


