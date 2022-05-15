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
    const ruleCommand = document.getElementById('ruleCommand').value;
    const ruleDirection = document.getElementById('ruleDirection').value;
    const ruleStartRegister = document.getElementById('ruleStartRegister').value;
    const ruleQuantity = document.getElementById('ruleQuantity').value;
    const ruleComparison = document.getElementById('ruleComparison').value;

    const rule = {
        name: ruleName,
        direction: ruleDirection,
        protocol: ruleProtocol,
        command: ruleCommand,
        start_register: ruleStartRegister,
        quantity: ruleQuantity,
        comparison: ruleComparison,
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

