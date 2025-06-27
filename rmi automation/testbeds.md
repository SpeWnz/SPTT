# RMI Testbeds

It is possible to use the docker images provided officially by "qtc-de" on the RMG repository:
<br>
https://github.com/qtc-de/remote-method-guesser/tree/master/docker/example-server

Simply pull one of the three available versions with:

```
$ docker pull ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk8
$ docker pull ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk9
$ docker pull ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk11
```

Then run with "docker run", example:

```
docker pull ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk11
docker run ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk11
```

You may get an "out of memory" error, which can be fixed by issuing the following docker flag:

```
docker run --ulimit nofile=65536:65536 ghcr.io/qtc-de/remote-method-guesser/rmg-example-server:4.0-jdk8
```

When the docker is up and running, there will be 3 exposed targets:

```
172.17.0.2:9010
172.17.0.2:1090
172.17.0.2:1098
```

# Java versions

RMG and ysoserial need older java versions (Java 8, Java 11, and sometimes Java 17). They can be downloaded from Oracle:

<ul>
<li>Java 8: https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html</li>
<li>Java 11: https://www.oracle.com/java/technologies/javase/jdk11-archive-downloads.html</li>
<li>Java 17: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html</li>
</ul>