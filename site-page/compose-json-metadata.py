from openpyxl import load_workbook
import json

indexWorkbook = load_workbook(filename='scrape_sample.xlsx')
indexFile = indexWorkbook.active
# activitiesWorkbook = load_workbook(filename='advisory-activities.xlsx')

line_count = 0

page_metadata = []
for row in indexFile.iter_rows(min_row=1):
    if line_count > 0:
        new_page = {}
        for cell in row:
            if cell.column == 'B':
                new_page['title'] = cell.value
            if cell.column == 'C':
                new_page['gradeRange'] = cell.value
            if cell.column == 'D':
                new_page['product'] = cell.value
            if cell.column == 'F':
                new_page['audience'] = cell.value
        page_metadata.append(new_page)
    line_count += 1

with open('metadata.json', 'w') as f:
    f.write(json.dumps(page_metadata))
