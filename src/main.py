import os
import csv
import os.path

namecsv=''
date=''
nline=''
infoexec=''
date2=''
nline2=''
inforesult=''


# fnc loadcsv
def loadcsv(): 
    global namecsv
    global date
    global nline
    global infoexec
    global date2
    global nline2
    global inforesult

    if namecsv and date and nline and infoexec and date2 and nline2 and inforesult: 
        if os.path.isfile(namecsv + '.csv'):
            with open(namecsv + '.csv', 'a', newline='') as file:
                fieldnames = ['DATE_CMD', 'LINE_CMD', 'CMD_EXECUTE', 'DATE_RESULT', 'LINE_RESULT', 'RESULT']
                writer = csv.DictWriter(file, fieldnames= fieldnames)
                writer.writerow( {'DATE_CMD': date, 'LINE_CMD': nline, 'CMD_EXECUTE': infoexec, 'DATE_RESULT': date2, 'LINE_RESULT': nline2, 'RESULT': inforesult} )

        else:
            with open(namecsv + '.csv', 'a', newline='') as file:
                fieldnames = ['DATE_CMD', 'LINE_CMD', 'CMD_EXECUTE', 'DATE_RESULT', 'LINE_RESULT', 'RESULT']
                writer = csv.DictWriter(file, fieldnames= fieldnames)
                writer.writeheader()
                writer.writerow( {'DATE_CMD': date, 'LINE_CMD': nline, 'CMD_EXECUTE': infoexec, 'DATE_RESULT': date2, 'LINE_RESULT': nline2, 'RESULT': inforesult} )

# fnc cleanbuffer 
def cleanbuffer():
    global namecsv
    global date
    global nline
    global infoexec
    global date2
    global nline2
    global inforesult

    namecsv=''
    date=''
    nline=''
    infoexec=''
    date2=''
    nline2=''
    inforesult=''


# fnc loaddata
def loaddata(ncsv, line, info):
    global namecsv
    global date
    global nline
    global infoexec

    namecsv=''
    date=''
    nline=''
    infoexec=''

    nline = line
    date = info[0:23]

    # print('fnc loaddata, info: ')
    # print(info)
    
    x = (ncsv.split("\Factory", 1)[1])
    for i in x:
        if i == "_":
            break
        else:
            namecsv += i

    x = (info.split("Execute", 1)[1])
    for i in x:
        if i == ".":
            break
        else:
            infoexec += i

    # print('namecsv')
    # print(namecsv)

    # print('date')
    # print(date)

    # print('nline')
    # print(nline)

    # print('infoexec')
    # print(infoexec)


# loaddata2
def loaddata2(line, info):
    global date2
    global nline2
    global inforesult

    date2=''
    nline2=''
    inforesult=''

    nline2 = line
    date2 = info[0:23]

    # print('fnc loaddata 2, info: ')
    # print(info)

    x = (info.split("Result=", 1)[1])
    for i in x:
        if i == ",":
            break
        else:
            inforesult += i

    # print('date2')
    # print(date2)

    # print('nline2')
    # print(nline2)

    # print('inforesult')
    # print(inforesult)


# fnc savefile
def savefile(ftxt, fname):
    f = open("./" + fname + ".txt", "a")
    f.write(str(ftxt) + "\n")
    f.close()


# fnc search_substr
def search_substr(file_path, word, word2, fname):
    with open(file_path, 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find(word + ',') != -1 and line.find(word2 + ',') != -1 and line.find('ExecuteExecute') != -1:

                # print('debug line')
                # print(line)

                loaddata(str(file_path), str(lines.index(line)), line)

                savefile(str(word) + ' ' + str(word2) + ' string exists in file', fname)
                savefile(str(file_path), fname)
                savefile('Line Number:' + str(lines.index(line)), fname)
                savefile('Line:' + line, fname)


# fnc search_auxsubstr
def search_auxsubstr(file_path, fname, info):
    searchtarget=''
    searchtarget2=''

    # print('debug search_auxsubstr, info')
    # print(info)

    x = (info.split("window:", 1)[1])  
    for i in x:
        if i == ",":
            break
        else:
            searchtarget += i

    # print('Window=')
    # print(searchtarget)

    x = (info.split("RequestId=", 1)[1])  
    for i in x:
        if i == ",":
            break
        else:
            searchtarget2 += i

    # print('RequestId=')
    # print(searchtarget2)

    target='Window=' + searchtarget
    target2='RequestId=' + searchtarget2

    f = open(file_path, 'r')
    if target2 in f.read():
        search_substr(file_path, target, target2, fname)
    f.close()


# fnc search_str
def search_str(file_path, word, fname):
    with open(file_path, 'r') as fp:
        # read all lines in a list
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find(word) != -1:

                search_auxsubstr(file_path, fname, line)
                loaddata2(str(lines.index(line)), line)
                loadcsv()

                savefile(str(word) + ' string exists in file', fname)
                savefile(str(file_path), fname)
                savefile('Line Number:' + str(lines.index(line)), fname)
                savefile('Line:' + line, fname)

    cleanbuffer()


user_input = input('What is the name of your directory? ')
directory = os.listdir(user_input)


for fname in directory:
    if os.path.isfile(user_input + os.sep + fname):
        # Full path
        f = open(user_input + os.sep + fname, 'r')

        searchstring='Result=-'

        if searchstring in f.read():
            print('found string in file %s' % fname)
            search_str(user_input + os.sep + fname, searchstring, fname) 
        else:
            print('string not found')
        f.close()

