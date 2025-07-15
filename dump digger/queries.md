# Example queries

### Summarize the regex occurrences
```sql
SELECT regex, COUNT(*) AS occurrences
FROM regex_matches
GROUP BY regex
ORDER BY occurrences DESC
```

### Summarize the interesting files
```sql
SELECT category, COUNT(*) AS occurrences
FROM interesting_files
GROUP BY category
ORDER BY occurrences DESC
```


### Find all files with specific regex match
```sql
select DISTINCT * from regex_matches
where regex_matches.regex like "%JWT%"
```

### Find all "valid" IPv4 matches
```sql
select *
from regex_matches
where regex_matches.regex = "IPv4 Address"
and length(regex_matches.value) > 7
```

### Summarize all the extension for which there is no category
```sql
SELECT extension, COUNT(*) AS count
FROM inventory
WHERE (category == "" or category IS NULL)
GROUP BY extension
ORDER BY count DESC;
```

### Summarize inventory by extension
```sql
SELECT extension, COUNT(*) AS count
FROM inventory
GROUP BY extension
ORDER BY count DESC;
```

### Summarize inventory by category
```sql
SELECT COALESCE(category, 'Unknown') AS category, COUNT(*) AS count
FROM inventory
GROUP BY category
ORDER BY count DESC;
```