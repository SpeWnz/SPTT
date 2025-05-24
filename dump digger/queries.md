# Example queries


### Summarize the regex occurrences

```
SELECT regex, COUNT(*) AS occurrences
FROM regex_matches
GROUP BY regex
ORDER BY occurrences DESC
```

### Summarize the interesting files

```
SELECT category, COUNT(*) AS occurrences
FROM interesting_files
GROUP BY category
ORDER BY occurrences DESC
```


### Find all files with specific regex match

```
select DISTINCT * from regex_matches
where regex_matches.regex like "JWT"
```

### Find all "valid" IPv4 matches

```
select *
from regex_matches
where regex_matches.regex = "IPv4 Address"
and length(regex_matches.value) > 7
```
