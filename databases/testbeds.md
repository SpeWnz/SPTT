# Docker testbeds

Use these docker testbeds to test the tool

## Mongo DB

```
docker pull mongo
docker run --name mongo-db -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=example mongo --bind_ip_all
```

## PostgreSQL

```
docker pull postgres
docker run --name postgres-container -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=example -e POSTGRES_DB=your_database -p 5432:5432 postgres
```

## MySQL

```
docker pull mysql:latest
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=example -e MYSQL_DATABASE=your_database -p 3306:3306 mysql:latest
```

## Microsoft SQL (MSSQL)
Note, mssql requires a strong password or the docker image wont start


```
docker pull mcr.microsoft.com/mssql/server
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=example-P4ssw0rd' -p 1433:1433 --name sql_server mcr.microsoft.com/mssql/server
```

For ms-sql, the obdc driver will need to be installed. The microsoft documentation can be found here:
<br>
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline

```
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update -y
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18
```


## IBM DB2

The container for IBM DB2 needs additional flags to give privileged access as well as more memory and cpu power. Otherwise, errors may occur such as:

```
SQL1032N No start database manager command was issued. SQLSTATE=57019
```

A path for the volume must also be chosen. In this case "/tmp/docker-ibmdb2-stuff". The chosen path must also have the appropriate permissions:

```
docker pull ibmcom/db2
docker run --privileged=true --memory="4g" --cpus="2" --name=db2 -e DB2INST1_PASSWORD=yourpassword -e DBNAME=sampledb -e LICENSE=accept -p 50000:50000 -v /tmp/docker-ibmdb2-stuff:/database ibmcom/db2

sudo chmod -R 755 /tmp/docker-ibmdb2-stuff
```

When performing tests against an IBM DB2 instance, it is mandatory to specify the name of the database. Therefore it is assumed that one already knows this information. It is thus recommended to first perform enumeration using the <b>ibmdb2-enum-db.py</b> tool and eventually with the <b>ibmdb2-enum-user.py</b> tool.
Furtermore, it is important to keep in mind that IBM DB2 uses the host OS users as database users. 