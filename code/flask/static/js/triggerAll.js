function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const deleteRule = async (ruleId) => {
    const rule = RULES.filter((rule) => {
        return rule.id == ruleId
    });

    fetch('/getRules?action=deleteRule', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule)
    })
    await sleep(1000);
    window.location.reload(true);
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

const logout = async () => {
    fetch('/getRules?action=logout', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    await sleep(1000);
    window.location.reload(true);
}
