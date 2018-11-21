# tripsapp

The tripsapp folder contains all code for transforming a docx into a usable array of objects data store or better still an array of objects that can be populated into a data store of choice.

Features:
  - Conversion of .docx file to .json file
  - Conversion of .json to .docx file
  - Rest API based on Flask. Endpoints can:
    * Retrieve all records 
    * Update a record
    * Create new record
    * Delete a record
    
    
Endpoints:

* GET     
  - /api/v1/resources/records         ()-> Returns all records available
  - /api/v1/resources/records/api/v1/resources/records/docxfile   ()-> Downloads the most recent database records into a .docx file
* POST    
  - /api/v1/resources/records         ({record object})-> Returns status message | (Creates new entry // Denies new entry)
* PUT     
  - /api/v1/resources/records/{id}    (id)-> Returns status message | (Successful update // Fail)
* DELETE  
  - /api/v1/resources/records/{}      ({record object})-> Returns status message | (Deletes entry // Denies delete)    
