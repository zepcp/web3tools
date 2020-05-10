Web3Tools
======
**Web3Tools** is an extender for the [web3py library](https://web3py.readthedocs.io/en/stable/)


Usage - Basic Tools
----------

    from web3tools import Utils

Create an ethereum account

    address, private_key = Utils.create()
    keystore = Utils.encrypt(private_key, "myPassword")

Get address

    private_key = Utils.decrypt("myKeystore", "myPassword")
    address = Utils.get_address(private_key)

Sign a message & Recover signer's address
 
    signature = Utils.sign_message("myPrivateKey", "myMessage")
    address = Utils.recover_message(signature, "myMessage")


Usage - Ewt
----------

    from web3tools import Ewt
    ewt = Ewt(expiration=30)

Ewt Authentication, similar to [jwt](https://jwt.io/) but using the ethereum encryption keys

    ewt_token = ewt.generate("myPrivateKey")
    is_valid = ewt.validate(ewt_token)


Usage - Blockchain Reader
----------

    from web3tools import Reader
    reader = Reader(Providers.INFURA_MAINNET.value.format("myInfuraKey"))

Crawl blockchain

    current_block_number = reader.get_current_block_number()
    current_block_info = reader.get_block(current_block_number)
    transaction = reader.get_transaction("myTxid")
    receipt = reader.get_receipt("myTxid")
    gas_price = reader.get_gas_price()

Get Wallet Info

    balance = reader.get_balance("myWallet")
    nonce = reader.get_nonce("myWallet")
    
Read Contracts

    contract = reader.get_contract_instance("abiFilePath", "contractAddress")
    value = reader.call_view(contract, "viewName", "viewArguments")
    events = reader.find_events(contract, "eventName", from_block=0, to_block="latest")
    events_on_transaction = reader.find_event_receipt(contract, "eventName", "myTxid")


Usage - Launch Transactions
----------

    from web3tools import Provider, Transactor
    transactor = Transactor(Providers.INFURA_MAINNET.value.format("myInfuraKey"))

Send *1 Eth* to *receiverAddress*

    transactor.launch_transaction("myPrivateKey", "receiverAddress", transactor.to_wei(1))

Call a *transfer* function of a *token contract* to send *1 Token* to *receiverAddress*

    contract = transactor.get_contract_instance("abiFilePath", "contractAddress")
    transactor.launch_function(contract, "myPrivateKey", "transfer",
                               "receiverAddress", transactor.to_wei(1))
