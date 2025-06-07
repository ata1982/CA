#!/bin/bash
set -e

echo "🔧 EC2インスタンスをセットアップ中..."

# システムアップデート
sudo apt-get update
sudo apt-get upgrade -y

# 必要なパッケージインストール
sudo apt-get install -y python3-pip python3-venv git nodejs npm

# Claude Codeのインストール（実際のインストール方法に置き換え）
# npm install -g @anthropic-ai/claude-code

# プロジェクトディレクトリ作成
mkdir -p ~/claude-agent-system

# Python仮想環境作成
cd ~/claude-agent-system
python3 -m venv venv
source venv/bin/activate

echo "✅ セットアップ完了!"