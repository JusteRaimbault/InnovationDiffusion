import csv

def parse_csv(f,delimiter,quote,id_field):
    print('importing file '+str(f))
    r=open(f,'rb')
    #lines=r.readlines()
    lines = csv.reader(r, delimiter=delimiter, quotechar=quote)
    header = lines[0]
    res={}
    #for l in range(1,len(lines)):
    for currentline in lines[1:]:
        #if l % 1000 == 0 : print(l)
        #currentline = lines[l].split(delimiter)
        currentrec = {}
        if len(currentline)==len(header):
            for j in range(0,len(currentline)):
                currentrec[header[j]]=currentline[j].replace("\"","")
            currentrec['id']=currentrec[id_field]
            res[currentrec['id']]=currentrec
        else :
            print('Error record :'+str(currentline))
    return(res)
