function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const getRules = async () => {
    return fetch('/getRules').then((response) => {
        return response.json();
    }).then((data) => {
        const rules = [];
        for(var i in data) {
            rules.push(data[i])
        }
        return rules;
    });

};

const updateRule = (rule) => {
    if(rule.is_active == 'true')
        rule.is_active = 'false';
    else
        rule.is_active = 'true';

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
};

const triggerCheck = async (eventItemId) => {
    const rules = await getRules();

    const currentRule = rules.find(rule => rule['id'] == eventItemId);
    if(!currentRule) {
        return;
    }

    updateRule(currentRule);
    await sleep(1000);
    window.location.reload(true);

}
