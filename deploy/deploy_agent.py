import paramiko
import json
import os
from pathlib import Path
import tarfile
import io

class AgentDeployer:
    def __init__(self):
        self.load_instance_info()
        
    def load_instance_info(self):
        """インスタンス情報を読み込み"""
        with open('instance_info.json') as f:
            self.instance_info = json.load(f)
            
    def create_deployment_package(self):
        """デプロイ用のパッケージを作成"""
        print("📦 デプロイパッケージを作成中...")
        
        with tarfile.open('claude-agent-deploy.tar.gz', 'w:gz') as tar:
            # プロジェクトファイルを追加（.venvなどは除外）
            exclude_dirs = {'venv', '.venv', '__pycache__', '.git', 'logs', 'workspace', 'deploy'}
            project_root = Path(__file__).parent.parent
            
            for item in project_root.iterdir():
                if item.name not in exclude_dirs and not item.name.startswith('.'):
                    tar.add(item, arcname=item.name)
        
        print("✅ パッケージ作成完了")
        
    def deploy_to_ec2(self):
        """EC2にデプロイ"""
        print("🚀 EC2にデプロイ中...")
        
        # SSH接続
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        key_path = Path.home() / '.ssh' / 'claude-agent-key.pem'
        
        try:
            ssh.connect(
                self.instance_info['public_ip'],
                username='ubuntu',
                key_filename=str(key_path)
            )
        except Exception as e:
            print(f"❌ SSH接続エラー: {e}")
            print("インスタンスが完全に起動するまで少し待ってから再試行してください")
            return
        
        # SFTPでファイル転送
        sftp = ssh.open_sftp()
        
        try:
            sftp.put('claude-agent-deploy.tar.gz', '/home/ubuntu/claude-agent-deploy.tar.gz')
            sftp.put('setup_instance.sh', '/home/ubuntu/setup_instance.sh')
        except Exception as e:
            print(f"❌ ファイル転送エラー: {e}")
            return
        
        # セットアップスクリプト実行
        commands = [
            'chmod +x setup_instance.sh',
            './setup_instance.sh',
            'mkdir -p claude-agent-system',
            'tar -xzf claude-agent-deploy.tar.gz -C claude-agent-system/',
            'cd claude-agent-system && source venv/bin/activate && pip install -r requirements.txt',
        ]
        
        for cmd in commands:
            print(f"実行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            error = stderr.read().decode()
            if error:
                print(f"エラー: {error}")
                
        # systemdサービス作成
        service_content = '''[Unit]
Description=Claude Agent System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/claude-agent-system
Environment="PATH=/home/ubuntu/claude-agent-system/venv/bin"
ExecStart=/home/ubuntu/claude-agent-system/venv/bin/python -m src.agent dashboard
Restart=always

[Install]
WantedBy=multi-user.target
'''
        
        # サービスファイルをアップロード
        service_io = io.StringIO(service_content)
        sftp.putfo(service_io, '/tmp/claude-agent.service')
        
        # サービスの設定
        service_commands = [
            'sudo mv /tmp/claude-agent.service /etc/systemd/system/',
            'sudo systemctl daemon-reload',
            'sudo systemctl enable claude-agent',
            'sudo systemctl start claude-agent'
        ]
        
        for cmd in service_commands:
            print(f"実行: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            
        print("✅ デプロイ完了!")
        
        sftp.close()
        ssh.close()

if __name__ == '__main__':
    deployer = AgentDeployer()
    deployer.create_deployment_package()
    deployer.deploy_to_ec2()