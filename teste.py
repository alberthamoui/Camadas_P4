def gabarito(s):
    return ((1.275* s +1.25) /(s +0.625))
def eu(s):
    return ((((51*s/25))+2)/((8*s/5)+1))

s = 9

print(gabarito(s)==eu(s))
