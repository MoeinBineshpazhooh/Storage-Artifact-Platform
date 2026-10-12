import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, root / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

validator = load('validator', 'scripts/validate.py')
assert not validator.validate(root), validator.validate(root)
cases = [
    ('ceph/kubernetes/external-ceph/storageclass-rbd.yaml', lambda t: t.replace('reclaimPolicy: Retain', 'reclaimPolicy: Delete'), 'must retain data'),
    ('manifests/minio/docker-compose.yaml', lambda t: t.replace('MINIO_ROOT_PASSWORD:?', 'MINIO_ROOT_PASSWORD:-'), 'must be explicitly required'),
    ('manifests/longhorn/storageclass-pvc.yaml', lambda t: t.replace('claimName: demo-longhorn-pvc', 'claimName: missing-pvc'), 'has no example'),
    ('manifests/longhorn/storageclass-pvc.yaml', lambda t: t.replace('type: Recreate', 'type: RollingUpdate'), 'needs one replica and Recreate'),
    ('ceph/kubernetes/external-ceph/pvc.yaml', lambda t: t + '\nkind: Pod\n', 'duplicate key'),
    ('README.md', lambda t: t + '\n[Missing](no-file.md)\n', 'missing local link'),
    ('ceph/kubernetes/external-ceph/pvc.yaml', lambda t: '', 'empty YAML'),
]
for filename, mutate, expected in cases:
    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / 'repo'
        shutil.copytree(root, copy)
        path = copy / filename
        path.write_text(mutate(path.read_text()))
        errors = validator.validate(copy)
        assert any(expected in error for error in errors), errors
        print('PASS: validator rejects', expected)

persistence = load('persistence', 'scripts/check-persistence.py')
for scenario in ['persisted', 'lost', 'unchanged', 'unsafe-strategy']:
    state = {'restarted': False, 'token': None}
    def fake(namespace, *args):
        if args[:2] == ('get', 'deployment'):
            return json.dumps({'spec': {'replicas': 1, 'strategy': {'type': 'RollingUpdate' if scenario == 'unsafe-strategy' else 'Recreate'}, 'selector': {'matchLabels': {'app': 'test'}}, 'template': {'spec': {'containers': [{'name': 'test', 'volumeMounts': [{'name': 'data', 'mountPath': '/data'}]}], 'volumes': [{'name': 'data', 'persistentVolumeClaim': {'claimName': 'test'}}]}}}})
        if args[:2] == ('get', 'pods'):
            uid = 'new' if state['restarted'] and scenario != 'unchanged' else 'old'
            return json.dumps({'items': [{'metadata': {'name': uid, 'uid': uid}, 'status': {'conditions': [{'type': 'Ready', 'status': 'True'}]}}]})
        if args[:2] == ('rollout', 'restart'):
            state['restarted'] = True
        if args[0] == 'exec' and 'sh' in args:
            state['token'] = args[-2]
        if args[0] == 'exec' and 'cat' in args:
            return 'lost' if state['restarted'] and scenario == 'lost' else state['token']
        return ''
    persistence.kubectl = fake
    try:
        persistence.run('lab', 'test')
        assert scenario == 'persisted'
    except ValueError:
        assert scenario != 'persisted'
    if scenario == 'unsafe-strategy':
        assert not state['restarted']
    print('PASS: persistence helper scenario', scenario)
