# Bambda cheatsheet

Some useful Bambda functions to use in Burp to filter specific results.


### Entries with "example" in url

```java
CharSequence content = "example";
return requestResponse.url().toLowerCase().contains(content);
```

### Entries with "example" in the response

```java
CharSequence content = "example";
return requestResponse.response().toString().contains(content);
```

### Entries with "example" in either request or response

```java
CharSequence content = "example";
return (requestResponse.response().toString().toLowerCase().contains(content) || requestResponse.request().toString().toLowerCase().contains(content));
```


### Search multiple strings in the response

For some reason burp raises an error but it works anyway

Match any of the patterns:
```java
CharSequence[] patterns = {"session","token","jwt"};
boolean match = false;
for (CharSequence p: patterns) {
		if (requestResponse.response().toString().toLowerCase().contains(p))
	    {
	        match = true;
	    }
}
return match;
```

Match all of the patterns:
```java
CharSequence[] patterns = {"session","token"};
boolean match = true;
for (CharSequence p: patterns) {
		if (!requestResponse.response().toString().toLowerCase().contains(p))
	    {
	        match = false;
	    }
}
return match;
```