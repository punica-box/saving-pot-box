new Vue({
    el: '#vue-app',
    data: function () {
        return {
            loginDialogVisible: true,
            loginForm: {
                acctPass: ''
            },
            settingForm: settingForm
        }
    },
    methods: {
        getAccounts: getAccounts,
        createAccount: createAccount,
        networkChange: networkChange,
        accountChange: accountChange,
        getDefaultAccountData: getDefaultAccountData,
        async sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        reloadLoginPage() {
            window.location.reload();
        },
        async handleLoginDialogClose(done) {
            await this.$confirm('Are you sure to close this dialog?', 'Warning', {
                confirmButtonText: 'OK',
                cancelButtonText: 'Cancel',
                type: 'warning'
            }).then(_ => {
                window.location.reload();
            }).catch(_ => {
            });
        },
        async getIdentities() {
            try {
                let url = Flask.url_for('get_identities');
                let response = await axios.get(url);
                this.loginForm.identityOptions = [];
                for (let i = 0; i < response.data.result.length; i++) {
                    this.loginForm.identityOptions.push({
                        value: response.data.result[i].ont_id,
                        label: response.data.result[i].label
                    });
                }
            } catch (error) {
                console.log(error);
            }
        },
        async changeToFirstAccount() {
            if (this.settingForm.accountSelected.length === 0 && this.settingForm.accountOptions.length !== 0) {
                let firstAccount = this.settingForm.accountOptions[0].value;
                this.settingForm.accountSelected = [firstAccount];
                this.settingForm.b58AddressSelected = firstAccount;
            }
        },
        async login() {
            if (this.loginForm.acctPass === '') {
                this.$message({
                    type: 'error',
                    message: 'Please input password',
                    duration: 3000
                });
                return
            }
            let unlock_acct_url = Flask.url_for('unlock_account');
            let redirect_url = '';
            try {
                let response = await axios.post(unlock_acct_url, {
                    'b58_address_selected': this.settingForm.b58AddressSelected,
                    'acct_password': this.loginForm.acctPass
                });
                redirect_url = response.data.redirect_url;
                this.$message({
                    type: 'success',
                    center: true,
                    message: response.data.result,
                    duration: 3000
                });
            } catch (error) {
                redirect_url = error.response.data.redirect_url;
                this.$message({
                    type: 'error',
                    center: true,
                    message: error.response.data.result,
                    duration: 3000
                });
            }
            await this.sleep(2000);
            window.location.replace(redirect_url);
        }
    },
    async created() {
        await this.getAccounts();
        await this.getDefaultAccountData();
        await this.changeToFirstAccount();
    }
});