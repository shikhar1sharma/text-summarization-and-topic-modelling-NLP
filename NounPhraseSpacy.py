import xlrd
import xlwt
import spacy


def ExtractActionVerbsSRL(firstSheet, rowNumber, sentence):

    nlp = spacy.load("en_core_web_sm")
    sentence = "But seeing the key talent leaving the company is disheartening. We need better days & looking forward to it."
    doc = nlp(sentence)
    print (sentence)
    sentence.encode('ascii', 'ignore')


    actions = set()
    for i in doc.noun_chunks:
        actions.add(i)
    print (list(actions))
    return str(list(actions))




def ReadXML(file):
    #annotator = Annotator()
    wb = xlrd.open_workbook(file)
    #TO DO : Change it to add in the existing excel file
    newExcelFile = xlwt.Workbook()
    sheet1 = newExcelFile.add_sheet('Action_Verbs')
    for rowNumber in range(5,6):
        #Pass the rows and I am hardcoding the coulumn as 1. Change it according to the column needed in excel
        firstSheet = wb.sheet_by_index(0)
        actionVerbs = ExtractActionVerbsSRL(firstSheet,rowNumber,firstSheet.row_values(rowNumber)[1])
        sheet1.write(rowNumber,0,actionVerbs)
    newExcelFile.save('output_SRL_Verbs.xls')

def main():

    ReadXML('nigel_Comments.xls')

    #print (wb.nsheets)

if __name__ == "__main__":
    main()