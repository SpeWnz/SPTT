# Dump Digger
<i>Dump Digger</i> (for lack of a better name) is a tool i wrote to dig and extract useful information from dumps (i.e. large folders, exfiltrated data, etc...). It can extract tokens, passwords, api keys, etc...

I highly recommend running it inside a container, as several stuff needs to be installed (which you might not want in your specific system).

Please follow the instructions below to build the container.


## Containered install and usage

1. Build the "base image" using the prodived dockerfile
```
docker build --tag "spewnz/dump-digger-base" .
```
2. Create and execute the container with the following command. Replace "/your-folder" with the folder you want share with the host. That folder is where you'll place the files you want to analyse:
```
docker run -d -v /your-folder:/shared-folder --name "dump-digger-base" "spewnz/dump-digger-base"
```
3. Step inside the running container with:
```
docker exec -it "dump-digger-base" /bin/bash
```
4. Run the install script
```
cd _INSTALL/
chmod +x container-install.sh
./container-install.sh


(oneliner)
cd _INSTALL/; chmod +x container-install.sh; ./container-install.sh
```

5. You may now stop the container and restart it later if needed
```
docker stop dump-digger-base
docker start dump-digger-base
```

When you need to analyse files, just repeat step 3 to get into the container and execute the script as needed. Of course, it would make sense to output the results db in the shared folder, to access it later.


## Usage

Example usage
```
python3 main.py -f /shared-folder/some-folder-to-analyse/ -t 10 -o /shared-folder/example-output.db 
```

<i>Dump Digger</i> looks for information based on either matching words in the <code>wordlist.txt</code> file, or matching regex content specified in the <code>core/regexes.py</code> file. You may change and fine-tune both of the files accordingly to your needs.


<i>Dump Digger</i> can take either a folder path to analyse, or a list of files (where each line is a path of a file to analyse). In cases where you are analysing very large folders with lots of files, it would be ideal to create the list of files prior to launching the script. This way, the script does not need to re-create the file list every time the script is launched.
```
find {starting path} -type f > list_of_files.txt
python3 main.py -f list_of_files.txt -t 10 -o /shared-folder/example-output.db
```