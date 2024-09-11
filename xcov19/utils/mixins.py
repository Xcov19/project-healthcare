import inspect
import operator
from typing import Tuple, Any, TypeVar, get_type_hints

ClassNameAttrGetter = operator.attrgetter("__name__")
BoundAttrGetter = operator.attrgetter("__bound__")


def match_signature(
    cls_signature: Tuple[str, Any], subclass_signature: Tuple[str, Any]
):
    """Match inspect signature by their names and type annotation."""
    param_name, param_type = cls_signature
    subcls_param_name, subcls_param_type = subclass_signature
    if param_name != subcls_param_name:
        raise NotImplementedError(
            f"""Method name mismatch:
                            Expected: {param_name}
                            Got: {subcls_param_name}
                            """
        )

    if ClassNameAttrGetter(param_type) != ClassNameAttrGetter(subcls_param_type):
        if (
            isinstance(param_type, TypeVar)
            and BoundAttrGetter(param_type) == subcls_param_type
        ):
            return True
        raise NotImplementedError(
            f"""
                            Signature mismatch for parameter {param_name}:
                            Expected: {param_type}
                            Got: {subcls_param_type}
                            """
        )
    return True


class InterfaceProtocolCheckMixin:
    """Checks for correct signature used by the implementation class.

    Drop in mixin wherever an implementation is subclasses with an
    interface definition.
    """

    def __init_subclass__(cls, **kwargs):
        parent_class = inspect.getmro(cls)[1]
        # raise Exception(inspect.getmembers(cls, predicate=inspect.isfunction))
        for defined_method in (
            method_name
            for method_name, _ in inspect.getmembers(cls, predicate=inspect.ismethod)
            if not method_name.startswith("__")
        ):
            # TODO: Raise if either classes don't have the method declared.

            try:
                # Get the method from both the parent and subclass
                cls_method = getattr(parent_class, defined_method)
                subclass_method = getattr(cls, defined_method)

                # Ensure the method is declared/overridden in the subclass and not just inherited
                if defined_method in cls.__dict__:
                    pass
                else:
                    raise NotImplementedError(
                        f"The method '{defined_method}' is inherited from the parent class '{parent_class.__name__}' and not overridden/declared."
                    )
            except AttributeError:
                raise NotImplementedError(
                    f"Method '{defined_method}' not found in parent class."
                )

            cls_method_params: dict = get_type_hints(cls_method)
            subclass_method_params: dict = get_type_hints(subclass_method)
            if len(cls_method_params) != len(subclass_method_params):
                raise NotImplementedError(f"""Method parameters mismatch:
                Expected: {cls_method_params.keys()}
                Got: {subclass_method_params.keys()}
                """)
            for cls_signature, subclass_signature in zip(
                cls_method_params.items(), subclass_method_params.items()
            ):
                match_signature(cls_signature, subclass_signature)
        super().__init_subclass__(**kwargs)
