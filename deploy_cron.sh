#!/bin/bash

# Deploy cron configuration to EC2 instance
# This script uploads and executes the cron setup on the remote EC2 instance

echo "🚀 Deploying cron configuration to EC2 instance..."

# Read instance info
if [ ! -f "deploy/instance_info.json" ]; then
    echo "❌ instance_info.json not found"
    echo "💡 Please create deploy/instance_info.json with EC2 instance information"
    exit 1
fi

# Extract IP from instance_info.json
EC2_IP=$(python3 -c "import json; print(json.load(open('deploy/instance_info.json'))['public_ip'])" 2>/dev/null)

if [ -z "$EC2_IP" ]; then
    echo "❌ Could not extract EC2 IP from instance_info.json"
    exit 1
fi

echo "📡 Target EC2 IP: $EC2_IP"

# Check SSH connectivity
echo "🔍 Testing SSH connection..."
if ! ssh -o ConnectTimeout=15 -o StrictHostKeyChecking=no -i ~/.ssh/claude-agent-key.pem ubuntu@$EC2_IP "echo 'Connection test successful'" 2>/dev/null; then
    echo "❌ SSH connection failed"
    echo "💡 Please check:"
    echo "   - EC2 instance is running"
    echo "   - Security group allows SSH (port 22)"
    echo "   - SSH key file exists at ~/.ssh/claude-agent-key.pem"
    exit 1
fi

echo "✅ SSH connection successful"

# Upload cron setup script
echo "📤 Uploading cron setup script..."
scp -i ~/.ssh/claude-agent-key.pem deploy/setup_cron.sh ubuntu@$EC2_IP:/tmp/setup_cron.sh

# Make it executable and run it
echo "⚙️ Executing cron setup on EC2..."
ssh -i ~/.ssh/claude-agent-key.pem ubuntu@$EC2_IP "
    chmod +x /tmp/setup_cron.sh
    /tmp/setup_cron.sh
"

if [ $? -eq 0 ]; then
    echo -e "\n✅ Cron deployment completed successfully!"
    
    # Show current status
    echo -e "\n📊 Current system status:"
    ssh -i ~/.ssh/claude-agent-key.pem ubuntu@$EC2_IP "
        echo '=== Cron Jobs ==='
        crontab -l
        
        echo -e '\n=== Cron Service Status ==='
        sudo systemctl is-active cron
        
        echo -e '\n=== Update Script Status ==='
        if [ -f '/home/ubuntu/news-ai-site/backend/update_news_viral.py' ]; then
            echo 'Update script: ✅ Ready'
        else
            echo 'Update script: ❌ Missing'
        fi
        
        echo -e '\n=== Recent Log (if any) ==='
        if [ -f '/tmp/news_update_cron.log' ]; then
            echo 'Log file created, monitoring...'
            tail -5 /tmp/news_update_cron.log 2>/dev/null || echo 'No entries yet'
        else
            echo 'Log file will be created on first run'
        fi
    "
    
    echo -e "\n🕐 The news update system will now run automatically every 15 minutes"
    echo "📝 Monitor with: ssh -i ~/.ssh/claude-agent-key.pem ubuntu@$EC2_IP 'tail -f /tmp/news_update_cron.log'"
    
else
    echo "❌ Cron deployment failed"
    exit 1
fi