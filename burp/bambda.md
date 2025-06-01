# Bambda cheatsheet

Some useful Bambda functions to use in Burp to filter specific results.


### Entries with "example" in url

```
return requestResponse.url().toLowerCase().contains("example");
```

### Entries with "example" in the response

```
return requestResponse.response().toString().contains("example");
```