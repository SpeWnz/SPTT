// copia questo nella console del browser
// come argomento metti la classe necessaria

function removePaywall(classToRemove)
{
    elements = document.querySelectorAll('*');
    elements.forEach(element => {
        element.classList.remove(classToRemove)
    });
}

removePaywall('NOME-CLASSE-QUI')