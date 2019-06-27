import re
from collections import defaultdict

datadict = defaultdict(int)
result = []
with open('gcsdata_ora_8396.trc', 'r') as f:
    content = f.readline()
    count = 0
    while len(content) > 0:
        count += 1
        obj = re.match('PARSE #([0-9]*)?.*tim=([0-9]*)?.*',content)
        if obj:
            cursorNo = obj.group(1)
            StartTime = obj.group(2)
            datadict[cursorNo] = StartTime

        obj = re.match("CLOSE #([0-9]*)?.*tim=([0-9]*)?.*",content)

        if obj:
            cursorNo = obj.group(1)
            if cursorNo in datadict:
                result.append({"cursor":cursorNo, "start":datadict[cursorNo], "end": obj.group(2), "second": (int(obj.group(2)) - int(datadict[cursorNo]))/1000000 })
                datadict.pop(cursorNo)

        if count % 10000 == 0:
            print(count)

        content = f.readline()

print(count)

with open("result.txt", 'w') as f:
    for seq,a in enumerate(result):
        f.write(str(a)+"\n")






