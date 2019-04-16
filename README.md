# Sane Doc Reports by [Demisto](https://demisto.com)

An extension to [sane-reports](https://github.com/demisto/sane-reports), 
> *"keep you sane and not pulling your hair out while generating DOCX reports"*

## Installation
*This project uses Python 3*  
`pipenv install sane-doc-reports`

## Usage
**CLI**  
First, generate a JSON file with the sane-reports repo.
```sh
$ sane-doc some.json -w out.docx # Not implemented yet. Use the library.
```

**Library**
```
import sane_doc_reports
```

## Development
1) Install the mypy addon for your IDE
2) Dev:
```sh
$ pipenv shell
$ pytest # For testing
$ pytest --cov=sane_doc_reports # For coverage
```

### Generating JSON files
1) Start a new demisto server with: `report.remove.data=false`
2) Go to the reports, generate a desired report
3) Get the json from `<demisto_path>/debug/lib/temp`

To check how it looks in the sane-reports:
1) Change the `incidentDailyReportTempalte.json` file with the json from the last step (in `lib/temp`)
2) `npm run start`
3) To mark the tables there you can open the console and add this:
```js
document.body.innerHTML += "<style>.report-layout .react-grid-layout .react-grid-item{border: 1px solid grey;}</sctyle>"
```

### How to add new docx elements (text, tables, charts...)
1) Create a file in the sane_doc_reports/docx folder with the same name as the 
type in the sane json file.
2) Every docx element should implement a `insert(cell_object, section):` function.
The function needs to create the elements into the cell_object file.