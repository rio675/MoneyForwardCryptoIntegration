# MoneyForwardCryptoIntegration
MoneyForwardCryptoIntegrationは、仮想通貨資産の統合管理と自動同期を実現するプロジェクトです。このプロジェクトの目的は、マネーフォワードと公式API非対応の様々な仮想通貨プラットフォーム（例: Ledger、Bybitなど）の間での仮想通貨残高を自動的に同期し、マネーフォワードの資産状況を最新に保つことです。<br>
[MoneyForward](https://moneyforward.com/)

 ## How to install
 ### 1. AWSアカウントを取得、下記を参考にSeleniumを実行可能な環境を整える
 [AWS Lambda PythonでSeleniumを使える環境を構築する]( https://dev.classmethod.jp/articles/aws-lambda-python-selenium-make-env/)<br>
[AWS LambdaでSeleniumを動かすときに"Unable to import module 'lambda_function': urllib3 v2.0 only supports OpenSSL 1.1.1+, …](https://qiita.com/wonderland90th/items/a54fa021882ec3c080e3)<br>
[【Python】ChromeDriverのエラーまとめ【selenium】](https://sushiringblog.com/chromedriver-error#index_id1)

### 2. EventBridgeからLambdaでmoneyforward_balance_updater.pyを定期実行
[AWS Lambdaで遊ぼう #2 Lambda関数を定期実行する](https://www.benjamin.co.jp/blog/technologies/lambda-2-eventbridge/)
