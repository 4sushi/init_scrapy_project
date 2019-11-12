"""
Script to init a scrapy project with a conda environment (python 3)

@author: mbouchet
"""

import subprocess
import sys
import os
from shutil import copyfile, move

print('\nInstallation steps:')


# check input params
if len(sys.argv) != 2:
    print("✗ Bad parameters, run 'python3 init_scrapy_project.py <srapy_project_name>")
    exit(1)
srapy_project_name = sys.argv[1]

# check conda is installed
process = subprocess.Popen('conda', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("✗ Check conda is installed \n\nError message:\nYou have to install and/or configure conda, refer to an administrator")
    exit(1)
print("✓ Check conda is installed")

# Create the project directory
try:
    os.mkdir(srapy_project_name)
except Exception as e:
    print("✗ Create the project directory \n\nError message:\n%s" % e)
    exit(1)
savedPath = os.getcwd()
newPath = os.path.join(savedPath, srapy_project_name)
os.chdir(newPath) # cd new directory    
print("✓ Create the project directory")

# Try to init git project
process = subprocess.Popen('git init', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("⛿ Try to init git project \n\nWarning message:\n%s" % stderr)
else:
    print("✓ Try to init git project")
f = open("readme.md","w+") # Create readme file
f.write('[EDIT]')
f.close()

# Install new conda env (if doesn't exist)
process = subprocess.Popen('conda info --envs', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("✗ Install new conda env (if doesn't exist) \n\nError message:\n%s" % stderr)
    exit(1)
elif b'\np3.6' not in stdout:
    process = subprocess.Popen('conda create --name p3.6 python=3.6 -y', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("✗ Install new conda env (if doesn't exist) \n\nError message:\n%s" % stderr)
        exit(1)
print("✓ Install new conda env (if doesn't exist)")

# Install scrapy, pymysql
process = subprocess.Popen('conda install scrapy pymysql -y', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("✗ Install scrapy, pymysql \n\nError message:\n%s" % stderr)
    exit(1)
print("✓ Install scrapy, pymysql")

# Init scrapy project
process = subprocess.Popen('scrapy startproject scrapy_%s .' % srapy_project_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("✗ Init scrapy project \n\nError message:\n%s" % stderr)
    exit(1)
print("✓ Init scrapy project") 

# Create spider
process = subprocess.Popen('scrapy genspider spider_%s example.com' % srapy_project_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if process.returncode != 0:
    print("✗ Create spider \n\nError message:\n%s" % stderr)
    exit(1)
print("✓ Create spider 'spider_%s'" % srapy_project_name) 

# Copy files to scrapy project
try:
    copyfile(os.path.join(savedPath, 'files', 'init.sql'), 'scrapy_%s/init.sql' % srapy_project_name)
    copyfile(os.path.join(savedPath, 'files', 'run.sh'), os.path.join(newPath, 'run.sh'))
    copyfile(os.path.join(savedPath, 'files', 'gitignore'), '.gitignore')
    copyfile(os.path.join(savedPath, 'files', 'conf.json'), 'scrapy_%s/conf.json' % srapy_project_name)
    copyfile(os.path.join(savedPath, 'files', 'conf.json'), 'scrapy_%s/conf_default.json' % srapy_project_name)
    copyfile(os.path.join(savedPath, 'files', 'pipelines.py'), 'scrapy_%s/pipelines.py' % srapy_project_name)
    copyfile(os.path.join(savedPath, 'files', 'spider.py'), 'scrapy_%s/spiders/spider_%s.py' % (srapy_project_name, srapy_project_name))
except Exception as e:
    print("✗ Copy files to scrapy project\n\nError message:\n%s" % e)
    exit(1)
print("✓ Copy files to scrapy project") 


# Edit files scrapy
try:
    SPIDER_NAME = 'spider_%s' % srapy_project_name
    CLASS_NAME = ''.join([x.capitalize() for x in srapy_project_name.split('_')])
    PROJECT_NAME = 'scrapy_%s' % srapy_project_name
    # edit spider
    with open('scrapy_%s/spiders/spider_%s.py' % (srapy_project_name, srapy_project_name), 'r') as f :
        filedata = f.read()
    filedata = filedata.replace('$PROJECT_NAME$', PROJECT_NAME)
    filedata = filedata.replace('$CLASS_NAME$', CLASS_NAME)
    filedata = filedata.replace('$SPIDER_NAME$', SPIDER_NAME)
    with open('scrapy_%s/spiders/spider_%s.py' % (srapy_project_name, srapy_project_name), 'w') as f :
        f.write(filedata)
    # edit pipeline
    with open('scrapy_%s/pipelines.py' % (srapy_project_name), 'r') as f :
        filedata = f.read()
    filedata = filedata.replace('$CLASS_NAME$', CLASS_NAME)
    with open('scrapy_%s/pipelines.py' % (srapy_project_name), 'w') as f :
        f.write(filedata)
    # edit run.sh 
    with open('run.sh', 'r') as f :
        filedata = f.read()
    filedata = filedata.replace('$SPIDER_NAME$', SPIDER_NAME)
    with open('run.sh', 'w') as f :
        f.write(filedata)
except Exception as e:
    print("✗ Edit files scrapy\n\nError message:\n%s" % e)
    exit(1)
print("✓ Edit files scrapy") 

# Try to commit the project with git
process = subprocess.Popen('git add .', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
process2 = subprocess.Popen('git commit -m "init project"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process2.communicate()
if process.returncode != 0 or process2.returncode != 0:
    print("⛿ Try to commit the project with git \n\nWarning message:\n%s" % stderr)
else:
    print("✓ Try to commit the project with git")

os.chdir(savedPath) # Return current directory

# Move the directory of the project to the parent dir
try:

    move(srapy_project_name, os.path.join(os.path.dirname(os.getcwd()), srapy_project_name))
    print(os.getcwd())
    print(srapy_project_name, os.path.join(os.path.dirname(os.getcwd()), srapy_project_name))
    print("✓ Move the directory of the project to the parent dir")
except Exception as e:
    print("⛿ Move the directory of the project to the parent dir \n\nWarning message:\n%s" % e)


print('\nDev steps:')
print('➤ Edit the configuration file with your database settings in %s/scrapy_%s/conf.json' % (srapy_project_name, srapy_project_name))
print('➤ Run the script %s/scrapy_%s/init.sql in your database' % (srapy_project_name, srapy_project_name))
print('➤ Write the code of your spider in %s/scrapy_%s/spiders/spider_%s.py' % (srapy_project_name, srapy_project_name, srapy_project_name))
print('➤ Edit the item class to add the attributs that you want to save in %s/scrapy_%s/items.py' % (srapy_project_name, srapy_project_name))
print('➤ Create a table on mysql to store your data, add the request CREATE to the file %s/scrapy_%s/init.sql' % (srapy_project_name, srapy_project_name))
print('➤ Edit the pipelines class to save yours items in the database %s/scrapy_%s/pipelines.py' % (srapy_project_name, srapy_project_name))
print('➤ Edit the readme.md file, add description and important information about the project')
print('When the project is finished:')  
print('➤ Commit/push your project in this new repository')


print('\n\nInformation:')
print('➤ To install a package, run the command "conda activate p3.6 && conda install <package>"')
print('➤ To run the scraping, you can use the shell script "./run.sh"')
print('➤ If you have to change some settings, do not change in the file "settings.py". Set it in the spider, in the variable "custom_settings"')
print('➤ If you have to add fields in conf.json, add this fields in conf_default.json with a default value\n  (do not put your real ip/login/password in the default file).')
print()
