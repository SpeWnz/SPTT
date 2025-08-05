# Useful Powershell one-liners

## Alias
Powershell does not feature "alias" like in linux. However we can mimic this by using the "function" keyword.

Behave like fish shell:
```ps1
function ll{ls -force}; function ..{cd ..}
```


## Files 
### File names

Search a specific file by specifing the filename and the starting folder:

```ps1
Get-ChildItem -Path C:\ -Recurse -File | Where-Object { $_.Name -like "something.txt" }
```

Search all powershell history files
```ps1
Get-ChildItem -Path C:\ -Recurse -File | Where-Object { $_.Name -like "ConsoleHost_history.txt" }
```

Search all files that end with a specific extension:

```ps1
Get-ChildItem -Path C:\ -Recurse -File | Where-Object { $_.Name -like "*.log" }
```

Search all files that do not end with one or more specific extensions:
```ps1
Get-ChildItem -Force | Where-Object { $_.Name -notmatch "\.dll|\.exe|\.png|\.ico|\.sys|\.ax" }
```

### File contents

Search through the contents of files recursively starting from the current pwd (similar to linux <code>grep -rnwi . -e "something"</code>):
```ps1
Get-ChildItem -Recurse -File | Select-String -Pattern "\bsome content here\b" -CaseSensitive:$false | ForEach-Object {"$($_.Path):$($_.LineNumber):$($_.Line)"}
```
<b>NOTE:</b> Since it also prints out the content of the line, the output may be very large. To work around this, it is possible to omit the <code>$($_.Line)</code> part and only print out the path and line number.

Search multiple texts through the contents of files recursively, starting from the current pwd, but only in files with specific extensions. Also, print unique results:
```ps1
$patterns = @('\bpassword\b','\bjohnny\b','\bjohanna\b'); Get-ChildItem -Recurse -Include *.txt,*.ini,*.log,*.cfg,*.xml,*.conf,*.bat -File | Select-String -Pattern $patterns -CaseSensitive:$false | Select-Object -ExpandProperty Path -Unique
```

### Archives

Compress a file or a folder into a zip archive
```ps1
Compress-Archive -Path "C:\Path\To\Source" -DestinationPath "C:\Path\To\Archive.zip"
```


## Services
### Service specific properties

Select the name and the start mode of a service whose name is "backup"

```ps1
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like 'backup'}
```

Select the name, state, and the path, of a service whose state is "Running"

```ps1
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```