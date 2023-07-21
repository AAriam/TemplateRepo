
# Standard libraries
from typing import Literal
import datetime
from pathlib import Path
# Non-standard libraries
import tomlkit
import tomlkit.items


class PyProjectTOML:

    def __init__(self, metadata: dict, path_pyproject: str | Path = "./pyproject.toml"):
        with open(path_pyproject) as f:
            self._file: tomlkit.TOMLDocument = tomlkit.load(f)
        self._metadata: dict = metadata
        return

    def update_header_comment(self):
        lines = [
            f"{self._metadata['project_name']} pyproject.toml File.",
            (
                "Automatically generated on "
                f"{datetime.datetime.utcnow().strftime('%Y.%m.%d at %H:%M:%S UTC')} "
                f"by PyPackIT {pypackit.__version__}"
            ),
            "This file contains build system requirements and information,",
            " which are used by pip to build the package.",
            " For more information, see https://pypackit.readthedocs.io",
        ]
        for line_idx, line in enumerate(lines):
            self._file.body[line_idx][1].trivia.comment = f"# {line}"
        return

    def update_project_table(self):


        data_type = {
            "name": ("str", self._metadata['package']['name']),
            "description": ("str", self._metadata['project']['tagline']),
            "readme": ("str", self._metadata['paths']['pypi_readme']),
            "requires-python": ("str", f">= {self._metadata['package']['python_version_min']}"),
            "license": ("inline_table", {"file": self._metadata['paths']['licenses'][0]}),
            "authors": "array_of_inline_tables",
            "maintainers": "array_of_inline_tables",
            "keywords": ("array", self._metadata['project']['keywords']),
            "classifiers": ("array", self._metadata['package']['trove_classifiers']),
            "urls": (
                "table",
                {
                    "Homepage": "",
                    "Download": "",
                    "News": "",
                    "Documentation": "",
                    "Bug Tracker": "",
                    "Sponsor": "",
                    "Source": ""
                }
            ),
            "scripts": "table",
            "gui-scripts": "table",
            "entry-points": "table_of_tables",
            "dependencies": (
                "array",
                (
                    [dep['pip_spec'] for dep in self._metadata['package']['dependencies']]
                    if self._metadata['package']['dependencies'] else None
                )
            ),
            "optional-dependencies": (
                "table_of_arrays",
                (
                    {
                        group_name: [dep['pip_spec'] for dep in deps]
                        for group_name, deps in self._metadata['package']['optional_dependencies'].items()
                    }
                    if self._metadata['package']['optional_dependencies'] else None
                )
            ),
        }
        for key, (dtype, val) in data_type.items():
            if dtype == 'str':
                toml_val = val
            elif dtype == 'array':
                toml_val = tomlkit.array(val).multiline(True)
            elif dtype == 'table':
                toml_val = val
            elif dtype == 'inline_table':
                toml_val = tomlkit.inline_table().update(val)
            elif dtype == 'array_of_inline_tables':
                toml_val = tomlkit.array().multiline(True)
                for table in val:
                    toml_val.append(tomlkit.inline_table().update(table))
            elif dtype == 'table_of_arrays':
                toml_val = {
                    tab_key: tomlkit.array(arr).multiline(True)
                    for tab_key, arr in val.items()
                }
            elif dtype == 'table_of_tables':
                toml_val = tomlkit.table(is_super_table=True).update(val)
            else:
                raise ValueError(f"Unknown data type {dtype} for key {key}.")
            self._file['project'][key] = toml_val
        return

    
    def _update_project_authors_maintainers(self, role: Literal['authors', 'maintainers']):
        people = tomlkit.array().multiline(True)
        for person in self._metadata['project'][role]:
            person_dict = dict(name=person['name'])
            if person.get('email'):
                person_dict['email'] = person['email']
            people.append(tomlkit.inline_table().update(person_dict))
        self._file['project'][role] = people
    
    def update_project_authors(self):
        """
        Update the project authors in the pyproject.toml file.

        References
        ----------
        https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#authors-maintainers
        """
        return self._update_project_authors_maintainers(role='authors')

    def update_project_maintainers(self):
        """
        Update the project maintainers in the pyproject.toml file.

        References
        ----------
        https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#authors-maintainers
        """
        return self._update_project_authors_maintainers(role='maintainers')

    def update_project_urls(self):
        """
        Update the project urls in the pyproject.toml file.

        References
        ----------
        https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#urls
        """
        urls = tomlkit.inline_table()
        for url_key, url_val in self._metadata['urls'].items():
            urls[url_key] = url_val
        self._file['project']['urls'] = urls
        return


    def update_versioningit_onbuild(self):
        tab = self._file['tool']['versioningit']['onbuild']
        tab['source-file'] =  f"src/{self._metadata['package']['name']}/__init__.py"
        tab['build-file'] = f"{self._metadata['package']['name']}/__init__.py"
        return


def from_filepath(filepath):
    file = pypackit.jsons.read(filepath)

