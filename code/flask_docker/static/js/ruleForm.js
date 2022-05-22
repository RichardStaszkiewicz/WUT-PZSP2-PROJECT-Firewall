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
    console.log(field)
    field.style.display = "flex";

    console.log(field.style.display);
}

const triggerAddProtocolField = (fieldId) => {
    const protocolsIds = ['add_MODBUS', 'add_IP/TCP', 'add_SLMP']
    hideFields(protocolsIds)
    showFormField(`add_${fieldId}`)
}

const triggerAddFunctionField = (fieldId) => {
    const functionFieldsIds = ['add_f1', 'add_f5', 'add_f6', 'add_f23']
    hideFields(functionFieldsIds)
    showFormField(`add_${fieldId}`)
}

const triggerProtocolField = (fieldId, id) => {
    const protocolsIds = [`${id}_MODBUS`, `${id}_IP/TCP`, `${id}_SLMP`];
    hideFields(protocolsIds)
    showFormField(`${id}_${fieldId}`);
}

const triggerFunctionField = (fieldId, id) => {
    const functionFieldsIds = [`${id}_f1`, `${id}_f5`, `${id}_f6`, `${id}_f23`];
    hideFields(functionFieldsIds);
    showFormField(`${id}_${fieldId}`)
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