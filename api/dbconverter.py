import docx
import json
import os

# Directory Path
dirpath = os.getcwd()


def convert_to_json(filename):
    """
    Convert from DOCX to JSON
    :param filename: .docx file
    :return: .json file
    """
    document = docx.Document(filename)
    document_to_json = []
    docs = []

    # Read .docx file line by line
    for row in range(0, len(document.paragraphs)):
        if row == 0:
            # Handle first row as header
            header = [x.lower()
                      for x in document.paragraphs[row].text.split("\t") if x]
        else:
            # Handle the rest of the rows
            current_row = [
                x for x in document.paragraphs[row].text.split("\t") if x]
            # If column lengths don't match, we cant parse -> lets get out of here
            if len(header) != len(current_row):
                return print("Cannot parse document")
            document_to_json.append(dict(zip(header, current_row)))

    for a in range(0, len(document_to_json)):
        # Add an extra field to data to serve as primary key
        document_to_json[a]['primaryid'] = a+1
        docs.append(document_to_json[a])
    filepathnamewext = '' + filename[:-5] + '.json'

    # Write to json
    with open(filepathnamewext, 'w') as fp:
        json.dump(docs, fp)
    return docs


def convert_to_docx(filename):
    """
    Convert from JSON to DOCX
    :param filename: .json file
    :return: .docx file
    """
    k = json.loads(open(filename).read())
    document = docx.Document()
    font = document.styles['Normal'].font
    font.name = 'Arial'

    paragraph = document.add_paragraph()

    # Create header
    paragraph.add_run("{}\t{}\t{}\t{}\t{}\t{}".format(
        "Id", "datetime", "description", "longitude", "latitude", "elevation"))
    for product in k:
        p = document.add_paragraph()
        for i in (0, len(product)):
            id = product['id']
            datetime = product['datetime']
            description = product['description']
            elevation = product['elevation']
            latitude = product['latitude']
            longitude = product['longitude']
            # Add each json object as individual lines
            p.add_run(
                "{}\t{}\t{}\t{}\t{}\t{}".format(id, datetime, description, longitude, latitude, elevation))
            break
    # Save as .docx file
    document.save(dirpath+'/files/input.txt.docx')


# Convert to .docx
toDocxfile = dirpath+'/files/input.txt.json'
convert_to_docx(toDocxfile)
