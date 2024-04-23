# コンテナ内でlambda関数を配置するディレクトリ名を定義
ARG FUNCTION_DIR="/function"

# msが公開しているplaywright1.42.0用のイメージを使用する
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy as build-image

# 依存ライブラリをインストールする
RUN apt-get update
#RUN apt-get install -y g++
#RUN apt-get install -y make
#RUN apt-get install -y cmake
#RUN apt-get install -y unzip
#RUN apt-get install -y libcurl4-openssl-dev

# おまじない1
ARG FUNCTION_DIR

# lambda関数を配置するディレクトリを作成する
RUN mkdir -p ${FUNCTION_DIR}

# lambda関数のコード一式をコピーする
COPY ./* ${FUNCTION_DIR}

# runtime interface clientというライブラリをインストールする
RUN python -m pip install --upgrade pip
RUN python -m pip install --target ${FUNCTION_DIR} playwright awslambdaric

# その他のランタイムをインスト＾るする（お好みで）
#RUN python -m pip install --target ${FUNCTION_DIR} boto3 pandas

# マルチステージビルドのおまじない
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# おまじない2
ARG FUNCTION_DIR

# 作業ディレクトリを移動
WORKDIR ${FUNCTION_DIR}

# おまじない3
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# 実行された時に発行するコマンドを指定する
ENTRYPOINT [ "/usr/bin/python", "-m", "awslambdaric" ]
CMD [ "moneyforward_balance_updater.lambda_handler" ]