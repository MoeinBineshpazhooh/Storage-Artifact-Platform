"""Offline validation for storage examples, Compose YAML and documentation."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDS = {
    'ceph/kubernetes/rook-ceph/operator.yaml',
    'ceph/kubernetes/rook-ceph/cluster.yaml',
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise yaml.constructor.ConstructorError(
                'mapping', node.start_mark, f'duplicate key: {key}', key_node.start_mark
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def validate(root):
    errors = []
    resources = []
    paths = sorted(p for p in root.rglob('*') if p.is_file() and not any(
        part in ('.git', '.venv', '__pycache__') for part in p.parts
    ))
    for path in paths:
        relative = str(path.relative_to(root))
        if not re.search(r'\.(yaml|yml)(\.example)?$', relative):
            continue
        try:
            documents = list(yaml.load_all(path.read_text(), Loader=UniqueKeyLoader))
            if not documents:
                if relative not in SCAFFOLDS:
                    raise ValueError('empty YAML is not a documented scaffold')
                continue
            for doc in documents:
                if not isinstance(doc, dict):
                    raise ValueError('expected a YAML mapping')
                if relative.startswith('.github/workflows/'):
                    continue
                if 'services' in doc:  # Compose examples
                    if not isinstance(doc['services'], dict) or not doc['services']:
                        raise ValueError('Compose needs a nonempty services mapping')
                    continue
                if not doc.get('apiVersion') or not doc.get('kind') or not doc.get('metadata', {}).get('name'):
                    # The Harbor installer config is YAML, not a Kubernetes resource.
                    if relative == 'harbor/installation/docker-compose/harbor.yml.example':
                        continue
                    raise ValueError('resource needs apiVersion, kind and metadata.name')
                resources.append((path, doc))
        except (yaml.YAMLError, ValueError, TypeError, AttributeError) as error:
            errors.append(f'{relative}: {error}')

    claims = {(path.parent, doc['metadata'].get('namespace', 'default'), doc['metadata']['name'])
              for path, doc in resources if doc['kind'] == 'PersistentVolumeClaim'}
    for path, doc in resources:
        try:
            if doc['kind'] not in ('Deployment', 'Pod'):
                continue
            spec = doc['spec']
            pod_spec = spec['template']['spec'] if doc['kind'] == 'Deployment' else spec
            volumes = {v['name']: v for v in pod_spec.get('volumes', [])}
            for container in pod_spec.get('containers', []):
                for mount in container.get('volumeMounts', []):
                    if mount['name'] not in volumes:
                        raise ValueError(f'unknown mounted volume {mount["name"]}')
            pvc_volumes = [v for v in volumes.values() if 'persistentVolumeClaim' in v]
            for volume in pvc_volumes:
                claim = volume['persistentVolumeClaim']['claimName']
                if (path.parent, doc['metadata'].get('namespace', 'default'), claim) not in claims:
                    raise ValueError(f'PVC {claim} has no example in this directory/namespace')
            if doc['kind'] == 'Deployment':
                labels = spec['template']['metadata'].get('labels', {})
                if not all(labels.get(k) == v for k, v in spec['selector']['matchLabels'].items()):
                    raise ValueError('Deployment selector does not match pod labels')
                if pvc_volumes and (spec.get('replicas', 1) != 1 or spec.get('strategy', {}).get('type') != 'Recreate'):
                    raise ValueError('single-volume lab Deployment needs one replica and Recreate')
        except (KeyError, ValueError, TypeError, AttributeError) as error:
            errors.append(f'{path.relative_to(root)}: {error}')

    for path in paths:
        if path.suffix != '.md':
            continue
        text = path.read_text()
        if any(marker in text for marker in ('\ue200', '\ue201', '\ue202')):
            errors.append(f'{path.relative_to(root)}: unsupported chat rendering markup')
        text = re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text)
        for target in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
            parts = urlsplit(target.strip('<>'))
            if parts.scheme or parts.netloc or not parts.path:
                continue
            destination = (path.parent / unquote(parts.path)).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'{path.relative_to(root)}: missing local link {target}')
    return errors


if __name__ == '__main__':
    errors = validate(ROOT)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        sys.exit(1)
    print('PASS: YAML syntax, unique keys, storage example consistency and local Markdown links')
