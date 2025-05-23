# birth_app/management/commands/load_workflow.py
from django.core.management.base import BaseCommand
import yaml
from digit_client.services import WorkflowV2Service
from digit_client.request_config import RequestConfig
from digit_client.models import BusinessService, State, WorkflowAction

class Command(BaseCommand):
    help = "Load initial workflow configuration for BTR from a YAML file"

    def handle(self, *args, **options):
        with open('btr_workflow.yaml', 'r') as f:
            workflow_config = yaml.safe_load(f)  # parse YAML into dict:contentReference[oaicite:7]{index=7}
        wf_service = WorkflowV2Service()
        req_info = RequestConfig.get_request_info()

        # Example: assume YAML defines one businessService with states/actions
        svc = workflow_config['businessService']
        states = []
        for s in svc.get('states', []):
            actions = [WorkflowAction(tenant_id=svc['tenantId'], **a) for a in s.get('actions', [])]
            states.append(State(
                tenant_id=svc['tenantId'],
                business_service_id="",  # will be filled by service
                sla=s.get('sla'),
                state=s.get('state'),
                application_status=s.get('applicationStatus'),
                is_start_state=s.get('isStartState', False),
                is_terminate_state=s.get('isTerminateState', False),
                doc_upload_required=s.get('docUploadRequired', False),
                is_state_updatable=s.get('isStateUpdatable', False),
                actions=actions
            ))
        business_service = BusinessService(
            tenant_id=svc['tenantId'],
            business_service=svc['businessService'],
            business=svc['business'],
            states=states
        )
        # Create (or update) the workflow configuration in eGov Workflow service
        wf_service.create_business_service([business_service], request_info=req_info)
        self.stdout.write(self.style.SUCCESS("Workflow loaded successfully"))
