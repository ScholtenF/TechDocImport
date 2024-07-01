import os
import pymupdf
# pip install pymupdf

# globals
# Dictionary filename[fieldname] (value)
extracted_data = {}
current_filename = None
current_template = None
page_template_fieldnames = {}
SEPARATOR = ";"
NEWLINE = "\n"

def revisionValidator(text):
    return "Revision" in text

def revisionFormatter(text):
    return removeAll(text, ["Revision", "\n"])

def removeAll(text, fragments, replace_by = ""):
    result = text
    for fragment in fragments:
        result = result.replace(fragment, replace_by)
    return result

def readTemplates(template_data, template_dir):
    template_files = os.listdir(template_dir)
    for template_file in template_files:
         full_filename = os.path.join(template_dir, template_file)
         readTemplate(template_data, full_filename, template_file)

def readTemplate(template_data, fileName, name):
    document = pymupdf.open(fileName)
    template_data[name]={}
    for page in document:
        fieldAnnottations = getFieldAnnotations(page)
        if fieldAnnottations:
            template_data[name][page.number] = fieldAnnottations
    document.close()

# See https://pymupdf.readthedocs.io/en/latest/annot.html
def getFieldAnnotations(page):
        results = {}
        for annot in page.annots():
            if annot.type[1] == "Square": # Annotation must be a rectangle
                fieldname = annot.info["title"]  # Author text used as fieldname, can be set using PDF reader like Okular
                results[fieldname] = {}
                results[fieldname]["area"] = annot.rect
        return results

def extractData(fileName, template_data):
    document = pymupdf.open(fileName)
    current_filename = fileName
    extracted_data[current_filename]={}  
    for template in template_data:
        global current_template
        current_template = template
        for page in document:
            page_number = page.number
            if page_number in template_data[template]:
                global page_template_fieldnames
                page_template_fieldnames = template_data[template][page_number]
                for page_field in page_template_fieldnames:
                    foundText = page.get_text("text", page_template_fieldnames[page_field]["area"])
                    if foundText:
                        field_is_valid = True
                        if page_field in field_validators:
                            field_is_valid = field_validators[page_field](foundText)
                        if field_is_valid:
                            if page_field in field_formatters:
                                foundText = field_formatters[page_field](foundText)    
                            extracted_data[current_filename][page_field]=foundText
        if len(extracted_data[current_filename]) > 0:
            break

def extractDataFromFolder(folder, template_data):
    files = os.listdir(folder)
    for filename in files:
        full_filename = os.path.join(folder, filename)
        extractData(full_filename, template_data)

def createCSV(extractedData):
    fieldnames = {}

    for item in extractedData:
        for field in extractedData[item]:
            if not (field in fieldnames):
                fieldnames[field]=field
    result = "filename" + SEPARATOR
    for fieldName in fieldnames:
        result += fieldName + SEPARATOR
    result += NEWLINE
    for item in extractedData:
        result += item + SEPARATOR
        for fieldName in fieldnames:
            value = ""
            if fieldName in extractedData[item]:
                value = extractedData[item][fieldName]
            result += value + SEPARATOR            
        result += NEWLINE
    return result

template_data = {}
field_validators = {}
field_formatters = {}
field_validators["revision"]=revisionValidator
field_formatters["revision"]=revisionFormatter

readTemplates(template_data, r".\\templates")

#print(template_data)
extractDataFromFolder(r".\\input", template_data)

#print(extracted_data)
csv = createCSV(extracted_data)
print(csv)