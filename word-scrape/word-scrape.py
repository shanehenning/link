import docx

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    print('doc: ', doc)
    for para in doc.paragraphs:
        fullText.append(para.text)
        return '\n'.join(fullText)

print(getText('Class Meeting Section List.docx'))
