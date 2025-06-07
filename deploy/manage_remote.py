import click
import boto3
import paramiko
import json
from pathlib import Path
import sys

class RemoteManager:
    def __init__(self):
        self.ec2 = boto3.resource('ec2', region_name='ap-northeast-1')
        self.load_instance_info()
        
    def load_instance_info(self):
        try:
            with open('instance_info.json') as f:
                self.instance_info = json.load(f)
        except FileNotFoundError:
            self.instance_info = None
            
    def ssh_command(self, command):
        """SSHでコマンド実行"""
        if not self.instance_info:
            print("❌ インスタンス情報が見つかりません。先にインスタンスを起動してください。")
            return None
            
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
            return None
        
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        
        if error:
            print(f"エラー: {error}")
        
        return result

@click.group()
def cli():
    """Claude Agent リモート管理ツール"""
    pass

@cli.command()
def setup():
    """AWS環境をセットアップ"""
    from aws_setup import AWSSetup
    setup = AWSSetup()
    if setup.check_credentials():
        setup.create_key_pair()
        setup.create_security_group()

@cli.command()
def start():
    """EC2インスタンスを起動"""
    from ec2_launcher import EC2Launcher
    launcher = EC2Launcher()
    launcher.launch_instance()

@cli.command()
def stop():
    """EC2インスタンスを停止"""
    from ec2_launcher import EC2Launcher
    launcher = EC2Launcher()
    launcher.stop_instance()

@cli.command()
def terminate():
    """EC2インスタンスを削除"""
    from ec2_launcher import EC2Launcher
    launcher = EC2Launcher()
    launcher.terminate_instance()

@cli.command()
def deploy():
    """最新のコードをデプロイ"""
    from deploy_agent import AgentDeployer
    deployer = AgentDeployer()
    deployer.create_deployment_package()
    deployer.deploy_to_ec2()

@cli.command()
def status():
    """エージェントのステータス確認"""
    manager = RemoteManager()
    result = manager.ssh_command('sudo systemctl status claude-agent')
    if result:
        print(result)

@cli.command()
def logs():
    """ログを表示"""
    manager = RemoteManager()
    result = manager.ssh_command('tail -n 50 /home/ubuntu/claude-agent-system/logs/agent.log')
    if result:
        print(result)

@cli.command()
def restart():
    """エージェントを再起動"""
    manager = RemoteManager()
    result = manager.ssh_command('sudo systemctl restart claude-agent')
    if result is not None:
        print("✅ エージェントを再起動しました")

@cli.command()
def ssh():
    """SSH接続情報を表示"""
    manager = RemoteManager()
    if manager.instance_info:
        print(f"ssh -i ~/.ssh/claude-agent-key.pem ubuntu@{manager.instance_info['public_ip']}")
    else:
        print("インスタンス情報が見つかりません")

@cli.command()
def info():
    """インスタンス情報を表示"""
    manager = RemoteManager()
    if manager.instance_info:
        print(json.dumps(manager.instance_info, indent=2))
    else:
        print("インスタンス情報が見つかりません")

if __name__ == '__main__':
    cli()