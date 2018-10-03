

def parse_csv(f,delimiter,id_field):
    r=open(f,'r')
    lines=r.readlines()
    header = lines[0].split(delimiter)
    res={}
    for l in range(1,len(lines)):
        if l % 1000 == 0 : print(l)
        currentline = lines[l]
        currentrec = {}
        for j in range(0,len(currentline)):
            currentrec[header[j]]=currentline[j]
        currentrec['id']=currentrec[id_field]
        res[currentrec['id']]=currentrec
    return(res)
