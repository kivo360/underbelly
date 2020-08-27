from underbelly.envs.utils import *
from underbelly.envs.schemas import Identifier, EpisodeIdentifier
from underbelly.imports import *


class IDependenciesAbstract(abc.ABC, metaclass=VerificationType):
    """Dependencies Abstract

    Searches through all of the set variables and determines if all of the desired dependencies are there.

    Args:
        abc ([type]): Abstract
        metaclass (VerificationType, optional): Force runs a series of commands on the class when it inits. Defaults to VerificationType.

    Raises:
        AttributeError: You didn't add any dependencies. You need to add at least 1.
    """

    __keyword_placeholder: dict = {}
    __keyword_dependencies: dict = {}
    __iskwdepend: bool = False

    __initdepend: dict = {}
    __isinitdepend: bool = False

    __merged_depend: dict = {}

    _dependencies: AnyDict = {}
    dependencies: AnyDict = {}

    def __init__(self, *args, **kwargs) -> None:
        self.__keyword_placeholder = kwargs

    def __merge_set_dependencies(self):
        if not self.__iskwdepend and not self.__isinitdepend:
            raise AttributeError(
                "You didn't add any dependencies. You need to add at least 1."
            )
        while True:
            if not self.__isinitdepend:
                self.__merged_depend = self.__keyword_dependencies
                break
            if not self.__iskwdepend:
                self.__merged_depend = self.__initdepend
                break
            self.__merged_depend = toolz.dicttoolz.merge(
                self.__initdepend, self.__keyword_dependencies
            )
            break

        self.__merged_depend = collections.OrderedDict(
            sorted(self.__merged_depend.items())
        )
        _add_definition = add_definition(self)
        map(_add_definition, self.__merged_depend)

    def __extract_kwargs(self, **kwargs):
        keywords = self.__keyword_placeholder
        if is_falsy(keywords):
            self.__isinitdepend, self.__initdepend = {}, False
            return
        _, _, successful = is_match_dict(self.dependencies, kwargs)
        if len(successful) == 0: return
        self.__isinitdepend, self.__initdepend = True, merge(*successful)

    def __extract_init(self):
        current_dict = self.__dict__
        if is_falsy(current_dict):
            self.__isinitdepend, self.__initdepend = {}, False
            return
        _, _, successful = is_match_dict(self.dependencies, current_dict)
        if len(successful) == 0: return
        self.__isinitdepend, self.__initdepend = True, merge(*successful)

    def __consolidate_essentials(self):
        self._dependencies.update(self.dependencies)
        self.dependencies = copy.copy(self._dependencies)

    def __pull_keywords(self):
        is_valid, keywords = is_match_key_dict(
            self.dependencies, self.__keyword_placeholder, is_any=True
        )
        if not is_valid:
            self.__keyword_dependencies, self.__iskwdepend = {}, False
            return
        self.__keyword_dependencies, self.__iskwdepend = self.__extract_kwargs(**keywords)

    def _verify_fields(self):
        self.__consolidate_essentials()
        self.__pull_keywords()
        self.__extract_init()
        self.__merge_set_dependencies()

    def copy(self):
        return copy.deepcopy(self)
