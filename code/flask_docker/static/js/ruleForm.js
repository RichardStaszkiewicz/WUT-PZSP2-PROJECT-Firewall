const triggerRuleForm = (ruleId) => {
    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    ruleForm.style.display = "block";
}

const closeRuleForm = (ruleId) => {
    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    ruleForm.style.display = "none";
}

const saveRuleForm = async (ruleId) => {
    const ruleName = document.getElementById(`${ruleId}_name`).value;
    const ruleProtocol = document.getElementById(`${ruleId}_protocol`).value;
    const ruleCommand = document.getElementById(`${ruleId}_command`).value;
    const ruleDirection = document.getElementById(`${ruleId}_direction`).value;
    const ruleStartRegister = document.getElementById(`${ruleId}_startRegister`).value;
    const ruleQuantity = document.getElementById(`${ruleId}_quantity`).value;
    const ruleComparison = document.getElementById(`${ruleId}_comparison`).value;
    const ruleIsActive = document.getElementById(`${ruleId}_isActive`).value === 'True';

    const rule = {
        id: parseInt(ruleId),
        name: ruleName,
        direction: ruleDirection,
        protocol: ruleProtocol,
        command: ruleCommand,
        start_register: ruleStartRegister,
        quantity: ruleQuantity,
        comparison: ruleComparison,
        is_active: ruleIsActive,
    }

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });

    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    ruleForm.style.display = "none";
    window.location.reload(true);
}