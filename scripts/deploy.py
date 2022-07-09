from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENV
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # publish_source 是否開源（用於etherscan驗證代碼）
    # 前面的這一大串是orcale，傳給了FundMe.sol的constructor
    # 如果我們在持續性網絡如rinkeby，就用下面的這大串
    # 否則我們將部署mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # 如果已经部署了MockV3 就不部署
        deploy_mocks()

        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    return fund_me


def main():
    print(network.show_active())
    deploy_fund_me()
