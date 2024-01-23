// this is just a test to get all the pdf links in the href tags

function printHrefByExtension(extension) {
    // Get all the "a" tags on the page
    const anchorTags = document.getElementsByTagName('a');
  
    // Iterate through each "a" tag
    for (let i = 0; i < anchorTags.length; i++) {
      const href = anchorTags[i].getAttribute('href');
  
      // Check if the "href" contains the specified extension
      if (href && href.endsWith(`.${extension}`)) {
        console.log(href);
      }
    }
  }
  
printHrefByExtension('pdf');
  