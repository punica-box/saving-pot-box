new Vue({
    el: '#vue-app',
    data: function () {
        return {
            ontBankForm: ontBankForm,
            ongBankForm: ongBankForm,

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
        savingOnt: savingOnt,
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
                await this.getAccounts();
            } else if (tab.label === 'Information Query') {
                this.isSwitchToSettings = true;
                await this.getAccounts();
            } else {
                this.isSwitchToSettings = true;
            }
        }
    },
    async created() {
        await this.getAccounts();
        await this.getDefaultAccountData();
    }
});
