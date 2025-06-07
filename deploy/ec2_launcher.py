import boto3
import time
import json
from pathlib import Path

class EC2Launcher:
    def __init__(self):
        self.ec2 = boto3.resource('ec2', region_name='ap-northeast-1')
        self.ec2_client = boto3.client('ec2', region_name='ap-northeast-1')
        
    def get_latest_ubuntu_ami(self):
        """最新のUbuntu 22.04 AMIを取得"""
        response = self.ec2_client.describe_images(
            Filters=[
                {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
                {'Name': 'state', 'Values': ['available']}
            ],
            Owners=['099720109477']  # Canonical
        )
        
        images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        return images[0]['ImageId']
    
    def launch_instance(self, instance_name='claude-agent-instance'):
        """EC2インスタンスを起動"""
        print("🚀 EC2インスタンスを起動中...")
        
        # ユーザーデータスクリプト（起動時に実行）
        user_data = '''#!/bin/bash
        apt-get update
        apt-get install -y python3-pip python3-venv git
        '''
        
        instances = self.ec2.create_instances(
            ImageId=self.get_latest_ubuntu_ami(),
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',  # 無料枠
            KeyName='claude-agent-key',
            SecurityGroups=['claude-agent-sg'],
            UserData=user_data,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': instance_name}]
            }]
        )
        
        instance = instances[0]
        print(f"⏳ インスタンス {instance.id} の起動を待機中...")
        
        instance.wait_until_running()
        instance.reload()
        
        print(f"✅ インスタンスが起動しました!")
        print(f"   ID: {instance.id}")
        print(f"   パブリックIP: {instance.public_ip_address}")
        print(f"   SSH接続: ssh -i ~/.ssh/claude-agent-key.pem ubuntu@{instance.public_ip_address}")
        
        # インスタンス情報を保存
        instance_info = {
            'instance_id': instance.id,
            'public_ip': instance.public_ip_address,
            'launch_time': str(instance.launch_time)
        }
        
        Path('instance_info.json').write_text(json.dumps(instance_info, indent=2))
        
        return instance

    def stop_instance(self, instance_id=None):
        """インスタンスを停止"""
        if not instance_id:
            # 保存された情報から取得
            info = json.loads(Path('instance_info.json').read_text())
            instance_id = info['instance_id']
        
        instance = self.ec2.Instance(instance_id)
        instance.stop()
        print(f"⏸️  インスタンス {instance_id} を停止中...")
        instance.wait_until_stopped()
        print("✅ インスタンスを停止しました")

    def terminate_instance(self, instance_id=None):
        """インスタンスを削除"""
        if not instance_id:
            info = json.loads(Path('instance_info.json').read_text())
            instance_id = info['instance_id']
        
        instance = self.ec2.Instance(instance_id)
        instance.terminate()
        print(f"🗑️  インスタンス {instance_id} を削除中...")
        instance.wait_until_terminated()
        print("✅ インスタンスを削除しました")

if __name__ == '__main__':
    launcher = EC2Launcher()
    launcher.launch_instance()