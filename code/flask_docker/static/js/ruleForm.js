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
    const field = document.getElementById(`${fieldId}`);
    field.style.display = "flex";
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
    const ruleIsActive = document.getElementById(`${ruleId}_isActive`).value === 'True';

    const rule = {
        id: parseInt(ruleId),
        name: ruleName,
        protocol: ruleProtocol,
        is_active: ruleIsActive,
    }

    if(ruleProtocol === "IP/TCP") {
        rule['source address'] = document.getElementById(`${ruleId}_source_address`).value;
        rule['destination address'] = document.getElementById(`${ruleId}_destination_address`).value;
        rule['source port'] = document.getElementById(`${ruleId}rule_source_port`).value;
        rule['source address'] = document.getElementById(`${ruleId}_destination_port`).value;
    }

    if(ruleProtocol === "MODBUS" || ruleProtocol === "SLMP") {
        rule['function'] = document.getElementById(`${ruleId}_function`).value;

        if(rule.function === "f1") {
            rule['starting address'] = document.getElementById(`${ruleId}_starting_address`).value;
            rule['last address'] = document.getElementById(`${ruleId}_last_address`).value;
        }
        
        if(rule.function === "f5") {
            rule['output address'] = document.getElementById(`${ruleId}_output_address`).value;
            rule['value'] = document.getElementById(`${ruleId}_value`).value;
        }

        if(rule.function === "f6") {
            rule['output address'] = document.getElementById(`${ruleId}_output_address`).value;
            rule['min value'] = document.getElementById(`${ruleId}_min_value`).value;
            rule['max value'] = document.getElementById(`${ruleId}_max_value`).value;
        }

        if(rule.function === "f23") {
            rule['read starting address'] = document.getElementById(`${ruleId}_read_starting_address`).value;
            rule['read last address'] = document.getElementById(`${ruleId}_read_last_address`).value;
            rule['write starting address'] = document.getElementById(`${ruleId}_write_starting_address`).value;
            rule['write last address'] = document.getElementById(`${ruleId}_write_last_address`).value;
        }
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