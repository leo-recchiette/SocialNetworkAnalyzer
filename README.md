# Run with Docker (recommended) #

The whole stack — the app (PHP + Python 2.7), Neo4j, and MySQL — can be started
with a single command, no manual setup required:

```bash
docker compose up --build
```

Then open http://localhost:8080. See **[DOCKER.md](DOCKER.md)** for details
(ports, default credentials, persistence, troubleshooting).

The manual setup below is only needed if you want to run the app **without**
Docker.

---

# Set up (manual / without Docker) #

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
   * Install the Python dependencies with `pip install -r docker/requirements.txt`. That file is the authoritative, last-Python-2.7-compatible set (some of the older versions originally listed here cannot install on Python 2.7). It pins:
        - numpy 1.16.6
        - scipy 1.2.3
        - pandas 0.24.2
        - scikit-learn 0.20.4
        - nltk 3.4.5
        - requests 2.27.1
        - mysql-connector-python 8.0.23
        - py2neo 4.3.0 (installed from its git tag — it was removed from PyPI)
   * After installing nltk, download the corpora it uses: `python -m nltk.downloader stopwords punkt`
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

### 3. Set the database credentials ###
   `/server/dbConnector.py` reads its connection settings from environment
   variables (with localhost defaults), so you no longer edit the file — export
   the values your local Neo4j/MySQL use:
   ````
   export NEO4J_HOST=localhost NEO4J_PORT=7687 NEO4J_USER=neo4j NEO4J_PASSWORD=yourpassword
   export MYSQL_HOST=127.0.0.1 MYSQL_PORT=3306 MYSQL_USER=root MYSQL_PASSWORD=yourpassword MYSQL_DATABASE=sna_tool
   ````
   The browser no longer connects to Neo4j directly, so there is **no separate
   frontend password to set**: the graph visualization's Cypher is proxied
   through `server.php` (`action: runQuery`) to
   `server/dataSearcher/runVizQuery.py`, which uses the same env-driven
   `server/dbConnector.py`.

   * If you have some problem with the installed packages, set `PYTHONPATH` to include `server/` and `server/dataSearcher/nlp/` (the `sys.path.append('~/...')` lines in the scripts do not work — `~` is not expanded). Also check the `mbox.php`/`mimeDecode.php` (PEAR) include path used by ```server.php```.

### 4. Build and serve the frontend ###
   The UI is a **React + Mantine** app under [`frontend/`](frontend/), built
   with Vite. Build it and serve the static output together with `server.php`
   from a single PHP docroot:
   ````
   cd frontend
   npm install
   npm run build          # outputs to dist/
   cd ..
   php -S localhost:8000  # serve dist/ + server.php + server/ from one docroot
   ````
   For frontend-only work you can instead run `npm run dev`, which proxies
   `/server.php` to a running Docker stack on `:8080` (see
   [frontend/vite.config.js](frontend/vite.config.js)).

# Sample dataset #

The [`dataset/enron/`](dataset/enron/) folder ships two ready-to-use mailbox
dumps for quick, preliminary tests — no need to export your own data first.
They are subsets of the public **Enron email corpus** in `.mbox` format, so the
app routes them to the mbox uploader (`mboxDumpUploader.py`) automatically (the
dispatcher picks the dumper by file extension / name).

| File | Mailbox (`X-Origin`) | Messages | Size | Date span |
| --- | --- | --- | --- | --- |
| `mbox-enron-white-s-all.mbox` | Sally White (`WHITE-S`) | ~3,266 | 6.0 MB | 29 Nov 2000 – 6 Feb 2002 |
| `mbox-enron-smith-m-all.mbox` | Matt Smith (`SMITH-M`) | ~1,642 | 3.1 MB | 1 Aug 2000 – 8 Jan 2002 |

To try one, start the stack, register/log in, and upload the `.mbox` file
through the app's upload form. Once it has been loaded into Neo4j you can
explore its relationship/traffic networks, map, timeline, and word frequency.

> **Note:** the date sliders/filters only return results inside each dump's date
> span shown above — filtering to a window outside it yields an empty graph.

# The Application #

This application allows the analysis of social network data such as mbox files, Facebook, and Twitter profile dumps.

<img width="712" alt="Schermata" src="https://user-images.githubusercontent.com/33377086/110707247-4fc3bd80-81f9-11eb-90b7-a64d35b709ce.png">

The GUI is divide into four section  
   1. Filter option
   2. Main area
   3. Second area
   4. Drawer


