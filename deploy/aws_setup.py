import boto3
import json
import os
from pathlib import Path

class AWSSetup:
    def __init__(self):
        self.ec2 = boto3.client('ec2', region_name='ap-northeast-1')
        self.iam = boto3.client('iam')
        
    def check_credentials(self):
        """AWS認証情報の確認"""
        try:
            self.ec2.describe_regions()
            print("✅ AWS認証情報が正しく設定されています")
            return True
        except Exception as e:
            print(f"❌ AWS認証エラー: {e}")
            print("以下のコマンドでAWS CLIを設定してください:")
            print("aws configure")
            return False
    
    def create_key_pair(self, key_name='claude-agent-key'):
        """SSH用のキーペアを作成"""
        try:
            response = self.ec2.create_key_pair(KeyName=key_name)
            
            # 秘密鍵を保存
            key_path = Path.home() / '.ssh' / f'{key_name}.pem'
            key_path.parent.mkdir(exist_ok=True)
            key_path.write_text(response['KeyMaterial'])
            key_path.chmod(0o400)
            
            print(f"✅ キーペアを作成しました: {key_path}")
            return str(key_path)
        except self.ec2.exceptions.ClientError as e:
            if 'InvalidKeyPair.Duplicate' in str(e):
                print(f"キーペア {key_name} は既に存在します")
                return str(Path.home() / '.ssh' / f'{key_name}.pem')
            raise

    def create_security_group(self, group_name='claude-agent-sg'):
        """セキュリティグループの作成"""
        try:
            response = self.ec2.create_security_group(
                GroupName=group_name,
                Description='Security group for Claude Agent System'
            )
            
            sg_id = response['GroupId']
            
            # SSH接続を許可
            self.ec2.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[{
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # 本番環境では制限推奨
                }]
            )
            
            print(f"✅ セキュリティグループを作成しました: {sg_id}")
            return sg_id
        except self.ec2.exceptions.ClientError as e:
            if 'InvalidGroup.Duplicate' in str(e):
                # 既存のセキュリティグループを取得
                response = self.ec2.describe_security_groups(
                    GroupNames=[group_name]
                )
                return response['SecurityGroups'][0]['GroupId']
            raise

if __name__ == '__main__':
    setup = AWSSetup()
    if setup.check_credentials():
        setup.create_key_pair()
        setup.create_security_group()