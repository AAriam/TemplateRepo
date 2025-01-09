"""Hooks for different stages of the CCA pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from controlman.cache_manager import CacheManager
    from controlman.datatype import DynamicFile, DynamicDir
    from pyserials import NestedDict


class Hooks:
    """CCA Hooks.

    During control center synchronization events,
    this class is instantiated with the given parameters.
    Then, during each synchronization stage,
    if a corresponding method is defined in this class,
    that method will be called at that stage.

    Parameters
    ----------
    repo_path
        Path to the root of the repository.
    ccc
        Control center configurations
        from the existing `metadata.json` file
        on the current branch.
    ccc_main
        Control center configurations
        from the existing `metadata.json` file
        on the main branch.
    cache_manager
        Cache manager with `get` and `set` methods
        to retrieve and set cached values.
    github_token
        GitHub token for making authenticated GitHub API requests.
        This is always provided when running on the cloud,
        but on local machines it is only provided if the user explicitly
        inputs one.
    kwargs
        For forward compatibility with newer PyPackIT versions
        that may add additional input argument.
    """

    def __init__(
        self,
        repo_path: Path,
        ccc: NestedDict,
        ccc_main: NestedDict,
        cache_manager: CacheManager,
        github_token: str | None = None,
        **kwargs,
    ):
        self.repo_path = repo_path
        self.ccc = ccc
        self.ccc_main = ccc_main
        self.cache_manager = cache_manager
        self.github_token = github_token
        return

    def initialization(self) -> None:
        """Run hooks at the beginning of the CCA pipeline (stage 0)."""
        return

    def load(self, data: dict) -> None:
        """Run hooks after loading configurations from YAML files (stage 1).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            This only contains the configurations that are explicitly defined
            in the control center YAML files, plus any externally inherited data.
        """
        return

    def load_validation(self, data: dict) -> None:
        """Run hooks after validating the loaded configurations against the schema (stage 2).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            Compared to the `load` stage, this has added default values from the schema.
            Note that at this stage, default values are only added to existing configurations.
        """
        return

    def augmentation(self, data: dict) -> None:
        """Run hooks after augmenting configurations (stage 3).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            Compared to the `load_validation` stage, this has all additional
            data automatically generated by PyPackIT.
        """
        return

    def augmentation_validation(self, data: dict) -> None:
        """Run hooks after validating the augmented configurations against the schema (stage 4).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            Compared to the `augmentation` stage, this may have added default values from the schema.
            Note that at this stage, default values are only added to existing configurations.
        """
        return

    def templating(self, data: dict) -> None:
        """Run hooks after resolving templates (stage 5).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            Compared to the `augmentation_validation` stage, this has all
            templates resolved.
        """
        return

    def templating_validation(self, data: dict) -> None:
        """Run hooks after validating the final configurations against the schema (stage 6).

        Parameters
        ----------
        data
            Top-level mapping containing all control center configurations.
            This is the complete form of the configurations with all default values
            added.
        """
        return

    def output_generation(self, data: dict, files: list[DynamicFile], dirs: list[DynamicDir]) -> None:
        """Run hooks after generating outputs (stage 7).

        Parameters
        ----------
        data
            Complete control center configurations.
            Note that modifying this dictionary at this stage
            will have no effects, since all dynamic content are already generated.
        files
            List of dynamic files.
        dirs
            List of dynamic directories.
        """
        return

    def synchronization(self) -> None:
        """Run hooks after synchronizing the repository (stage 8).

        This is the last stage of the pipeline.
        """
        return
