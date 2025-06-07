#!/bin/bash

echo "🔍 EC2インスタンス状況確認スクリプト"
echo "=================================="

INSTANCE_IP="13.158.19.10"
SSH_KEY="~/.ssh/claude-agent-key.pem"

echo "📡 接続テスト中..."
if timeout 10 ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i $SSH_KEY ubuntu@$INSTANCE_IP "echo 'Connected'" 2>/dev/null; then
    echo "✅ SSH接続成功"
    
    echo -e "\n🔍 システム状況確認:"
    ssh -i $SSH_KEY ubuntu@$INSTANCE_IP "
    echo '=== Basic Info ==='
    whoami && hostname && uptime
    
    echo -e '\n=== Nginx Status ==='
    if command -v nginx >/dev/null 2>&1; then
        echo 'Nginx installed ✅'
        sudo systemctl is-active nginx
        sudo systemctl is-enabled nginx
    else
        echo 'Nginx not installed ❌'
    fi
    
    echo -e '\n=== Website Files ==='
    if [ -d '/var/www/html' ]; then
        ls -la /var/www/html/
    else
        echo '/var/www/html does not exist ❌'
    fi
    
    echo -e '\n=== Cron Jobs ==='
    crontab -l 2>/dev/null || echo 'No cron jobs ❌'
    
    echo -e '\n=== Update Script ==='
    if [ -f '/home/ubuntu/news-ai-site/update_news.py' ]; then
        echo 'Update script exists ✅'
        ls -la /home/ubuntu/news-ai-site/update_news.py
    else
        echo 'Update script missing ❌'
    fi
    
    echo -e '\n=== Python Processes ==='
    ps aux | grep python | grep -v grep || echo 'No Python processes'
    
    echo -e '\n=== Recent Logs ==='
    echo 'Nginx access log (last 3 lines):'
    sudo tail -3 /var/log/nginx/access.log 2>/dev/null || echo 'No access log'
    
    echo -e '\nSystem log (last 3 cron entries):'
    sudo grep CRON /var/log/syslog 2>/dev/null | tail -3 || echo 'No cron logs'
    "
    
else
    echo "❌ SSH接続失敗"
    echo "可能な原因:"
    echo "- インスタンスがまだ起動中"
    echo "- セキュリティグループでSSH(22)が開放されていない" 
    echo "- IPアドレスが変更された"
    echo ""
    echo "💡 解決方法:"
    echo "1. AWSコンソールでインスタンス状態を確認"
    echo "2. 5-10分待ってから再実行"
    echo "3. セキュリティグループでポート22を0.0.0.0/0に開放"
fi

echo -e "\n📋 実行時刻: $(date)"