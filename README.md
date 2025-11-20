# NOTAM Parsing Tool
Takes an XLS file of NOTAM data from https://notams.aim.faa.gov/notamSearch/

> [!WARNING]
> Can only classify obstruction NOTAMS currently

## Usage:
Call `python annotator.py examplesheet.xls`
This will output NOTAM.txt and finalannotations.json
You can check the results at https://arunmozhi.in/ner-annotator/ by putting in the output files
