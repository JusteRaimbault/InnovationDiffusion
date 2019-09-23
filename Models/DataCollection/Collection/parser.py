
from lxml import html,etree



def getrawtext(f):
    rawtext = open(f).readlines()
    text=''
    for l in rawtext:
        text=text+l.replace('\n','')
    return(text)

def parse(id,rawtext,verbose=False):
    tree = html.fromstring(rawtext)

    res = {}
    res['id']=id

    # title
    title = tree.xpath("//span[@itemprop='title']")[0].text.strip()
    if verbose:
        print('Title: '+title)
    res['title']=title

    # publicationNumber: id with code
    fullid = tree.xpath("//dd[@itemprop='publicationNumber']")[0].text
    res['fullid']=fullid

    # events : granted, published
    events = tree.xpath("//dd[@itemprop='events']")

    # grant
    # can be event granted
    grantDateSpan = tree.xpath("//time[@itemprop='grantDate']")
    if len(grantDateSpan)>0:
        grantDate=grantDateSpan[0].get('datetime')
        res['granted']=grantDate
    else:
        for event in events:
            #print(html.tostring(event))
            #print(event.xpath("span[@itemprop='type']")[0].text)
            if event.xpath("span[@itemprop='type']")[0].text == 'granted':
                grantDate = event.xpath("time[@itemprop='date']")[0].get('datetime')
                res['granted']=grantDate

    # application


    # abstract
    withabstract = tree.xpath("//abstract")
    if len(withabstract)>0:
        abstract = ''
        for e in withabstract[0].getchildren():
            abstract = abstract+' '+str(e.text)
        res['abstract']=abstract

    # description -> keep html (header, chemistry)
    description=[str(e.text) for e in tree.xpath("//div[@class='description']")[0].getchildren()]
    if verbose:
        print('Description: '+str(len(description))+' paragraphs')
    res['text']=description

    # inventor


    # assignee


    # publication
    #  -> can have several publication dates
    #  -> extract the provisory id from it
    #  -> the field publicationDate is however present ?
    published = tree.xpath("//time[@itemprop='publicationDate']")[0].get('datetime')
    res['published']=published

    # status
    status = tree.xpath("//span[@itemprop='status']")[0].text.strip()
    res['status']=status


    # citations
    # -> ~ two types of citations, "Orig" and final : what difference ?
    # backwardReferencesOrig,  backwardReferencesFamily,  backwardReferences,  detailedNonPatentLiterature,
    #  forwardReferences,  forwardReferencesOrig
    #  note : is forward ref field useful, as evolves in time anyway?
    citationsorigs=[]
    rows = tree.xpath("//tr[@itemprop='backwardReferencesOrig']")
    for row in rows:
        #print(html.tostring(row))
        #for child in row.getchildren():
        #    print(html.tostring(child)) # why the fuck xpath not working?
        #print(row.xpath("span[@itemprop='publicationNumber']"))
        #for span in row.findall('span'):
        #    print(span)
        #    print(html.tostring(span))
        #    print(span.keys())
        #    if 'itemprop' in span.keys():
        #        if span.get('itemprop')=='publicationNumber':
        #            citationsorigs.append(span.text)
        # ultra dirty but xpath does not work !
        for descendant in row.iterdescendants():
            if descendant.get('itemprop')=='publicationNumber':
                #print(html.tostring(descendant))
                citationsorigs.append(descendant.text)
        #print(citationsorigs)
        #print(row.xpath("span[@itemprop='publicationNumber']")[0].text)

    #citationsorigs = [row.xpath("span[@itemprop='publicationNumber']")[0].text for row in tree.xpath("//tr[@itemprop='backwardReferencesOrig']")]

    citationsfamily = [row.xpath("span[@itemprop='publicationNumber']")[0].text for row in tree.xpath("//tr[@itemprop='backwardReferencesFamily']")]
    citations = set(citationsorigs).union(set(citationsfamily))
    citationsnonorig = [row.xpath("span[@itemprop='publicationNumber']")[0].text for row in tree.xpath("//tr[@itemprop='backwardReferences']")]
    citationsadd = set(citationsnonorig).difference(citations)
    citationexternal = [row.xpath("span[@itemprop='publicationNumber']")[0].text for row in tree.xpath("//tr[@itemprop='detailedNonPatentLiterature']")]
    if len(citations)>0:
        res['citations']=list(citations)
    if len(citationsadd)>0:
        res['additional_citations']=list(citationsadd)
    if len(citationexternal)>0:
        res['citationexternal']=list(citationexternal)

    # prior art keywords and date
    priorArtKeywords = [kw.text for kw in tree.xpath("//dd[@itemprop='priorArtKeywords']")]
    res['priorArtKeywords']=priorArtKeywords
    priorArtDate = tree.xpath("//time[@itemprop='priorArtDate']")[0].text
    res['priorArtDate']=priorArtDate


    # pdflink
    pdflinks = tree.xpath("//a[@itemprop='pdfLink']")
    if len(pdflinks)>0:
        res['pdf']=pdflinks[0].get('href')
    # other links and images: not needed - for now (ex patents chemistry)


    return(res)


def validate(parsed):
    print('Title: '+str('title' in parsed)+' ; id: '+str('id' in parsed)+' ; text: '+str(len(parsed['text']))+' pars ; granted: '+str('granted' in parsed)+
        '; Abstract: '+str('abstract' in parsed+' ; citations : '+str('citations' in parsed))
    )
    return('title' in parsed and 'id' in parsed and 'text' in parsed and 'granted' in parsed)
