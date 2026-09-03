import json,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"benchmarks/phase2/tasks.json"
RESULTS=ROOT/"benchmarks/phase2/results"

def load_tasks():
    with REGISTRY.open() as f:
        return json.load(f)

def new_run(candidate,commit,provider,model,task):
    return {
        "candidate":candidate,"candidate_commit":commit,
        "provider_id":provider,"model_id":model,
        "task_id":task["id"],"environment_id":"github-actions-ubuntu",
        "start_status":"NOT_STARTED","end_status":"NOT_STARTED",
        "success":False,"correctness":None,"duration_ms":None,
        "resource_cost":None,"tool_calls":[],
        "recovery_attempts":0,"final_state":None,
        "evidence_artifacts":[],"failure_classification":None
    }

if __name__=="__main__":
    tasks=load_tasks()
    print(f"PHASE2_RUNNER_READY tasks={len(tasks)}")
