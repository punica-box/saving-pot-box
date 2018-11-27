new Vue({
    el: '#vue-app',
    data: function () {
        return {
            ontBankForm: ontBankForm,
            ongBankForm: ongBankForm,
            depositOntVisible: depositOntVisible,

            isSwitchToSettings: true,
            albumArray: [],
            eventInfoSelect: eventInfoSelect,
            eventKey: eventKey,
            assetSelect: assetSelect,
            assetKey: assetKey,
            settingForm: settingForm
        }
    },
    methods: {
        reloadPotPage: reloadPotPage,
        createOntPot: createOntPot,
        queryOntPotDuration: queryOntPotDuration,
        queryOngPotDuration: queryOngPotDuration,
        queryOntPotSavingTime: queryOntPotSavingTime,
        queryOngPotSavingTime: queryOngPotSavingTime,
        savingOnt: savingOnt,
        submitDepositOntForm: submitDepositOntForm,
        handleDepositOntClose: handleDepositOntClose,
        takeOntOut: takeOntOut,
        queryOntPotInfo: queryOntPotInfo,
        createOngPot: createOngPot,
        savingOng: savingOng,
        takeOngOut: takeOngOut,
        queryOngPotInfo: queryOngPotInfo,

        getAccounts: getAccounts,
        queryBalance: queryBalance,
        queryEvent: queryEvent,
        importAccount: importAccount,
        removeAccount: removeAccount,
        createAccount: createAccount,
        clearNewAccountHexPrivateKey: clearNewAccountHexPrivateKey,
        accountChange: accountChange,
        networkChange: networkChange,
        changeContract: changeContract,
        getContractAddress: getContractAddress,
        isDefaultWalletAccountUnlock: isDefaultWalletAccountUnlock,
        getDefaultAccountData: getDefaultAccountData,

        async tabClickHandler(tab, event) {
            if (tab.label === 'DApp Settings') {
                if (this.isSwitchToSettings === true) {
                    this.isSwitchToSettings = false;
                    await this.getAccounts();
                    await this.getContractAddress();
                    await this.getDefaultAccountData();
                }
            } else if (tab.label === 'Saving Pot') {
                this.isSwitchToSettings = true;
                this.queryOntPotDuration();
                this.queryOngPotDuration();
                this.queryOntPotSavingTime();
                this.getAccounts();
            } else if (tab.label === 'Information Query') {
                this.isSwitchToSettings = true;
                await this.getAccounts();
            } else {
                this.isSwitchToSettings = true;
            }
        }
    },
    async created() {
        this.getAccounts();
        this.getDefaultAccountData();
        this.queryOntPotDuration();
        this.queryOngPotDuration();
        this.queryOntPotSavingTime();
        this.queryOngPotSavingTime();
    }
});
