import inspect


class InterfaceProtocolCheckMixin:
    """Checks for correct signature used by the implementation class.

    Drop in mixin wherever an implementation is subclasses with an
    interface definition.
    """

    def __init_subclass__(cls, **kwargs):
        parent_class = inspect.getmro(cls)[1]
        for defined_method in (
            method
            for method in dir(cls)
            if not method.startswith("__") and callable(getattr(cls, method))
        ):
            cls_method = getattr(parent_class, defined_method)
            subclass_method = getattr(cls, defined_method)
            cls_method_params = inspect.signature(cls_method).parameters
            subclass_method_params = inspect.signature(subclass_method).parameters
            if cls_method_params.keys() != subclass_method_params.keys():
                raise NotImplementedError(f"""Signature for {defined_method} not correct:
                Expected: {list(cls_method_params.keys())}
                Got: {list(subclass_method_params.keys())}
                """)
        super().__init_subclass__(**kwargs)
