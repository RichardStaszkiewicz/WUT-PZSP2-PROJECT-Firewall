const enableAll = () => {
    fetch('/getRules?action=enableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    window.location.reload(true);
}

const disableAll = () => {
    fetch('/getRules?action=disableAll', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
    })
    window.location.reload(true);
}

const savePush = () => {
    const rulesHTML = document.getElementById('rules').getElementsByTagName('li');
    console.log(rulesHTML)

    const ruules = rulesHTML.map(rule => {
        console.log(rule)
        return {
            id: ''
        }
    })

    const rules = [
        {
            "id": 101,
            "name": "Wszystkie multiple read readujące mniej niz 100",
            "direction": "IN",
            "protocol": "MODBUS",
            "command": "Device Read Multiple Registers",
            "Start Register": "Any",
            "quantity": 100,
            "comparison": "MAX",
            "is_active": true
        },
        {
            "id": 102,
            "name": "Wszystkie multiple read readujące mniej niz 150",
            "direction": "IN",
            "protocol": "MODBUS",
            "command": "Device Read Multiple Registers",
            "Start Register": "Any",
            "quantity": 150,
            "comparison": "MAX",
            "is_active": true
        },
        {
            "id": 103,
            "name": "Wszystkie multiple read readujące mniej niz 170",
            "direction": "IN",
            "protocol": "MODBUS",
            "command": "Device Read Multiple Registers",
            "Start Register": "Any",
            "quantity": 170,
            "comparison": "MAX",
            "is_active": true
        }
    ]

    fetch('/getRules?action=save', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rules)
    })
    //window.location.reload(true);
}