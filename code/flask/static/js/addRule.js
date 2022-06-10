function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

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
    const ruleName = document.getElementById('rule_name').value;
    const ruleProtocol = document.getElementById('rule_protocol').value;
    const ruleIsActive = 'false';

    const rule = {
        id: RULES.length + 1,
        name: ruleName,
        is_active: ruleIsActive,
        protocol: ruleProtocol,
    }

    if(ruleProtocol === "TCP") {
        rule['source_address'] = document.getElementById('TCP_rule_source_address').value;
        rule['destination_address'] = document.getElementById('TCP_rule_destination_address').value;
        rule['source_port'] = document.getElementById('TCP_rule_source_port').value;
        rule['destination_port'] = document.getElementById('TCP_rule_destination_port').value;
    }

    if(ruleProtocol === "MODBUS") {
        ruleCommand = document.getElementById('MODBUS_rule_command');
        const ruleCommandId = ruleCommand.options[ruleCommand.selectedIndex].id;
        rule['command'] = ruleCommand.value;

        if(ruleCommandId === "f1") {
            rule['start_register'] = document.getElementById('f1_rule_start_register').value;
            rule['end_register'] = document.getElementById('f1_rule_end_register').value;
        }
        
        if(ruleCommandId === "f5") {
            rule['output_address'] = document.getElementById('f5_rule_output_address').value;
            rule['value'] = document.getElementById('f5_rule_value').value;
        }

        if(ruleCommandId === "f6") {
            rule['output_address'] = document.getElementById('f6_rule_output_address').value;
            rule['start_register'] = document.getElementById('f6_rule_start_register').value;
            rule['end_register'] = document.getElementById('f6_rule_end_register').value;
        }
    }

    if(ruleProtocol === "SLMP") {
        rule['command'] = document.getElementById('SLMP_rule_command').value;
        rule['subcommand'] = document.getElementById('SLMP_rule_subcommand').value;
        rule['start_register'] = document.getElementById('SLMP_rule_start_register').value;
        rule['end_register'] = document.getElementById('SLMP_rule_end_register').value;
    }

    RULES.push(rule);

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
}

