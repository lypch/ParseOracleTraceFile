import re
import json

datadict = {}
result = []
sqldict = {}
SQLText = None
SQLCursor = ""
SQLID = ""

with open('gcsdata_ora_8396.trc', 'r') as f:
    content = f.readline()
    count = 0
    while len(content) > 0:
        count += 1

        if SQLText is not None:
            obj = re.match('END OF STMT', content)
            if obj:
                sqldict[SQLCursor] = {"sqlid": SQLID, "SQLTEXT":SQLText.replace("\n"," ")}
                SQLText = None
            else:
                SQLText += content
        else:
            obj = re.match("PARSING IN CURSOR #([0-9]*)?.*sqlid='(.*)'",content)
            if obj:
                SQLCursor = obj.group(1)
                SQLID = obj.group(2)
                SQLText = ""
            else:
                obj = re.match('PARSE #([0-9]*)?.*tim=([0-9]*)?.*',content)
                if obj:
                    cursorNo = obj.group(1)
                    StartTime = obj.group(2)
                    datadict[cursorNo] = StartTime

                else:
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
    for a in result:
        f.write(str(a)+"\n")

with open("SQL.txt" , 'w') as f:
    for data in sqldict:
        f.write("{} {}".format(data,sqldict[data])+"\n")
