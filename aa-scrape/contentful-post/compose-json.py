from openpyxl import load_workbook
import json

file = load_workbook(filename='advisory-activities-v4-voice-updates-LWP.xlsx')
sheets = file.sheetnames

md = {
'Class Challenge': ['objective', 'materials', 'themes', 'prep', 'activityInstructions', 'introduction', 'steps', 'reflection', 'additionalSection', 'description'],
'Class Meeting': ['objective', 'themes', 'preparation', 'instructions', 'warm-up', 'discussion', 'reflection', 'description'],
'Service Learning':['objective', 'materials', 'themes', 'preparation', 'projectDescription', 'instructionsHeader', 'investigation', 'planning', 'action', 'reflection', 'demonstration', 'description']
}
allData = []
data = {}

def camelCase(string):
    string = ''.join(x for x in cell.value.title() if not x.isspace())
    return string[0].lower() + string[1:]

for sheet in sheets:
    headers = []
    line_count = 0
    for row in file[sheet].iter_rows():
        if sheet == 'Service Learning':
            data = {}

            # to limit the amount of activities processed
            if line_count > 3:
                break

            for cellIndex, cell in enumerate(row):
                if cell.value != None:
                    if line_count == 0:
                        headers.append(camelCase(cell.value))
                    else:
                        data[headers[cellIndex]] = {}
                        data[headers[cellIndex]]['en-US'] = cell.value
            if line_count > 0:
                if data != {}:
                    allData.append(data)
            line_count += 1
        with open('test-output.json', 'w') as f:
            f.write(json.dumps(allData))
