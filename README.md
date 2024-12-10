# Azure AI Document Intelligence サンプル

## 前提
下記アプリケーションがインストール済であること
```
git
python
vscode(python拡張機能含む)
```

以下、サンプルを実行するまでの環境構築&実行手順

## 1. git clone
任意のフォルダで以下コマンド実行
→TechLabo-Python-azure-ai-documentintelligenceフォルダが作成される。

```
git clone https://github.com/udonkot/TechLabo-Python-azure-ai-documentintelligence.git
```
## 2. developブランチチェックアウト
コマンドプロンプトを起動し、1.で生成されたフォルダに移動。下記コマンド実行
→developブランチに切り替わる
```
git checkout develop
```

## 3. 環境変数設定
以下の環境変数を設定してください。
AzurePortalから確認できます。

| 環境変数名                    | 説明                                                |
| ----------------------------- | --------------------------------------------------- |
| DOCUMENTINTELLIGENCE_API_KEY  | Azure AI Document Intelligence の API キー          |
| DOCUMENTINTELLIGENCE_ENDPOINT | Azure AI Document Intelligence のエンドポイント URL |

## 4.vscode起動
1．で作成したフォルダを読み込む

## 5.ターミナル起動

## 6.python仮想環境作成
ターミナル上で下記コマンドを実行
```
python -m venv venv
```

## 7.仮想環境有効化
ターミナルで下記コマンド実行
→ターミナルの先頭に”(venv)”と表示されれば仮想環境の有効化に成功
```
./venv/Scripts/activate
```

## 8. ライブラリインストール
下記コマンドを実行
```
python -m pip install azure-core
python -m pip install azure-ai-documentintelligence
```

## 9. python実行
samplesフォルダ配下のPythonスクリプトを実行
例）サンプルの図面を読み込むスクリプトを実行する場合
→読み込んだ値と座標位置が出力される
```
python .\samples\sample_analyze_addon_highres.py
```
