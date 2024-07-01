# Import PDF Data 

## Summary

- extract metadata from PDF files using templates to define areas to extract metadata info
- used to extract revision from technical drawings

## Basic operation

- make sure pymupdf is installed
    `pip install pymupdf`
- in templates folder add examples of PDF to extract metadata from
- mark metadata in template PDF by adding an annotation of type 'Rectangle'
- use properties of the annotation and change the field of 'Author' to the name of the field the region contains (example: revision)
- to validate the field content, include the header text so a validator function can be used to check on its presence 

- optionally: in the script add a validator function for the field to which gets the value and returns true/false depending on if the input value is valid 
- optionally: in the script register a formatter function to remove/trim the value for example to clean-up line endings, field headers etc

## Examples:

In templates folder two PDFs have a annotation for the revision field.
With the test data the result should output:

```csv
filename;revision;
.\\input\0210309-24.PDF;01;
.\\input\0231009-01.PDF;03;
```
