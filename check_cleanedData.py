import os, json, re
def convert(input):
    elif isinstance(input, type(list)):
        return [convert(element) for element in input] 
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


rootdir = './newMovies'
list = os.listdir(rootdir)
for i in range(0,len(list)):
    path = os.path.join(rootdir,list[i])
    if os.path.isfile(path):
        name = os.path.basename(path)
        with open('./newMovies/{0}'.format(name)) as f:
            texts = convert(json.load(f))
            print name
            for j in range(len(texts)):
                print texts[j]
            


