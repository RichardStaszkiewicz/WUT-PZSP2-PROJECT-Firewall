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
        id: Math.random(),
        name: ruleName,
        protocol: ruleProtocol,
        is_active: true,
    }

    if(ruleProtocol === "IP/TCP") {
        rule['source address'] = document.getElementById('rule_source_address').value;
        rule['destination address'] = document.getElementById('rule_destination_address').value;
        rule['source port'] = document.getElementById('rule_source_port').value;
        rule['destination port'] = document.getElementById('rule_destination_port').value;
    }

    if(ruleProtocol === "MODBUS" || ruleProtocol === "SLMP") {
        rule['function'] = document.getElementById('rule_function').value;

        if(rule.function === "f1") {
            rule['starting address'] = document.getElementById('rule_starting_address').value;
            rule['last address'] = document.getElementById('rule_last_address').value;
        }
        
        if(rule.function === "f5") {
            rule['output address'] = document.getElementById('rule_output_address').value;
            rule['value'] = document.getElementById('rule_value').value;
        }

        if(rule.function === "f6") {
            rule['output address'] = document.getElementById('rule_output_address').value;
            rule['min value'] = document.getElementById('rule_min_value').value;
            rule['max value'] = document.getElementById('rule_max_value').value;
        }

        if(rule.function === "f23") {
            rule['read starting address'] = document.getElementById('rule_read_starting_address').value;
            rule['read last address'] = document.getElementById('rule_read_last_address').value;
            rule['write starting address'] = document.getElementById('rule_write_starting_address').value;
            rule['write last address'] = document.getElementById('rule_write_last_address').value;
        }
    }

    console.log(RULES)

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
}

