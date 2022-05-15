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
    rule.is_active = !rule.is_active;

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

    const checkBtn = document.getElementById(eventItemId);

    checkBtn.onclick = () => {
        updateRule(currentRule);
        window.location.reload(true);
    }

}
