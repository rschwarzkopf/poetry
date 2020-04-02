from crashtest.contracts.solution import Solution


class PythonRequirementCompatibilitySolution(Solution):
    def __init__(self, exception):
        from poetry.mixology.incompatibility_cause import PythonCause
        from poetry.core.semver import parse_constraint

        self._title = "Check your dependencies Python requirement."

        failure = exception.error
        version_solutions = []
        for incompatibility in failure._incompatibility.external_incompatibilities:
            if isinstance(incompatibility.cause, PythonCause):
                root_constraint = parse_constraint(
                    incompatibility.cause.root_python_version
                )
                constraint = parse_constraint(incompatibility.cause.python_version)

                version_solutions.append(
                    "For <fg=default;options=bold>{}</>, a possible solution would be "
                    'to set the `<fg=default;options=bold>python</>` property to <fg=yellow>"{}"</>'.format(
                        incompatibility.terms[0].dependency.name,
                        root_constraint.intersect(constraint),
                    )
                )

        description = (
            "The Python requirement can be specified via the `<fg=default;options=bold>python</>` "
            "or `<fg=default;options=bold>markers</>` properties"
        )
        if version_solutions:
            description += "\n" + "\n".join(version_solutions)

        self._description = description

    @property
    def solution_title(self) -> str:
        return self._title

    @property
    def solution_description(self):
        return self._description

    @property
    def documentation_links(self):
        return [
            "https://python-poetry.org/docs/dependency-specification/#python-restricted-dependencies",
            "https://python-poetry.org/docs/dependency-specification/#using-environment-markers",
        ]
