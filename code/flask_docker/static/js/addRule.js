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
const ruleName = document.getElementById('ruleName').value;
const ruleProtocol = document.getElementById('ruleProtocol').value;
const ruleProfile = document.getElementById('ruleProfile').value;
const ruleDirection = document.getElementById('ruleDirection').value;
const ruleParameters = document.getElementById('ruleParameters').value;
const ruleExpectedValue = document.getElementById('ruleExpectedValue').value;

const addRuleBtn = document.getElementById('confirmAddRule');

const rule = {
    name: ruleName,
    protocol: ruleProtocol,
    profile: ruleProfile,
    direction: ruleDirection,
    analysed_param: ruleParameters,
    expected_val: ruleExpectedValue,
}

addRuleBtn.onclick = () => {
    //TODO: create addRule function
}

