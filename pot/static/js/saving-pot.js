let ontBankForm = {
    amount: '',
    duration: ''
};

let ongBankForm = {
    amount: '',
    duration: ''
};

let reloadPotPage = async function () {
    window.location.reload();
};

let createOntPot = async function () {
    let timeLimit;
    try {
        timeLimit = await this.$prompt('Please input the time limit of your ont pot', 'Tip', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            inputPattern: /^\+?[1-9]\d*$/,
            inputErrorMessage: 'Invalid Time Limit'
        });
        timeLimit = timeLimit.value;
    } catch (error) {
        this.$message.warning('Create canceled');
    }
    let url = Flask.url_for('create_ont_pot');
    try {
        let response = await axios.post(url, {'time_limit': timeLimit});
        this.$message.success(response.data.result);
    } catch (error) {
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let savingOnt = async function () {

};

let takeOntOut = async function () {

};


let queryOntPotInfo = async function () {

};

let createOngPot = async function () {
    let timeLimit;
    try {
        timeLimit = await this.$prompt('Please input the time limit of your ong pot', 'Tip', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            inputPattern: /^\+?[1-9]\d*$/,
            inputErrorMessage: 'Invalid Time Limit'
        });
        timeLimit = timeLimit.value;
    } catch (error) {
        this.$message.warning('Create canceled');
    }
    let url = Flask.url_for('create_ong_pot');
    try {
        let response = await axios.post(url, {'time_limit': timeLimit});
        this.$message.success(response.data.result);
    } catch (error) {
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let savingOng = async function () {

};

let takeOngOut = async function () {

};


let queryOngPotInfo = async function () {

};