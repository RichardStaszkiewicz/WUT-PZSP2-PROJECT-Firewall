const triggerRuleForm = (ruleId) => {
    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    ruleForm.style.display = "block";
}

const closeRuleForm = (ruleId) => {
    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    ruleForm.style.display = "none";
}

const hideFields = (fieldsIds) => {
    fieldsIds.forEach((id) => {
        const field = document.getElementById(`${id}`);
        field.style.display = 'none';
    })
}

const showFormField = (fieldId) => {
    console.log(fieldId)
    const field = document.getElementById(`${fieldId}`);
    field.style.display = "flex";
}

const triggerAddProtocolField = (fieldId) => {
    console.log(fieldId)
    const protocolsIds = ['add_MODBUS', 'add_IP/TCP', 'add_SLMP']
    hideFields(protocolsIds)
    showFormField(`add_${fieldId}`)
}

const triggerAddFunctionField = (fieldId) => {
    const functionFieldsIds = ['add_f1', 'add_f5', 'add_f6', 'add_f23']
    hideFields(functionFieldsIds)
    showFormField(`add_${fieldId}`)
}

const triggerProtocolField = (fieldId) => {
    const protocolsIds = ['MODBUS', 'IP/TCP', 'SLMP'];
    hideFields(protocolsIds)
    showFormField(fieldId);
}

const triggerFunctionField = (fieldId) => {
    const functionFieldsIds = ['f1', 'f5', 'f6', 'f23'];
    hideFields(functionFieldsIds);
    showFormField(fieldId)
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