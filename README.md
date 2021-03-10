# Set up #

### 1. Creation of databases ###
   First of all you'll need to create a local instance of two databases: SQL and Neo4j
   #### SQL ####
   * Create a db called 'sna_tool'
       ```create database sna_tool;```
   * Create two tables called 'users' and 'word_frequency'. Use the commands below to do this quickly 
      ````
      CREATE TABLE `users` (
        `mail` varchar(30) NOT NULL,
        `password` varchar(30) NOT NULL
      );

      CREATE TABLE `word_frequency` (
        `word` varchar(500) NOT NULL,
        `value` varchar(10) NOT NULL,
        `user Profile Property` varchar(45) NOT NULL,
        `User Registered on SNA` varchar(45) NOT NULL,
        `Social Network` varchar(45) NOT NULL
      ) ;

      alter table word_frequency change word word varchar(500) character set utf8;
      ````   
   #### Neo4j ####
   * Install JDK on your machine. (I used jdk-8u221)
   * Then download the community edition of Neo4j. You can do this [here](https://neo4j.com/download-center/#community). After that you have download this, you need to enable apoc module in Neo4j.
   * Download apoc module [here](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases). (I used apoc-3.5.0.5)
   * To enable apoc, put the ```apoc-x.x.x.jar``` into ```/neo4j/plugins/``` path. Then go into ```/neo4j/conf/``` path and modify ```neo4j.conf``` as follow
   ````
   ...
   dbms.directories.plugins=/path/where/you/have/neo4j-community-3.5.18/plugins
   ...
   dbms.security.procedures.unrestricted=algo.*,apoc.* 
   ...
   dbms.security.procedures.whitelist=apoc.*
   ...  
   ````
### 2. Environment setting ###

   * Install anaconda, find instruction (https://docs.anaconda.com/anaconda/install/). Alternatively you could install miniconda for python 2.7 according to you OS. Download from [here](https://docs.conda.io/en/latest/miniconda.html)
   * Create an env using the command ``` conda create --name (env_name)```, then activate it
   * Install pip according to your OS. Instruction [here](https://pip.pypa.io/en/stable/installing/)
   * Install the following package using the comand ```pip install```:
        - mysql-connector 2.2.9
        - nltk 3.4.5
        - numpy 1.9.0
        - pandas 0.22.0
        - py2neo 4.3.0
        - scikit-learn 0.22.4
        - scipy 1.2.3 
        - sklearn
   * Install Pear package manager. You can find instruction [here](https://pear.php.net/manual/en/installation.getting.php)
        - Install mail_mbox. More information [here](https://pear.php.net/package/Mail_Mbox/download)
        - Install mail_mimeDecode. More information [here](https://pear.php.net/package/Mail_mimeDecode/)
   * Modify into ```php.ini```  the lines below to allow the file upload :
   `````
   ; Maximum allowed size for uploaded files.
   upload_max_filesize = 500M

   ; Must be greater than or equal to upload_max_filesize
   post_max_size = 500M
   `````

### 3. Set variable inside the code ###
   * Need to set the password (and the host) into ```/server/dbConnector.py```
   ````
   def neo4jHelper():
    return Graph(host='localhost:7687', auth=('neo4j', '*******'))

   def sqlHelper():
    return mysql.connector.connect(
        user='root',
        password='*******',
        host='127.0.0.1',
        database='sna_tool'
    )
   ````
   * If you have some problem with the installed packages, you should modify the path using absolute path in ```sys.path.append()``` into python scripts or mbox.php and mimeDecode.php path into ```server.php```

# The Application #

This application allows the analysis of social network data such as mbox files, Facebook, and Twitter profile dumps.

<img width="712" alt="Schermata" src="https://user-images.githubusercontent.com/33377086/110707247-4fc3bd80-81f9-11eb-90b7-a64d35b709ce.png">

The GUI is divide into four section  
   1. Filter option
   2. Main area
   3. Second area
   4. Drawer


