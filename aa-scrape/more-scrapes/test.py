from collections import OrderedDict

mydict = {'carl':40,
          'alan':2,
          'bob':1,
          'danny':3}



from collections import OrderedDict
OrderedDict(sorted(d.items(), key=lambda i:keyorder.index(i[0])))
print(OrderedDict(mydict))
