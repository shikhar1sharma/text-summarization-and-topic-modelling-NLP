# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import re
import math
from pycorenlp import *
import itertools
from collections import defaultdict
import json

ENTITYOCURRANCELIST = []
# Function to find out if the whole WORD is present in a sentence
def contains_word(s, w):
    return (' ' + w.lower() + ' ') in (' ' + s.lower() + ' ')

# Counting the number of occurance of the entity and saving in a list
def CountingEntityoccurance(tempList):
    for elements in tempList:
        if elements not in ENTITYOCURRANCELIST:
            ENTITYOCURRANCELIST.append(elements)

def GeneratingJsonObjec1Counts(dictionaryForJosnObject1, companyName):
    wordCountDictionary = {}
    finalJsonObjectDictionary = {}
    for items in dictionaryForJosnObject1.values():
        #print items['text']
        if items['text'].lower() in wordCountDictionary.keys():
            wordCountDictionary[items['text'].lower()] +=1
        else:
            wordCountDictionary[items['text'].lower()] = 1

    finalJsonObjectDictionary[companyName] = wordCountDictionary
    data = json.dumps(finalJsonObjectDictionary, ensure_ascii=False)
    with open("data1.json", "w") as f:
        f.write(data)

def GeneratingJsonObject2(EntityOcurranceList, companyName):
    dictionaryForJosn = {}
    for index, text in enumerate(EntityOcurranceList):
        dictionaryForInsideJson = {}
        #for i in range(len(EntityOcurranceList[0])):
        neededIndex = -1
        for indexOfTuple, tupleText in enumerate(EntityOcurranceList[index][0].split(" ")):
            if companyName.lower() == str(tupleText.lower()):
                neededIndex = indexOfTuple
        if neededIndex != -1:
            dictionaryForInsideJson["text"] = EntityOcurranceList[index][0].split(" ")[neededIndex]
        else:
            dictionaryForInsideJson["text"] = EntityOcurranceList[index][0]
        dictionaryForInsideJson["sentence"] = EntityOcurranceList[index][1]
        dictionaryForInsideJson["start Index"] = EntityOcurranceList[index][2]
        dictionaryForInsideJson["end Index"] = EntityOcurranceList[index][3]
        dictionaryForJosn[str(index)] = dictionaryForInsideJson
    print "dictionary_json ", dictionaryForJosn
    GeneratingJsonObjec1Counts(dictionaryForJosn, companyName)
    data = json.dumps(dictionaryForJosn,'data.json', ensure_ascii=False)
    with open("data.json", "w") as f:
        f.write(data)
def CorefWithEntity(sentence, companyName= None):
    #companyName = "American Express"
    nlp = StanfordCoreNLP("http://localhost:9000/")
    #sentence = "The company does NOT have a clear guideline for its employees to go to higher band levels. It is easy for someone to reach Band 35 in a matter of 1-2 years from a Band 30. Compare this to the scenario about 5-6 years ago where you had to stay in a Band 30 for at least 5-6 years before you are promoted to Band 35 thereby amassing experience. With Delivery Transformation, it has been easy to go to Band 35 with little or no experience. At Band 35, you are STUCK with no growth opportunities. The number of openings at Band 40 are far lower than the number of employees absorbed at Band 35 via Delivery Transformation."
    #sentence = "Fitbit won the latest round of its ongoing legal fight with AliphCom's Jawbone when the U.S. International Trade Commission, or ITC, ruled that Fitbit did not misappropriate the latter's trade secrets. Don't expect the fight to end anytime soon, though, as another judge just overturned a previous ruling that will allow Fitbit's patent infringement suit against Jawbone to proceed. It appears the legal battle between the two fitness-tracking device makers is just heating up.In the long-running legal battle that started in May 2015, Jawbone accused Fitbit of stealing trade secrets and patent infringement. Earlier this year, the U.S. ITC invalidated the sleep monitoring and data output patents Jawbone claimed Fitbit had infringed upon. In the ruling, Judge Dee Lord stated the patents seek a monopoly on the abstract ideas of collecting and monitoring sleep and other health-related data, and are therefore ineligible. While the patent infringement was just part of Jawbone's claims against Fitbit, the U.S. ITC recently issued another ruling in favor of Fitbit and said the company had not misappropriated trade secrets from Jawbone. The company had been attempting to block the import of Fitbit's devices to the United States under the Tariff Act. Naturally, Jawbone was not pleased with the U.S. ITC's recent ruling and has already announced plans to appeal. Although the ruling is a win for Fitbit, other lawsuits between the two companies are still pending in federal and state courts. The claims involved in the lawsuits are basically the same claims in the complaints to the U.S. ITC. Jawbone alleges that Fitbit stole trade secrets when it hired former Jawbone employees and infringed on several of its patents. Jawbone accuses its former employees of stealing at least 335,191 files, which included schematics, manufacturing data, and product launch schedules, when Fitbit first hired them. I'm sure Fitbit investors breathed a sigh of relief after the recent U.S. ITC decision, because a ruling in favor of Jawbone would have had a devastating impact on Fitbit's business. In a prepared statement, Fitbit co-founder and CEO James Park said: We are pleased with the ITC's initial determination rejecting Jawbone's trade secret claims. From the outset of this litigation, we have maintained that Jawbone's allegations were utterly without merit and nothing more than a desperate attempt by Jawbone to disrupt Fitbit's momentum to compensate for their own lack of success in the market."
    #sentence = "AMex is a hUGe firm. Amex has around 10,000 employees. Amex is all around the world. They work hard for the company"
    #sentence = "TenKsolar, an American builder of integrated high-efficiency solar panels, is winding down its operations, according to sources close to the firm. Few solar hardware startups survive to adulthood in this ruthlessly competitive market. The demise of many PV firms can be blamed on greed, sloth, pride or any of the other deadly startup sins. But in tenKsolar's case, it appears that rampant inverter failures (from other vendors' equipment) are the cause of this company's imminent end. The firm was founded in 2008 as a builder of integrated PV panels with intra-module power conditioning in tandem with a reflector. The company started shipping in 2010 with a focus on commercial roofs. It designed a system which mated an illumination-agnostic solar panel and a novel wiring scheme. Innovations in PV-cell-to-PV-cell interconnections ensured there was no single point of failure, according to Dallas Meyer, the CTO and founder of tenKsolar, in a previous interview. We're talking 30 percent to 40 percent advantage in power harvesting and a far better LCOE, he said. Meyer no longer works at the company. In October 2015, tenKsolar had to reprogram or replace APsystems microinverters at about 100 installation sites in Minnesota, most of them residential. [updated] We provided tenKsolar with an inverter which met specifications they outlined, however we found that they were operating the product far outside the parameters of those specifications, said Chris Barrett, APsystems Director of Engineering and Technical Services. No other APsystems inverters have experienced similar issues. And just a year and a half ago, tenKsolar raised $25 million from Goldman Sachs, Kresge Foundation, Oaktree Capital Management and Greencoat Capital. Investors from earlier financing rounds included PrairieGold Venture Partners, ESB Novusmodus and Korea Hanwha. Since 2010, the firm has raised more than $60 million. TenKsolar claimed it has produced panels for more than 500 installations, with many in the 1-megawatt range. It partially constructs panels in China and completes them in Minnesota. At one point, tenKsolar employed more than 90 workers in its Bloomington factory. The CEO at the time, Joel Cannon, said the firm expected sales of $40 million in 2015 and $100 million in 2016. Last year, the company named Jeffrey Hohn, former GM of 3Ms renewable energy division, as CEO. Hohn and other executive staff have not responded to inquiries from GTM. We have heard from several sources close to the firm suggesting that microinverters, this time from a different vendor (Lead Solar), are the cause of a series of disastrous field failures. There were catastrophic potting failures on their Lead Solar 700 and 1400 inverters, and they're failing everywhere, said a source. Layoffs have impacted two-thirds of the staff, with the rest slated to be let go by the end of June. The company is selling off its inventory and looking for a buyer for its technology. EPC customers of tenKsolar are using Dow 832 sealant to seal existing Lead Solar 700 W and 1,400 W inverters that are failing from water intrusion owing to failed potting installation during manufacturing in China, a source said. TenK had a number of good design ideas but should have focused on one or two of those ideas, according to sources, who acknowledged the difficulty of popularizing a unique solar panel. GTM Research solar analysts and tenKsolar partners appeared to genuinely like the company's technology. Price point was a big issue, but in the end, inverter choices hastened tenKsolar's downfall. "
    #sentence = "Ciber Inc said Tuesday that it has received Ameri Holdings Inc's offer to buy the company at 75 cents per share, but said little else. On Monday, New Jersey-based Ameri Holdings, with its shares trading on the over-the-counter bulletin board at AMRH, said it would pay 75 cents per share for Ciber's outstanding shares. Shares in the Greenwood Village information technology company soared more than 100 percent in Monday trading, rising from 28 cents per share to close at 58 cents."
    #sentence = "Microsoft Corp on Monday announced it has reached an agreement to acquire GitHub, the world's leading software development platform where more than 28 million developers learn, share and collaborate to create the future. Together, the two companies will empower developers to achieve more at every stage of the development lifecycle, accelerate enterprise use of GitHub, and bring Microsoft's developer tools and services to new audiences. Microsoft is a developer-first company, and by joining forces with GitHub we strengthen our commitment to developer freedom, openness and innovation, said Satya Nadella, CEO, Microsoft. We recognize the community responsibility we take on with this agreement and will do our best work to empower every developer to build, innovate and solve the world's most pressing challenges. Under the terms of the agreement, Microsoft will acquire GitHub for $7.5 billion in Microsoft stock. Subject to customary closing conditions and completion of regulatory review, the acquisition is expected to close by the end of the calendar year. GitHub will retain its developer-first ethos and will operate independently to provide an open platform for all developers in all industries. Developers will continue to be able to use the programming languages, tools and operating systems of their choice for their projects - and will still be able to deploy their code to any operating system, any cloud and any device. Microsoft Corporate Vice President Nat Friedman, founder of Xamarin and an open source veteran, will assume the role of GitHub CEO. GitHub's current CEO, Chris Wanstrath, will become a Microsoft technical fellow, reporting to Executive Vice President Scott Guthrie, to work on strategic software initiatives. I'm extremely proud of what GitHub and our community have accomplished over the past decade, and I can't wait to see what lies ahead. The future of software development is bright, and I'm thrilled to be joining forces with Microsoft to help make it a reality, Wanstrath said. Their focus on developers lines up perfectly with our own, and their scale, tools and global cloud will play a huge role in making GitHub even more valuable for developers everywhere."
    print (sentence)
    sentence.encode('ascii', 'ignore')
    # Regex to divide a paragraph into sentences. The result is stored in a list.
    total_sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s',sentence)
    #print(total_sentences)
    totalNumberOfSentences = len(total_sentences)
    #totalNumberOfSentences = 4
    # if totalNumberOfSentences <= 3: #means we need to pass the batch only once
    #
    # else:

    #batchOfThreeSentences = []
    batchNumber = 3.0
    corefDictionaryWithEntity = defaultdict(list)
    finalList = []
    # Iterating over number of batches which can be generated with total number of sentences and batch size as 3.
    # change the batch number if needed to include more senteces in future.
    for i in range(totalNumberOfSentences - int(batchNumber) + 1):
        batchOfThreeSentences = []
        corefDictionaryWithEntity.clear()

        for y in range(i,i+int(batchNumber)):
            batchOfThreeSentences.append(total_sentences[y])

        print batchOfThreeSentences

        # This is to join the sentences of the list into a single sentence seperated by a space.
        sentence = ' '.join(batchOfThreeSentences)
        sentence.encode('ascii', 'ignore')
        # Output the json object which has coref as a key.
        output = nlp.annotate(str(sentence), properties={'annotators': 'dcoref',
                                                    'ner.useSUTime': 0,
                                                    'outputFormat': 'json'})
        # Structure of the JSON output is like "corefs" and inside each of it, there are different numbers for each set of corefs
        #print "output",output
        # numx has a json value which is inside the "corefs" key
        numx = output["corefs"]
        # Inside each coref, there are many values which are corelated and their properties are inside this tag value.
        # Iterate through the number of coreferences, it will be marked from 1,2,3... This numbers can be fetched using items()
        for numberOfCorefs, value in output["corefs"].items():
            #print ("keys",numberOfCorefs)
            # We will only look into those references where there are 2 or more interrelated referece. This API sometimes
            # output only one reference, which is of no use
            if len(numx[numberOfCorefs]) >= 2:
                tempList = []
                # Each required property is added in a tuple for each output tag, and this is further appened in a list for every coreference tag.
                for numberOfOccuranceOfEntity in range(len(numx[numberOfCorefs])):
                    tempTuple = (numx[numberOfCorefs][numberOfOccuranceOfEntity]['text'],numx[numberOfCorefs][numberOfOccuranceOfEntity]['sentNum']+i, numx[numberOfCorefs][numberOfOccuranceOfEntity]['startIndex'], numx[numberOfCorefs][numberOfOccuranceOfEntity]['endIndex'])
                    tempList.append(tempTuple)
                # this condition is to find out if the company name is present in any of the tuple in the list
                #[[set([3, u'the Technology Service Providers List']), set([3, u'its'])]] Eg for this list, there are two tuples, so we are checking if the company name is present in any of the tuple
                if companyName is not None:
                    for eachElementsInList in tempList:
                        if contains_word(eachElementsInList[0],companyName):
                            # Creating a dictionary : Key is coref number and Value is the list with desired properties(list has tuples)
                            corefDictionaryWithEntity[str(numberOfCorefs)].append(list(tempList))
                            CountingEntityoccurance(tempList)

                else:
                    corefDictionaryWithEntity[str(numberOfCorefs)].append(list(tempList))
                    CountingEntityoccurance(tempList)
        #print "Dictionary",corefDictionaryWithEntity
        # Using shallow copy because of pointer Issue while appending dictionary in list.
        # https://stackoverflow.com/questions/5244810/python-appending-a-dictionary-to-a-list-i-see-a-pointer-like-behavior
        finalList.append(corefDictionaryWithEntity.copy())
    #print("flist",finalList)
    #print ENTITYOCURRANCELIST
    GeneratingJsonObject2(ENTITYOCURRANCELIST, companyName)
    return str(list(output))




# If applying on the comments data in future using xml
# def ReadXML(file):
#     companyName = "TenKsolar"
#     wb = xlrd.open_workbook(file)
#     for rowNumber in range(5,6):
#         #Pass the rows and I am hardcoding the coulumn as 1. Change it according to the column needed in excel
#         firstSheet = wb.sheet_by_index(2)
#         actionVerbs = CorefWithEntity(firstSheet,rowNumber,firstSheet.row_values(rowNumber)[1], companyName)

def main():
    companyName = "Microsoft"
    with open("in.txt", "r") as f:
        sentences = f.read()
    CorefWithEntity(sentences, companyName)

    #print (wb.nsheets)

if __name__ == "__main__":
    main()