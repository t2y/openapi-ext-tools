import os

from ..utils.log import log
from ..utils.yaml import read_yaml, write_yaml


class BaseSpec:

    COMPONENTS = 'components'

    REF_FIELD = '$ref'

    def __init__(self, path,
                 read_func=read_yaml, write_func=write_yaml):
        self.path = path
        self.path_dir = os.path.dirname(path)
        self.read_func = read_yaml
        self.write_func = write_yaml

        self.data = None
        self.ref_filenames = set()
        self.ref_paths = []
        self.ref_spec = {}

    def __enter__(self):
        self.read()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self):
        self.data = self.read_func(self.path)

    def write(self, path):
        self.write_func(self.data, path)

    def get_external_refs_from_object(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                yield from self.get_external_refs_from_object(value)
            elif isinstance(value, list):
                yield from self.get_external_refs_from_list(value)

            if key == self.REF_FIELD:
                pos = value.find('#/')
                if pos > 0:
                    filename = value[:pos]
                    if os.path.basename(self.path) != filename:
                        yield filename

    def get_external_refs_from_list(self, data):
        for value in data:
            if isinstance(value, dict):
                yield from self.get_external_refs_from_object(value)
            elif isinstance(value, list):
                yield from self.get_external_refs_from_list(value)

    def get_external_refs(self, data):
        yield from self.get_external_refs_from_object(data)

    def walk(self, data):
        for filename in self.get_external_refs(data):
            self.ref_filenames.add(filename)

    def create_ref_spec(self, ref_path):
        with ReferenceSpec(ref_path) as spec:
            spec.resolve()
            spec.bundle()
        log.debug(f'created ref spec: {ref_path}')
        return spec

    def resolve(self):
        self.walk(self.data)

        for filename in self.ref_filenames:
            ref_path = os.path.join(self.path_dir, filename)
            self.ref_paths.append(ref_path)
            self.ref_spec[filename] = self.create_ref_spec(ref_path)

        self.replace_ref_fields(self.data)

    def replace_ref_fields(self, data):
        def replace(data, field, value):
            pos = value.find('#/')
            if pos > 0:
                filename = value[:pos]
                data[field] = value.replace(f'{filename}', '')
                log.debug(f'replaced ref field "{value}" to "{data[field]}"')

        for field, value in data.items():
            if isinstance(value, dict):
                self.replace_ref_fields(value)
            elif isinstance(value, list):
                for v in value:
                    self.replace_ref_fields({'dummy': v})

            if field == self.REF_FIELD:
                replace(data, field, value)

    def merge_components(self):
        components = self.data.get(self.COMPONENTS, {})
        for spec in self.ref_spec.values():
            spec_components = spec.data.get(self.COMPONENTS, {})
            for key, value in spec_components.items():
                components.setdefault(key, {})
                components[key].update(value)

    def bundle(self):
        self.merge_components()


class ReferenceSpec(BaseSpec):
    pass


class BundledSpec(BaseSpec):
    pass
