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

    const rule = {
        id: RULES.length + 1,
        name: ruleName,
        protocol: ruleProtocol,
        is_active: "true",
    }

    if(ruleProtocol === "IP/TCP") {
        rule['source_address'] = document.getElementById('rule_source_address').value;
        rule['destination_address'] = document.getElementById('rule_destination_address').value;
        rule['source_port'] = document.getElementById('rule_source_port').value;
        rule['destination_port'] = document.getElementById('rule_destination_port').value;
    }

    if(ruleProtocol === "MODBUS") {
        rule['function'] = document.getElementById('rule_function').value;

        if(rule.function === "f1") {
            rule['starting_address'] = document.getElementById('rule_starting_address').value;
            rule['last_address'] = document.getElementById('rule_last_address').value;
        }
        
        if(rule.function === "f5") {
            rule['output_address'] = document.getElementById('rule_output_address').value;
            rule['value'] = document.getElementById('rule_value').value;
        }

        if(rule.function === "f6") {
            rule['output_address'] = document.getElementById('rule_output_address').value;
            rule['min_value'] = document.getElementById('rule_min_value').value;
            rule['max_value'] = document.getElementById('rule_max_value').value;
        }

        if(rule.function === "f23") {
            rule['read_starting_address'] = document.getElementById('rule_read_starting_address').value;
            rule['read_last_address'] = document.getElementById('rule_read_last_address').value;
            rule['write_starting_address'] = document.getElementById('rule_write_starting_address').value;
            rule['write_last_address'] = document.getElementById('rule_write_last_address').value;
        }
    }

    if(ruleProtocol === "SLMP") {
        rule['command'] = document.getElementById('rule_command').value;
        rule["subcommand"] = document.getElementById('rule_subcommand').value;
        rule['min_value'] = document.getElementById('rule_min_value').value;
        rule['max_value'] = document.getElementById('rule_max_value').value;
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

