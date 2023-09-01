# database_integration_api

## Build

`docker-compose up`
Docker Compose file creates the API service and Database with all tables that will be used in this project. 

## Usage

The API has 3 routes:

### UPLOAD

**POST /upload/<table>**
This method uploads a csv file into the desired table in DB. To use it you need to provide the CSV file in field `csv_data` using Multipart Form.

Table valid values: `jobs`, `departments`, `employees`.

CURL Example:
```
curl --request POST \
  --url http://HOST/upload/jobs \
  --header 'Content-Type: multipart/form-data' \
  --form 'csv_data=path/jobs.csv'
```

### TRUNCATE

**DELETE /truncate/<table>**
This method truncate the desired table. No body data is required for this method.

Table valid values: `jobs`, `departments`, `employees`.

CURL Example:
```
curl --request DELETE \
  --url http://HOST/truncate/departments
```

### QUERY

**GET /query/<query>/<year>**
This method returns the result of a query in csv format. You need to provide in path the number of the query(1 or 2) and the year. No body data is required for this method.

There are 2 queries to be used in this method:
- **1** - Number of employees hired for each job and department in the selected year divided by quarter. Ordered alphabetically by department and job.
- **2** - Number of employees hired of each department that hired more employees than the mean of employees hired in selected year for all the departments, ordered
by the number of employees hired.

CURL Example:
```
curl --request GET \
  --url http://HOST/query/1/2021
```
