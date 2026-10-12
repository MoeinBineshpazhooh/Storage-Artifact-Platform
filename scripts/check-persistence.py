"""Restart one disposable test Deployment and verify a unique PVC marker survives."""
import argparse
import json
import subprocess
import uuid


def kubectl(namespace, *args):
    return subprocess.run(
        ['kubectl', '-n', namespace, *args], check=True, text=True,
        stdout=subprocess.PIPE, timeout=360,
    ).stdout.strip()


def run(namespace, deployment):
    data = json.loads(kubectl(namespace, 'get', 'deployment', deployment, '-o', 'json'))
    spec = data['spec']
    if spec.get('replicas', 1) != 1 or spec.get('strategy', {}).get('type') != 'Recreate':
        raise ValueError('Use a single-replica disposable test Deployment with Recreate strategy')
    selector = spec['selector']
    if selector.get('matchExpressions') or not selector.get('matchLabels'):
        raise ValueError('This helper requires a matchLabels-only selector')
    labels = ','.join(f'{key}={value}' for key, value in selector['matchLabels'].items())
    template = spec['template']['spec']
    volumes = {v['name']: v for v in template.get('volumes', [])}
    candidates = [c['name'] for c in template['containers'] if any(
        mount['mountPath'] == '/data' and 'persistentVolumeClaim' in volumes.get(mount['name'], {})
        for mount in c.get('volumeMounts', [])
    )]
    if len(candidates) != 1:
        raise ValueError('Exactly one container must mount a PVC at /data')
    container = candidates[0]

    def ready_pod():
        items = json.loads(kubectl(namespace, 'get', 'pods', '-l', labels, '-o', 'json'))['items']
        pods = [p for p in items if not p['metadata'].get('deletionTimestamp') and any(
            c.get('type') == 'Ready' and c.get('status') == 'True'
            for c in p.get('status', {}).get('conditions', [])
        )]
        if len(pods) != 1:
            raise ValueError('Expected exactly one Ready test pod for the selector')
        return pods[0]['metadata']['name'], pods[0]['metadata']['uid']

    kubectl(namespace, 'rollout', 'status', f'deployment/{deployment}', '--timeout=300s')
    old_name, old_uid = ready_pod()
    token = uuid.uuid4().hex
    marker = f'/data/.persistence-check-{token}'
    kubectl(namespace, 'exec', old_name, '-c', container, '--', 'sh', '-c',
            'set -eu; printf "%s" "$1" > "$2"; sync', 'sh', token, marker)
    if kubectl(namespace, 'exec', old_name, '-c', container, '--', 'cat', marker) != token:
        raise ValueError('Initial marker read failed')
    # This changes only the selected test Deployment's pod template annotation.
    kubectl(namespace, 'rollout', 'restart', f'deployment/{deployment}')
    kubectl(namespace, 'rollout', 'status', f'deployment/{deployment}', '--timeout=300s')
    new_name, new_uid = ready_pod()
    if new_uid == old_uid:
        raise ValueError('Pod was not replaced')
    if kubectl(namespace, 'exec', new_name, '-c', container, '--', 'cat', marker) != token:
        raise ValueError(f'Persistence failed; inspect marker {marker}')
    kubectl(namespace, 'exec', new_name, '-c', container, '--', 'rm', '--', marker)
    print('PASS: unique PVC marker survived pod replacement')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--namespace', required=True)
    parser.add_argument('--deployment', required=True)
    arguments = parser.parse_args()
    run(arguments.namespace, arguments.deployment)
