from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient


def handler(event, context):
    credentials, subscription_id = get_credentials(event)
    resource_group = event['environment_params']['resource_group']

    client = RecoveryServicesClient(credentials, subscription_id)
    backup_client = RecoveryServicesBackupClient(credentials, subscription_id)
    for vault in client.vaults.list_by_resource_group(resource_group):
        for backup_job in backup_client.backup_jobs.list(vault.name, resource_group):
            if backup_job.properties.operation == 'Restore':
                return True
    return False


def get_credentials(event):
    subscription_id = event['environment_params']['subscription_id']
    credentials = ServicePrincipalCredentials(
        client_id=event['credentials']['credential_id'],
        secret=event['credentials']['credential_key'],
        tenant=event['environment_params']['tenant']
    )
    return credentials, subscription_id
