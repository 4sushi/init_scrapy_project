# Init scrapy project

Script to init a scrapy project with a conda environment (python 3)
For Linux only. 


## How it works ?

Steps :

* Check if conda is installed
* Create the project with a conda environment 
* Install scrapy + pymysql package
* Create scrapy project + 1 spider
* Init git for the project, commit 

## Run

```
python3 init_scrapy_project.py <project_name>
```