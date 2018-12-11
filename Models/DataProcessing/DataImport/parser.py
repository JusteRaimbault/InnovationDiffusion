import csv

def parse_csv(f,delimiter,quote,id_field):
    print('importing file '+str(f))
    r=open(f,'r')
    #lines=r.readlines()
    lines = csv.reader(r, delimiter=delimiter, quotechar=quote)
    res={}
    header=[]
    #for l in range(1,len(lines)):
    l=0
    for currentline in lines:
        if l % 10000 == 0 : print(l)
        #currentline = lines[l].split(delimiter)
        if l==0 : header=currentline
        currentrec = {}
        if len(currentline)==len(header) and currentline != header:
            for j in range(0,len(currentline)):
                currentrec[header[j]]=currentline[j].replace("\"","")
            currentrec['id']=currentrec[id_field]
            res[currentrec['id']]=currentrec
        else :
            print('Error record :'+str(currentline))
        l=l+1
    return(res)

