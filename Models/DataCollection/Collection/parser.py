
from lxml import html,etree



def getrawtext(f):
    rawtext = open(f).readlines()
    text=''
    for l in rawtext:
        text=text+l.replace('\n','')
    return(text)

def parse(id,rawtext,verbose=False):
    """
    Not included:
      - External links, images links
      - Priority Applications [applications claiming priority instead]; family: application priority; Country status: priority [should test if different ?]
      - events : reassignement, expiration (?), priority (in priorities)
      - direct associations: in prev_pub
      - legal events
    """

    if verbose:
        print('Parsing '+str(id))

    tree = html.fromstring(rawtext)

    res = {}
    res['id']=id

    # title
    title = tree.xpath("//span[@itemprop='title']")[0].text.strip()
    if verbose:
        print('Title: '+title)
    res['title']=title

    # publicationNumber: id with code - should be the only dd with this attribute
    fullid=''
    fullidelem = tree.xpath("//dd[@itemprop='publicationNumber']")
    if len(fullidelem)>0:
        fullid = fullidelem[0].text.strip()
        res['fullid']=fullid


    # grant - can be event granted
    grantDate=''
    grantDateSpan = tree.xpath("//time[@itemprop='grantDate']")
    if len(grantDateSpan)>0:
        grantDate=grantDateSpan[0].get('datetime')
    else:
        grantDate=get_event_date(tree,'granted')
    if len(grantDate)>0:
        res['granted']=grantDate

    # publication
    pubdate=''
    published = tree.xpath("//dd/time[@itemprop='publicationDate']")
    if len(published) > 0:
        pubdate = published[0].get('datetime')
    else:
        pubdate = get_event_date(tree,'publication')
    if len(pubdate)>0:
        res['published']=pubdate


    # application
    # applicationNumber
    applicationNumber = tree.xpath("//section[@itemprop='application']/section[@itemprop='metadata']/span[@itemprop='applicationNumber']")
    if len(applicationNumber)>0:
        res['applicationNumber']=applicationNumber[0].text

    # application date
    appdate=get_event_date(tree,'filed')
    if len(appdate)>0:
        res['filed']=appdate

    # abstract
    withabstract = tree.xpath("//abstract")
    if len(withabstract)>0:
        abstract = ''
        for e in withabstract[0].getchildren():
            abstract = abstract+' '+str(e.text)
        res['abstract']=abstract

    # description -> keep html (header, chemistry)
    #description=[html.tostring(e) for e in tree.xpath("//div[@class='description']")[0].getchildren()]
    #if verbose:
    #    print('Description: '+str(len(description))+' paragraphs')
    descriptionelem=tree.xpath("//div[@class='description']")
    if len(descriptionelem)>0:
        #res['text']= "".join([html.tostring(child) for child in descriptionelem[0].iterchildren()])
        #res['text']=html.tostring(descriptionelem[0])
        text = ""
        for child in descriptionelem[0].iterchildren():
            text=text+html.tostring(child)
        res['text']=text

    # inventors
    inventors = []
    inventorselem = tree.xpath("//dd[@itemprop='inventor']")
    if len(inventorselem)>0:
        for inv in inventorselem:
            inventors.append(inv.text)
        res['inventors']=inventors


    # assignees
    assigneeCurrent = []
    assigneeCurrentElem = tree.xpath("//dd[@itemprop='assigneeCurrent']")
    if len(assigneeCurrentElem)>0:
        for ass in assigneeCurrentElem:
            assigneeCurrent.append(ass.text)
        res['assigneeCurrent']=assigneeCurrent

    assigneeOriginal = []
    assigneeOriginalElem = tree.xpath("//dd[@itemprop='assigneeOriginal']")
    if len(assigneeOriginalElem)>0:
        for ass in assigneeOriginalElem:
            assigneeOriginal.append(ass.text)
        res['assigneeCurrent']=assigneeOriginal


    # status
    status = tree.xpath("//span[@itemprop='status']")[0].text.strip()
    res['status']=status


    # citations
    # -> ~ two types of citations, "Orig" and final : what difference ?
    # backwardReferencesOrig,  backwardReferencesFamily,  backwardReferences,  detailedNonPatentLiterature,
    #  forwardReferences,  forwardReferencesOrig
    #  note : is forward ref field useful, as evolves in time anyway?
    citationsorigs=get_citations(tree,'backwardReferencesOrig')
    citationsfamily=get_citations(tree,'backwardReferencesFamily')
    citations=set(citationsorigs).union(set(citationsfamily))
    citationsnonorig =get_citations(tree,'backwardReferences')
    citationsadd = set(citationsnonorig).difference(citations)
    citationexternal = get_citations(tree,'detailedNonPatentLiterature','title')
    if len(citations)>0:
        res['citations']=list(citations)
    if len(citationsadd)>0:
        res['citations_additional']=list(citationsadd)
    if len(citationexternal)>0:
        res['citation_external']=list(citationexternal)


    # classification: techno classes
    classes = get_techno_classes(tree)
    if len(classes)>0:
        res['classifications']=classes

    # similar patents
    similar = get_citations(tree,'similarDocuments')
    if len(similar)>0:
        res['similar']=similar


    # Application: priority; different ids; applications claiming priority
    priorities=[]
    for priority in tree.xpath("//tr[@itemprop='appsClaimingPriority']"):
        priorities.append([
          get_first_text(priority.xpath(".//span[@itemprop='applicationNumber']")),
          get_first_text(priority.xpath(".//span[@itemprop='representativePublication']")),
          get_first_text(priority.xpath(".//td[@itemprop='priorityDate']")),
          get_first_text(priority.xpath(".//td[@itemprop='filingDate']"))
          ]
        )
    if len(priorities)>0:
        res['priorities']=priorities

    # publication in other patent offices
    otherpubs=[]
    for otherpub in tree.xpath("//tr[@itemprop='docdbFamily']"):
        otherpubs.append([get_first_text(otherpub.xpath(".//span[@itemprop='publicationNumber']")),get_first_text(otherpub.xpath(".//td[@itemprop='publicationDate']"))])
    if len(otherpubs)>0:
        res['other_pubs']=otherpubs

    # Publication: all ids - pre-grant publication - consider only one possible
    allids = []
    for altid in tree.xpath("//tr[@itemprop='pubs']"):
        currentid = get_first_text(altid.xpath(".//span[@itemprop='publicationNumber']")).strip()
        if currentid != fullid:
            allids.append([currentid,get_first_text(altid.xpath(".//td[@itemprop='publicationDate']"))])
    if len(allids)>0:
        res['prev_pub']=allids[0]


    # Claims
    claimselem=tree.xpath("//div[@class='claims']")
    if len(claimselem)>0:
        res['claims']=html.tostring(claimselem[0])


    # prior art keywords and date
    priorArtKeywords = [kw.text for kw in tree.xpath("//dd[@itemprop='priorArtKeywords']")]
    if len(priorArtKeywords)>0:
        res['priorArtKeywords']=priorArtKeywords
    priorArtDate = tree.xpath("//time[@itemprop='priorArtDate']")
    if len(priorArtDate)>0:
        res['priorArtDate']=priorArtDate[0].text

    # pdflink
    pdflinks = tree.xpath("//a[@itemprop='pdfLink']")
    if len(pdflinks)>0:
        res['pdf']=pdflinks[0].get('href')
    # other links and images: not needed - for now (ex patents chemistry)


    return(res)


def get_event_date(tree,type):
    res=''
    events = tree.xpath("//dd[@itemprop='events']")
    for event in events:
        # in the case of successive publications, will get the latest, so the good date - always the case ?
        if event.xpath("span[@itemprop='type']")[0].text == type:
            res = event.xpath("time[@itemprop='date']")[0].get('datetime')
    return(res)


def get_techno_classes(tree):
    res = []
    # should be in order, no need to retrieve the 'FirstCode' meta
    leaves = tree.xpath("//meta[@itemprop='Leaf']")
    for leaf in leaves:
        code = leaf.getparent().xpath("span[@itemprop='Code']")
        if len(code)>0:
            res.append(code[0].text)
    return(res)



def get_citations(tree, type,target = 'publicationNumber'):
    citlist=[]
    rows = tree.xpath("//tr[@itemprop='"+type+"']")
    for row in rows:
        examiner=''
        if len(row.xpath(".//span[@itemprop='examinerCited']"))>0:
            examiner="*"
        for descendant in row.iterdescendants():
            if descendant.get('itemprop')==target:
                citlist.append(descendant.text+examiner)
    return(citlist)


def get_first_text(elems):
    if len(elems)>0:
        return(elems[0].text)
    else:
        return('')



def validate(parsed):
    return('title' in parsed and 'id' in parsed and 'text' in parsed and 'granted' in parsed and 'published' in parsed)


def to_string(parsed):
    for attr in ['abstract','citations','citations_additional','citations_external','classifications',
                 'similar','claims','text','applicationNumber','priorities','prev_pub','other_pubs']:
        if attr not in parsed:
            parsed[attr]=[]
    return(
        'Id: '+str(parsed['id'])+'\n'+
        '    Full id: '+str(parsed['fullid'])+'\n'+
        '    Title: '+parsed['title']+'\n'+
        '    Text: '+str(len(parsed['text']))+'\n'+
        '    Granted: '+parsed['granted']+'\n'+
        '    Published: '+parsed['published']+'\n'+
        '    Abstract: '+str(len(parsed['abstract']))+'\n'+
        '    Citations: '+str(len(parsed['citations']))+'\n'+
        '    Citation add: '+str(len(parsed['citations_additional']))+'\n'+
        '    Citation ext: '+str(len(parsed['citations_external']))+'\n'+
        '    Classes: '+str(len(parsed['classifications']))+'\n'+
        '    Similar: '+str(len(parsed['similar']))+'\n'+
        '    Claims: '+str(len(parsed['claims']))+'\n'+
        '    Application: '+str(parsed['applicationNumber'])+'\n'+
        '    Priorities: '+str(len(parsed['priorities']))+'\n'+
        '    Prev pub: '+str(parsed['prev_pub'])+'\n'#+
        '    Other pubs: '+str(len(parsed['other_pubs']))
        )
