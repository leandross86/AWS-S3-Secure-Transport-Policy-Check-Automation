import boto3
import json

def lambda_handler(event, context):
    # Inicialize o cliente S3
    s3_client = boto3.client('s3')
    
    # Liste todos os buckets na conta
    buckets = s3_client.list_buckets()
    
    # Defina a política padrão com aws:SecureTransport
    default_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [
                    "",
                    "/*"
                ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                }
            }
        ]
    }
    
    # Itera sobre cada bucket
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        
        # Verifica se o bucket existe
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"O bucket {bucket_name} não existe.")
                continue
            
        # Obtém a política do bucket (se existir)
        try:
            bucket_policy = s3_client.get_bucket_policy(Bucket=bucket_name)
            bucket_policy_json = json.loads(bucket_policy['Policy'])
        except s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                bucket_policy_json = None  # Se não houver política no bucket, defina como None
            else:
                print(f"Erro ao obter a política do bucket {bucket_name}: {str(e)}")
                continue
        
        # Verifica se a política contém a condição aws:SecureTransport em alguma declaração
        if bucket_policy_json is not None:
            if 'Statement' in bucket_policy_json:
                found_condition = False
                for statement in bucket_policy_json['Statement']:
                    if 'Condition' in statement and 'aws:SecureTransport' in statement['Condition']:
                        found_condition = True
                        break  # A política contém aws:SecureTransport, passa para o próximo bucket
                
                if not found_condition:
                    # Não encontrou a condição aws:SecureTransport em nenhuma declaração, atualiza a política
                    for statement in bucket_policy_json['Statement']:
                        if 'Action' in statement and 'Resource' in statement:
                            statement['Condition'] = {
                                "Bool": {
                                    "aws:SecureTransport": "false"
                                }
                            }
                            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy_json))
                            print(f"Política atualizada para o bucket {bucket_name}.")
                            break  # Atualizou a política, passa para o próximo bucket
            else:
                # Não encontrou declarações na política, cria a política padrão
                default_policy_copy = default_policy.copy()
                default_policy_copy['Statement'][0]['Resource'] = [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
                s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(default_policy_copy))
                print(f"Política padrão criada para o bucket {bucket_name}.")
        else:
            # Se não houver política no bucket, define a política padrão
            default_policy_copy = default_policy.copy()
            default_policy_copy['Statement'][0]['Resource'] = [
                f"arn:aws:s3:::{bucket_name}",
                f"arn:aws:s3:::{bucket_name}/*"
            ]
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(default_policy_copy))
            print(f"Política padrão criada para o bucket {bucket_name}.")
    
    return "Verificação e atualização de políticas concluídas."