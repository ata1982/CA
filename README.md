# Claude Agent System

Claude Agent Systemは、Claude Codeを使用して自動でタスクを実行するPythonシステムです。YAMLファイルからタスクを読み込み、Claude Codeに指示を送信して実行し、結果を管理・監視できます。

## 機能

- 📝 YAMLファイルからのタスク定義読み込み
- 🤖 Claude Codeの自動実行とラッパー機能
- 📊 SQLiteデータベースでのタスク履歴管理
- 🎯 リアルタイムタスクステータス追跡
- 📈 ダッシュボードでの統計表示
- 🏥 システムヘルスチェック機能
- 🎨 Richライブラリによる美しいCLI出力

## インストール

```bash
# プロジェクトをクローンまたはダウンロード
cd claude-agent-system

# 依存関係をインストール
pip install -r requirements.txt

# 環境設定ファイルをコピー（必要に応じて編集）
cp .env.example .env
```

## 使用方法

### 基本的な使用方法

```bash
# タスクファイルから実行
python src/agent.py run --task-file tasks/example_tasks.yaml

# ダッシュボードを表示
python src/agent.py dashboard

# ヘルスチェックを実行
python src/agent.py health
```

### タスクファイルの形式

タスクはYAML形式で定義します：

```yaml
tasks:
  - id: "unique_task_id"
    name: "タスク名"
    description: "タスクの詳細説明"
    type: "python_script"  # または "web_app", "data_analysis", "code_review"
    parameters:
      filename: "output.py"
      # その他のパラメータ
```

### サポートされるタスクタイプ

1. **python_script**: Pythonスクリプトの作成
2. **web_app**: Webアプリケーションの開発
3. **data_analysis**: データ分析とレポート作成
4. **code_review**: コードレビューと改善提案

## プロジェクト構造

```
claude-agent-system/
├── src/
│   ├── __init__.py         # パッケージ初期化
│   ├── agent.py           # メインエージェントクラスとCLI
│   ├── task_manager.py    # タスク管理とデータベース操作
│   └── config.py          # 設定管理とログ設定
├── tasks/
│   └── example_tasks.yaml # サンプルタスク定義
├── logs/                  # ログファイル格納ディレクトリ
├── workspace/             # エージェントの作業ディレクトリ
├── requirements.txt       # Python依存関係
├── .env.example          # 環境設定テンプレート
└── README.md             # このファイル
```

## 設定

環境変数で以下の設定が可能です：

- `CLAUDE_CODE_COMMAND`: Claude Codeコマンド (デフォルト: "claude")
- `CLAUDE_CODE_TIMEOUT`: コマンドタイムアウト秒数 (デフォルト: 300)
- `LOG_LEVEL`: ログレベル (デフォルト: "INFO")

## 出力とログ

- 実行結果は`workspace/task_{task_id}/`ディレクトリに保存
- ログは`logs/agent.log`に出力
- タスク履歴はSQLiteデータベース`tasks.db`に保存

## CLI コマンド

### run
```bash
python src/agent.py run --task-file <yaml_file>
```
指定されたYAMLファイルからタスクを実行します。

### dashboard
```bash
python src/agent.py dashboard
```
タスク統計、システムヘルス、最近のタスクを表示するダッシュボードを開きます。

### health
```bash
python src/agent.py health
```
システムヘルスチェックを実行し、結果を表示します。

## サンプルタスク

`tasks/example_tasks.yaml`には以下のサンプルタスクが含まれています：

1. **Hello World スクリプト**: 基本的なPythonスクリプト作成
2. **Flask TODOアプリ**: 簡単なWebアプリケーション開発
3. **CSV分析**: データ分析とサマリー作成

## トラブルシューティング

### Claude Codeが見つからない場合
- Claude Codeが正しくインストールされているか確認
- `CLAUDE_CODE_COMMAND`環境変数で正しいパスを指定

### 権限エラーが発生する場合
- `workspace/`ディレクトリの書き込み権限を確認
- SQLiteデータベースファイルの作成権限を確認

### タスクがタイムアウトする場合
- `CLAUDE_CODE_TIMEOUT`環境変数で適切なタイムアウト値を設定
- 複雑なタスクは分割して実行することを検討

## 依存関係

- pyyaml: YAML ファイルの解析
- python-dotenv: 環境変数の管理
- aiofiles: 非同期ファイル操作
- click: CLI インターフェース
- rich: 美しいコンソール出力
- psutil: システムリソース監視

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。