#!/bin/bash

# EC2 IP更新スクリプト
# 使用方法: ./update_ip.sh [新しいIPアドレス]

if [ $# -eq 0 ]; then
    echo "使用方法: $0 [新しいIPアドレス]"
    echo "例: $0 52.194.123.45"
    exit 1
fi

NEW_IP=$1
echo "🔄 EC2 IPアドレスを $NEW_IP に更新します..."

# 1. instance_info.json を更新
echo "📝 instance_info.json を更新中..."
cd /Users/YUKI/Desktop/claude-agent-system/deploy
cat > instance_info.json << EOF
{
  "instance_id": "i-0ac6e3baad5cb682e",
  "public_ip": "$NEW_IP",
  "launch_time": "$(date -u +%Y-%m-%d\ %H:%M:%S+00:00)"
}
EOF

# 2. 接続テスト
echo "🔍 新しいIPアドレスで接続テスト..."
if timeout 10 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i ~/.ssh/claude-agent-key.pem ubuntu@$NEW_IP "echo 'Connection successful'" 2>/dev/null; then
    echo "✅ SSH接続成功！"
    
    # 3. システム状況確認
    echo "📊 システム状況確認中..."
    ssh -i ~/.ssh/claude-agent-key.pem ubuntu@$NEW_IP "
    echo '=== System Status ==='
    echo 'Hostname:' \$(hostname)
    echo 'Uptime:' \$(uptime)
    
    echo -e '\n=== Nginx Status ==='
    if command -v nginx >/dev/null 2>&1; then
        echo 'Nginx: ✅ Installed'
        sudo systemctl is-active nginx
    else
        echo 'Nginx: ❌ Not installed'
    fi
    
    echo -e '\n=== Website Files ==='
    if [ -d '/var/www/html' ]; then
        echo 'Website directory: ✅ Exists'
        ls -la /var/www/html/ | head -5
    else
        echo 'Website directory: ❌ Missing'
    fi
    
    echo -e '\n=== News Update Script ==='
    if [ -f '/home/ubuntu/news-ai-site/update_news.py' ]; then
        echo 'Update script: ✅ Exists'
    else
        echo 'Update script: ❌ Missing'
    fi
    
    echo -e '\n=== Cron Jobs ==='
    crontab -l 2>/dev/null | grep -c update_news || echo 'Cron job: ❌ Not set'
    "
    
    echo -e "\n🌐 ニュースサイトURL: http://$NEW_IP"
    echo "📋 IP更新完了: $NEW_IP"
    
else
    echo "❌ SSH接続失敗 - インスタンスがまだ起動中の可能性があります"
    echo "💡 2-3分待ってから再度実行してください"
fi