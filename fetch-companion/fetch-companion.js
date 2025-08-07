/*CHANGE THESE*/
const SERVER  = "127.0.0.1"
const PORT    = "8081"

/*
Purpose:
parse files found in google dorking results, so that they can be downloaded later with wget, for further inspection
*/
function dorkFiles() {
    const url = `http://${SERVER}:${PORT}/dorkFiles`;

    FILES = getFilesLinks()

    // Data to be sent in the POST request
    const postData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"data":FILES}),
      mode: 'cors',
    };
  
    // Perform the fetch
    fetch(url, postData)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text()
      })
      .then(data => {
        console.log('POST request successful:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
}

function getFilesLinks() 
{
    // Get all the "a" tags on the page
    const anchorTags = document.getElementsByTagName('a');

    var extList = ["pdf","docx","doc","txt","xls","xlsx","xsl","xslx"]
    var hrefList = [];
  
    // Iterate through each "a" tag
    for (let i = 0; i < anchorTags.length; i++) 
    {
      const href = anchorTags[i].getAttribute('href');
  
      extList.forEach(element => 
      {
        if(href && href.endsWith(element))
        {
            hrefList.push(href)
        }
      });
    }

    return hrefList;
}
  
/*
Purpose:
extract all HREFs from google dorking results.
This can be useful in situations where you want to find folder paths your scanner can't find,
in order to perform a more precise folder/path enumeration
*/
function dorkHREFs() {
    const url = `http://${SERVER}:${PORT}/dorkHREFs`;

    FILES = getHREFLinks()

    // Data to be sent in the POST request
    const postData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"data":FILES}),
      mode: 'cors',
    };
  
    // Perform the fetch
    fetch(url, postData)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text()
      })
      .then(data => {
        console.log('POST request successful:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
}

function getHREFLinks() 
{
    // Get all the "a" tags on the page
    const anchorTags = document.getElementsByTagName('a');

    var hrefList = [];

    // Iterate through each "a" tag
    for (let i = 0; i < anchorTags.length; i++) 
    {
      const href = anchorTags[i].getAttribute('href');
      hrefList.push(href)
    }

    return hrefList;
}

// string to base64
function toBase64Unicode(str) {
  return btoa(unescape(encodeURIComponent(str)));
}

// used by gumpGlobals()
function removeCircularReferences(obj) {
  const seen = new Set();

  // Custom replacer function to handle circular references
  return JSON.stringify(obj, (key, value) => {
    if (value && typeof value === 'object') {
      if (seen.has(value)) {
        return '[Circular]';  // Replace circular reference with a placeholder
      }
      seen.add(value);  // Track the object we've already seen
    }
    return value;
  });
}



function dumpGlobals(){
  const url = `http://${SERVER}:${PORT}/dumpGlobals`;

  GLOBALS = toBase64Unicode(removeCircularReferences(globalThis))

  // Data to be sent in the POST request
  const postData = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"data":GLOBALS}),
    mode: 'cors',
  };

  // Perform the fetch
  fetch(url, postData)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.text()
    })
    .then(data => {
      console.log('POST request successful:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}