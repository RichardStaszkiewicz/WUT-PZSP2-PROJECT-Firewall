function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const enableAll = async () => {
    fetch('/getRules?action=enableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    await sleep(1000);
    window.location.reload(true);
}

const disableAll = async () => {
    fetch('/getRules?action=disableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    await sleep(1000);
    window.location.reload(true);
}

const savePush = async () => {
    fetch('/getRules?action=save', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(RULES)
    })
    await sleep(1000);
    window.location.reload(true);
}

const fetchLogs = async () => {
    fetch('/getRules?action=fetchLogs', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    await sleep(1000);
    window.location.reload(true);
}