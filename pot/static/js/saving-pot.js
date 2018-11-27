let depositOntVisible = false;

let ontBankForm = {
    amount: '',
    savingTime: '',
    duration: '',
    depositOntAmount: ''
};

let ongBankForm = {
    amount: '',
    savingTime: '',
    duration: '',
    depositOngAmount: ''
};

let reloadPotPage = async function () {
    window.location.reload();
};

let queryOntPotAmount = async function () {
};

let queryOntPotDuration = async function () {
    let url = Flask.url_for('query_ont_pot_duration');
    try {
        let response = await axios.get(url);
        this.ontBankForm.duration = response.data.result;
    } catch (error) {
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let queryOngPotDuration = async function () {
    let url = Flask.url_for('query_ong_pot_duration');
    try {
        let response = await axios.get(url);
        this.ongBankForm.duration = response.data.result;
    } catch (error) {
        this.ongBankForm.duration = '';
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let queryOntPotSavingTime = async function () {
    let url = Flask.url_for('query_ont_pot_saving_time');
    try {
        let response = await axios.get(url);
        this.ontBankForm.savingTime = response.data.result;
    } catch (error) {
        this.ongBankForm.duration = '';
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let queryOngPotSavingTime = async function () {
    let url = Flask.url_for('query_ong_pot_saving_time');
    try {
        let response = await axios.get(url);
        this.ongBankForm.savingTime = response.data.result;
    } catch (error) {
        if (error.response.status === 500) {
            let redirect_url = error.response.data.redirect_url;
            window.location.replace(redirect_url);
        } else {
            this.$message.warning(error.response.data.result);
        }
    }
};

let createOntPot = async function () {
    let timeLimit;
    try {
        timeLimit = await this.$prompt('Please input the time limit of your ont pot', 'Tip', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            inputPattern: /^\+?[1-9]\d*$/,
            inputErrorMessage: 'Invalid Time Limit',
            closeOnClickModal: false,
            closeOnPressEscape: true
        });
        timeLimit = timeLimit.value;
    } catch (error) {
        this.$message.warning('Create canceled');
        return;
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
    // this.depositOntVisible = true;
    let timeLimit;
    try {
        timeLimit = await this.$prompt('T you want to deposit', 'Tip', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            inputPattern: /^\+?[1-9]\d*$/,
            inputErrorMessage: 'Invalid Time Limit',
            closeOnClickModal: false,
            closeOnPressEscape: true,
            iconClass: 'iconfont el-icon-third-ONT'
        });
        timeLimit = timeLimit.value;
    } catch (error) {
        this.$message.warning('Create canceled');
        return;
    }
};

let submitDepositOntForm = async function () {
    this.depositOntVisible = false;
};

let handleDepositOntClose = async function () {

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
        return;
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