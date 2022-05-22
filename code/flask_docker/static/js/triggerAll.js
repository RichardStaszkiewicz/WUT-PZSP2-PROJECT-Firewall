const enableAll = () => {
    fetch('/getRules?action=enableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    window.location.reload(true);
}

const disableAll = () => {
    fetch('/getRules?action=disableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    window.location.reload(true);
}

const savePush = () => {
    fetch('/getRules?action=save', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(RULES)
    })
    //window.location.reload(true);
}