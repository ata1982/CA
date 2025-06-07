#!/bin/bash

# Setup cron job for viral news updates (every 15 minutes)
# This script configures automatic news updates on the EC2 instance

echo "🕐 Setting up cron job for viral news updates..."

# Check if we're on EC2 instance
if [ -f "/home/ubuntu/.bashrc" ]; then
    echo "✅ Running on EC2 instance"
    
    # Create the cron job entry
    CRON_JOB="*/15 * * * * cd /home/ubuntu/news-ai-site/backend && /usr/bin/python3 /home/ubuntu/news-ai-site/backend/update_news_viral.py >> /tmp/news_update_cron.log 2>&1"
    
    # Backup existing crontab
    echo "📋 Backing up existing crontab..."
    crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
    
    # Remove any existing news update cron jobs
    echo "🧹 Removing existing news update cron jobs..."
    crontab -l 2>/dev/null | grep -v "update_news" | crontab - 2>/dev/null || true
    
    # Add the new cron job
    echo "➕ Adding new cron job (every 15 minutes)..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    
    echo "✅ Cron job added successfully!"
    echo "📅 Current crontab:"
    crontab -l
    
    echo -e "\n🔍 Verification:"
    echo "- Job will run every 15 minutes"
    echo "- Logs will be written to /tmp/news_update_cron.log"
    echo "- Next run: $(date -d '+15 minutes' '+%Y-%m-%d %H:%M:%S')"
    
    # Create log file with proper permissions
    touch /tmp/news_update_cron.log
    chmod 644 /tmp/news_update_cron.log
    
    echo -e "\n📝 To monitor the cron job:"
    echo "  tail -f /tmp/news_update_cron.log"
    echo ""
    echo "📊 To check cron status:"
    echo "  sudo systemctl status cron"
    echo ""
    echo "🗑️ To remove the cron job:"
    echo "  crontab -e"
    
else
    echo "❌ This script should be run on the EC2 instance"
    echo "💡 Use SSH to connect to EC2 first:"
    echo "   ssh -i ~/.ssh/claude-agent-key.pem ubuntu@[EC2_IP]"
    echo "   then run this script"
    exit 1
fi