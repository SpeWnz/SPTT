function getTextByXPATH(xpath)
{
    const result = document.evaluate(xpath,document,null,XPathResult.FIRST_ORDERED_NODE_TYPE,null);
    const element = result.singleNodeValue;

    if (element)
    {
        return element.innerText;
    }
    else
    {
        console.error('Element not found with the provided xpath:', xpath);
        return null;
    }
}

function parseDorks()
{
    var result = "";
    i = 1;
    while (result != null)
    {
        xpath = "/html/body/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[" + i + "]/td[2]/a";

        result = getTextByXPATH(xpath);
        console.log(result);
        i++;
    }
}

