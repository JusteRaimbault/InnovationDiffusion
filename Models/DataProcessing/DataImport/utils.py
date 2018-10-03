
CONFFILE = '../conf/parameters.csv'
CONFIGNOREDFILE = '../conf/parameters_ignored.csv'

##
# get param value from param file
def get_parameter(param_name,as_string=False,ignored=False):
    if not ignored :
        pfile=import_csv(CONFFILE,';')
    else :
        pfile=import_csv(CONFIGNOREDFILE,';')
    value = 0
    for line in pfile:
        if line[0]==param_name :
            if not as_string :
                value=float(line[1])
            else :
                value = line[1]
    return(value)



def import_csv(csvfile,delimiter):
    infile = open(csvfile,'r')
    res = []
    for line in infile.readlines():
        if line[0]!="#" :
            res.append(line.replace('\n','').split(delimiter))
    return(res)
