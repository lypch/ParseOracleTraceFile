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

        # At first the variable SQLTEXT is none, before encountering the PARSING IN CURSOR.
        if SQLText is not None:
            # When meet the string 'END OF STMT', means that the SQL statement is complete.
            obj = re.match('END OF STMT', content)
            if obj:
                sqldict[SQLID] =  {"sqlid": SQLID, "cursor": SQLCursor, "SQLTEXT":SQLText.replace("\n"," ")}
                SQLText = None
            else:
                SQLText += content
        else:
            # After meet the PARSING IN CURSOR, means that next line is the start of the SQL.
            obj = re.match("PARSING IN CURSOR #([0-9]*)?.*sqlid='(.*)'",content)
            if obj:
                SQLCursor = obj.group(1)
                SQLID = obj.group(2)
                SQLText = ""
            else:
                obj = re.match('PARSE #([0-9]*)?.*mis=([0-9]*)?.*tim=([0-9]*)?.*',content)
                if obj:
                    cursorNo = obj.group(1)
                    sqlmis = obj.group(2)
                    StartTime = obj.group(3)
                    datadict[cursorNo] = (sqlmis,StartTime)
                else:
                    obj = re.match("CLOSE #([0-9]*)?.*tim=([0-9]*)?.*",content)

                    if obj:
                        cursorNo = obj.group(1)
                        if cursorNo in datadict:
                            result.append({"cursor":cursorNo, "start":datadict[cursorNo][1], "end": obj.group(2), "second": (int(obj.group(2)) - int(datadict[cursorNo][1]))/1000000,"sqlmis": datadict[cursorNo][0]})
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
