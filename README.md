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

![](architecture_diagram.drawio.svg)

 ## How to install
 ### 1. AWSアカウントを取得、下記を参考にSeleniumを実行可能な環境を整える
 [AWS Lambda PythonでSeleniumを使える環境を構築する]( https://dev.classmethod.jp/articles/aws-lambda-python-selenium-make-env/)<br>
[AWS LambdaでSeleniumを動かすときに"Unable to import module 'lambda_function': urllib3 v2.0 only supports OpenSSL 1.1.1+, …](https://qiita.com/wonderland90th/items/a54fa021882ec3c080e3)<br>
[【Python】ChromeDriverのエラーまとめ【selenium】](https://sushiringblog.com/chromedriver-error#index_id1)

### 2. 所有資産に応じてgetterを変更/作成し統合

### 3. GitHub SecretsへのアカウントとAPIトークンの登録

[GitHub Actions でのシークレットの使用](https://docs.github.com/ja/actions/security-guides/using-secrets-in-github-actions)を参照してください。

#### 必須

- **AWS_ACCESS_KEY_ID**: Lambdaを実行するためのAWSアクセスキーID
- **AWS_SECRET_ACCESS_KEY**: Lambdaを実行するためのAWSアクセスキー
- **MONEYFORWARD_BANK_URL**: MoneyForwardに登録した更新対象の手動入力口座のURL。<br>
  例: https://moneyforward.com/accounts/show_manual/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- **MY_EMAIL_ADDRESS**: MoneyForwardに登録したメールアドレス
- **MONEYFORWARD_PASSWORD**: MoneyForwardのアカウントパスワード

#### 資産に応じて

- **STETH_WALLET_ADDRESS**: STETHが保管されているウォレットアドレス
- **BNBX_WALLET_ADDRESS**: BNBXが保管されているウォレットアドレス
- **BTC_WALLET_BALANCE_URL**: 自分のBTC xpubを表示しているBlockchain.comのページ。segwit対応の良いAPIが無くスクレイピングで暫定対応しているため。<br>
  例: https://www.blockchain.com/explorer/assets/btc/xpub/xpub6BhqNxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

### 4. EventBridgeからLambdaでmoneyforward_balance_updater.pyを定期実行
ハンドラはmoneyforward_balance_updater.lambda_handler<br>
[AWS Lambdaで遊ぼう #2 Lambda関数を定期実行する](https://www.benjamin.co.jp/blog/technologies/lambda-2-eventbridge/)
