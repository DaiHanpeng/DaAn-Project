import textract
import pdfminer


text = textract.process('Review_And_Edit.pdf', method='pdfminer')

print(text)