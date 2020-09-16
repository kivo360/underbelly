from typing import Dict
from underbelly.envs import models
from underbelly.imports import *
from pydantic import BaseModel


class Hook:

    def __init__(self) -> None:
        self.name: str = uuid.uuid4().hex

    def process(self, obj: type):
        raise NotImplementedError(
            f"Hook not filled in for {self.name}. Can't run for {obj.__class__.name}."
        )

    def __repr__(self) -> str:
        return f"<Hook name={self.name}>"


class Module(metaclass=VerificationType):

    def __init__(self):
        self.setting_child = True
        self._parameters = OrderedDict()
        self._buffers = OrderedDict()
        self._non_persistent_buffers_set = set()
        self._backward_hooks = OrderedDict()
        self._forward_hooks = OrderedDict()
        self._init_hooks: Dict[str, Hook] = OrderedDict()
        self._forward_pre_hooks = OrderedDict()
        self._state_dict_hooks = OrderedDict()
        self._load_state_dict_pre_hooks = OrderedDict()
        self._modules = OrderedDict()
        self._parent = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def parent(self) -> Optional['Module']:
        return self._parent

    def is_highest(self) -> bool:
        """Is Highest

        Check if this if the highest level of the tree.

        Returns:
            bool: Returns true if there is no parent.
        """
        return self.parent is None

    def is_parent(self) -> bool:
        """Is Parent

        Check if this if we have a parent.

        Returns:
            bool: Returns true if there is a parent.
        """
        return self.parent is not None

    def is_base(self) -> bool:
        """Is Base Module

        Check if this if the highest level of the tree.

        Returns:
            bool: Returns true if there is no parent.
        """
        return self.__class__.__name__ == "Module"

    def is_children(self) -> bool:
        """Is Highest

        Check if this if the highest level of the tree.

        Returns:
            bool: Returns true if there is no parent.
        """
        return len(self._modules) > 0

    def is_child(self, module: 'Module') -> bool:
        """Is Highest

        Check if this if the highest level of the tree.

        Returns:
            bool: Returns true if there is no parent.
        """
        if module.name in self._modules:
            return isinstance(module, Module)
        return False

    def children(self) -> Iterator['Module']:
        r"""Returns an iterator over immediate children modules.
        Yields:
            Module: a child module
        """
        for name, module in self.named_children():
            yield module

    def named_children(self) -> Iterator[Tuple[str, 'Module']]:
        r"""Returns an iterator over immediate children modules, yielding both
        the name of the module as well as the module itself.
        Yields:
            (string, Module): Tuple containing a name and child module
        Example::
            >>> for name, module in model.named_children():
            >>>     if name in ['conv4', 'conv5']:
            >>>         print(module)
        """
        memo = set()
        for name, module in self._modules.items():
            if module is not None and module not in memo:
                memo.add(module)
                yield name, module

    def register_init_hook(self, hook: Hook):

        self._init_hooks[hook.name] = hook
        return hook

    def __getattr__(self, name: str) -> Union['Module']:
        if '_modules' in self.__dict__:
            modules = self.__dict__['_modules']
            if name in modules:
                return modules[name]
        raise AttributeError(
            "'{}' object has no attribute '{}'".format(
                type(self).__name__, name
            )
        )

    def __setattr__(self, name: str, value: Union['Module']) -> None:

        def remove_from(*dicts_or_sets):
            for d in dicts_or_sets:
                if name in d:
                    if isinstance(d, dict):
                        del d[name]
                    else:
                        d.discard(name)

        modules = self.__dict__.get('_modules')
        if isinstance(value, Module):
            if modules is None:
                raise AttributeError(
                    "cannot assign module before Module.__init__() call"
                )
            remove_from(
                self.__dict__,
                self._parameters,
                self._buffers,
                self._non_persistent_buffers_set
            )
            if self.setting_child:
                value.setting_child = False
                value._parent = self
                modules[name] = value
                value.setting_child = True
                return
            object.__setattr__(self, name, value)

        elif modules is not None and name in modules:
            if value is not None:
                raise TypeError(
                    "cannot assign '{}' as child module '{}' "
                    "(underbelly.module or None expected)".format(value, name)
                )
            value._parent = self
            modules[name] = value
        elif isinstance(value, Hook):
            hooks = self.__dict__.get('_init_hooks')
            if hooks is None:
                raise AttributeError(
                    "cannot assign hooks before Module.__init__() call"
                )
            self.register_init_hook(value)
        else:
            object.__setattr__(self, name, value)

    def tree_status(self, level=0):
        current_name = self.__class__.__name__
        is_children = self.is_children()
        is_highest = self.is_highest()
        tabs = "".join(["\t" for _ in range(level)])
        parent = self.parent
        if parent is not None:
            logger.info(parent.name)
        logger.info(
            f"{tabs}Module Name: {current_name} -- Is Children: {is_children} -- Is Highest: {is_highest}"
        )
        if is_children:
            level += 1
            for child in self.children():
                child.tree_status(level)

    def _post_init_hooks(self):
        for name, hook in self._init_hooks.items():
            hook.process(self)


def main():

    class PrintAttrHook(Hook):

        def __init__(self):
            super().__init__()

        def process(self, obj: object):
            logger.warning(len(obj.__dict__.keys()))

    class TimeModule(Module):

        def __init__(self) -> None:
            super().__init__()

    class SystemModule(Module):

        def __init__(self) -> None:
            super().__init__()
            self.timer = TimeModule()

            # Post __init__ hooks
            self.print_hook = PrintAttrHook()

    sample_module = SystemModule()
    sample_module.tree_status()


if __name__ == "__main__":
    main()