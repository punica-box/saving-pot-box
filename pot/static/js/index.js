new Vue({
    el: '#vue-app',
    data: function () {
        return {
            ontBankForm: ontBankForm,
            ongBankForm: ongBankForm,

            uploadDialogVisible: uploadDialogVisible,
            uploadForm: uploadForm,
            unlockDialogVisible: true,
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

        unlockWalletAccount: unlockWalletAccount,
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
        async getAlbumArray() {
            let url = Flask.url_for('get_album_array');
            try {
                let response = await axios.get(url);
                this.albumArray = response.data.result;
            } catch (error) {
                console.log(error);
            }
        },
        async tabClickHandler(tab, event) {
            if (tab.label === 'DApp Settings') {
                if (this.isSwitchToSettings === true) {
                    this.isSwitchToSettings = false;
                    await this.getAccounts();
                    await this.getContractAddress();
                    await this.getDefaultAccountData();
                    await this.getDefaultIdentityData();
                }
            }
            else if (tab.label === 'Collapse Album') {
                this.isSwitchToSettings = true;
                await this.getAccounts();
                await this.getAlbumArray();
            }
            else if (tab.label === 'Card Album') {
                this.isSwitchToSettings = true;
                await this.getAccounts();
                await this.getAlbumArray();
            }
            else {
                this.isSwitchToSettings = true;
            }
        }
    },
    async created() {
        await this.getAccounts();
        await this.getDefaultAccountData();
    }
});
