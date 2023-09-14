# MoneyForwardCryptoIntegration
MoneyForwardCryptoIntegrationは、仮想通貨資産等の非対応資産の統合管理と自動同期を実現するプロジェクトです。このプロジェクトの目的は、マネーフォワードと公式非対応の様々な資産プラットフォーム（例: Ledger、Bybitなど）の間での仮想通貨残高を自動的に同期し、マネーフォワードの資産状況を最新に保つことです。<br>
[MoneyForward](https://moneyforward.com/)

#### MoneyForwardの問題点<br>
1.Segwit BTCに対応しておらず(Legacyのみ)、BTC残高が統合できない<br>
2.STETHやBNBXなど、ステーキング中の仮想通貨に対応しておらずそれらの残高が統合出来ない<br>
3.Ledger Walletに対応していない<br>
4.Bybit等の海外仮想通貨/株取引所に対応していない<br>
5.無料プランでは総資産推移が表示出来ない

### Solution and architecture<br>
本PythonスクリプトをAWS Lambdaから定期実行することで、各非公式APIやスクレイピングで非対応口座残高を取得し、Seleniumを用いてMoneyforwardの手動口座入力から残高を自動更新する。<br>

TODO: add　Architecture Diagram here

 ## How to install
 ### 1. AWSアカウントを取得、下記を参考にSeleniumを実行可能な環境を整える
 [AWS Lambda PythonでSeleniumを使える環境を構築する]( https://dev.classmethod.jp/articles/aws-lambda-python-selenium-make-env/)<br>
[AWS LambdaでSeleniumを動かすときに"Unable to import module 'lambda_function': urllib3 v2.0 only supports OpenSSL 1.1.1+, …](https://qiita.com/wonderland90th/items/a54fa021882ec3c080e3)<br>
[【Python】ChromeDriverのエラーまとめ【selenium】](https://sushiringblog.com/chromedriver-error#index_id1)

### 2. EventBridgeからLambdaでmoneyforward_balance_updater.pyを定期実行
[AWS Lambdaで遊ぼう #2 Lambda関数を定期実行する](https://www.benjamin.co.jp/blog/technologies/lambda-2-eventbridge/)
