function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

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
    const protocolsIds = ['add_MODBUS', 'add_TCP', 'add_SLMP']
    hideFields(protocolsIds)
    showFormField(`add_${fieldId}`)
}

const triggerAddFunctionField = () => {
    const selectedField = document.getElementById(`MODBUS_rule_command`);
    const fieldId = selectedField.options[selectedField.selectedIndex].id;
    const functionFieldsIds = ['add_f1', 'add_f5', 'add_f6']
    hideFields(functionFieldsIds)
    showFormField(`add_${fieldId}`)
}

const triggerProtocolField = (fieldId, id) => {
    const protocolsIds = [`${id}_MODBUS`, `${id}_TCP`, `${id}_SLMP`];
    hideFields(protocolsIds)
    showFormField(`${id}_${fieldId}`);
}

const triggerFunctionField = (id) => {
    const selectedField = document.getElementById(`${id}_MODBUS_rule_command`);
    const fieldId = selectedField.options[selectedField.selectedIndex].id;
    const functionFieldsIds = [`${id}_f1`, `${id}_f5`, `${id}_f6`];
    hideFields(functionFieldsIds);
    showFormField(`${id}_${fieldId}`)
}

const saveRuleForm = async (ruleId) => {
    const ruleName = document.getElementById(`${ruleId}_name`).value;
    const ruleProtocol = document.getElementById(`${ruleId}_protocol`).value;
    var ruleIsActive;
    
    if(document.getElementById(`${ruleId}_isActive`).value == 'true'){
        ruleIsActive = 'true';
    }
    else{
        ruleIsActive = 'false';
    }

    const rule = {
        id: parseInt(ruleId),
        name: ruleName,
        protocol: ruleProtocol,
        is_active: ruleIsActive,
    }

    if(ruleProtocol == "TCP") {
        rule['source_address'] = document.getElementById(`${ruleId}TCP_source_address`).value;
        rule['destination_address'] = document.getElementById(`${ruleId}TCP_destination_address`).value;
        rule['source_port'] = document.getElementById(`${ruleId}TCP_source_port`).value;
        rule['destination_port'] = document.getElementById(`${ruleId}TCP_destination_port`).value;
    }

    if(ruleProtocol == "MODBUS") {
        ruleCommand = document.getElementById(`${ruleId}_MODBUS_rule_command`);
        const ruleCommandId = ruleCommand.options[ruleCommand.selectedIndex].id;
        rule['command'] = ruleCommand.value;

        if(ruleCommandId === "f1") {
            rule['start_register'] = document.getElementById(`${ruleId}f1_start_register`).value;
            rule['end_register'] = document.getElementById(`${ruleId}f1_end_register`).value;
        }
        
        if(ruleCommandId == "f5") {
            rule['output_address'] = document.getElementById(`${ruleId}f5_output_address`).value;
            rule['value'] = document.getElementById(`${ruleId}f5_value`).value;
        }

        if(ruleCommandId == "f6") {
            rule['output_address'] = document.getElementById(`${ruleId}f6_output_address`).value;
            rule['start_register'] = document.getElementById(`${ruleId}f6_start_register`).value;
            rule['end_register'] = document.getElementById(`${ruleId}f6_end_register`).value;
        }
    }

    if(ruleProtocol == "SLMP") {
        rule['command'] = document.getElementById(`${ruleId}_SLMP_rule_command`).value;
        rule['subcommand'] = document.getElementById(`${ruleId}SLMP_rule_subcommand`).value;
        rule['start_register'] = document.getElementById(`${ruleId}SLMP_rule_start_register`).value;
        rule['end_register'] = document.getElementById(`${ruleId}SLMP_rule_end_register`).value;
    }
    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
    const ruleForm = document.getElementById(`ruleForm_${ruleId}`);

    await sleep(1000)
    ruleForm.style.display = "none";
    window.location.reload(true);
}
