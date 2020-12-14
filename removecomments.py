
# remove comments.py
# to remove comments from pdf file, make a temporary file and then delate it after processing
import PyPDF2
import pytesseract
import pdf2image
import yaml

settingsFile = "settings.yml"
settings = yaml.safe_load(open(settingsFile))

memexPath = settings["memex_path"]

#citationkey = "baggeOldNorseKings2016"
# remove comments from pdfs
def removeCommentsFromPDF(pathToPdf):
    with open(pathToPdf, "rb") as pdf_obj:
        pdf = PyPDF2.PdfFileReader(pdf_obj)
        out = PyPDF2.PdfFileWriter()
        for page in pdf.pages:
            out.addPage(page)
            out.removeLinks()
        tempPDF = pathToPdf.replace(".pdf", "_TEMP.pdf")
        with open(tempPDF, "wb") as f:
            out.write(f)
    #print("done!")
    return(tempPDF)