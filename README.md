
Python 3 used in this project 

Setup Steps: 

(1) Install Linux Virtual Machine on local computer by installing these two software packages: \

a. [virtualbox](https://www.virtualbox.org/wiki/Downloads) 

b. [vagrantup](https://www.vagrantup.com/downloads.html) 
 
(2) It is recommended to have a Unix-style terminal such as Git Bash, so install that too. 

(3) From the terminal, make a new directory called 'networking' and to activate the vagrant program, run with these commands:
              
              mkdir networking
              cd networking
              vagrant init ubuntu/trusty64
              vagrant up
              
(4) This previous step could take awhile depending on internet connection. When complete, run:

              vagrant ssh
    
This connects to the vagrant virtual machine.
              
(5) Run:
       
       sudo apt-get update && sudo apt-get upgrade

This makes sure everything is up to date. 

(6) Run: 

       cd /vagrant

(7) Download [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip, and store newsdata.sql in the vagrant folder in the virtual machine. 

(8) Run: 

       psql -d news -f newsdata.sql' to create news database

(3) Run: 

       psql -d news' 
to connect to the news database


(5)Run: 
       
       python news.py 
         
