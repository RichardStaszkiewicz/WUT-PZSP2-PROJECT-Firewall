//modal
const addRuleModal = document.getElementById('addRuleModal')
const openModalBtn = document.getElementById('addRule');
const closeModalBtn = document.getElementById('closeAddRuleModal')


openModalBtn.onclick = () => {
    addRuleModal.style.display = "flex";
}

closeModalBtn.onclick = () => {
    addRuleModal.style.display = 'none';
}

window.onclick = (event) => {
    if (event.target == addRuleModal) {
        addRuleModal.style.display = 'none';
    }
}

//inputs 
const addRuleBtn = document.getElementById('confirmAddRule');

addRuleBtn.onclick = () => {
    const ruleName = document.getElementById('ruleName').value;
    const ruleProtocol = document.getElementById('ruleProtocol').value;
    const ruleSource = document.getElementById('ruleSource').value;
    const ruleDestination = document.getElementById('ruleDestination').value;
    const ruleDestinationPort = document.getElementById('ruleDestinationPort').value;
    //const ruleExpectedValue = document.getElementById('ruleExpectedValue').value;
/*
    const rule = {
        name: ruleName,
        protocol: ruleProtocol,
        profile: ruleProfile,
        direction: ruleDirection,
        analysed_param: ruleParameters,
        is_active: true,
        expected_val: ruleExpectedValue,
    }
    */

    const rule = {
        name: ruleName,
        protocol: ruleProtocol,
        source: ruleSource,
        destination: ruleDestination,
        destination_port: ruleDestinationPort,
        is_active: true,
    }

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
}

