//const enableBtn = document.getElementById('checkButtonEnable');
//const disableBtn = document.getElementById('checkButtonDisable');

const getItemId = (event) => {
    return event.srcElement.id;
}

const getRules = () => {
    fetch('/getRules').then((response) => {
        return response.json();
    }).then((data) => {
        return data;
    })
};

const triggerCheck = (value, rule) => {
    rule.is_active = value;

    fetch('/getRules', {
        method: 'POST',
        headers: {
            "Content-Type": 'application/json',
        },
        body: JSON.stringify(rule),
    });
};


/*
enableBtn.onclick = () => {
    //triggerCheck(false, {});
}

disableBtn.onclick = () => {
    //triggerCheck(true, {});
}
*/