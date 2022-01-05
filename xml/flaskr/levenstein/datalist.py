import json

f = open('intervenants.json')

data = json.load(f)

with open("datalist.txt", 'w', encoding='utf8') as fb:
    for num in data:
        fb.write("<option>"+data[num]["représentant"]["nom"]+"</option>\n")




f.close()