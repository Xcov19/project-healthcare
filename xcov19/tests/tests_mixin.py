import pytest
from xcov19.utils.mixins import InterfaceProtocolCheckMixin


class BaseClass:
    @classmethod
    def method_with_params(cls, param1: int, param2: str) -> None:
        pass


def test_incorrect_implementation_missing_method():
    # Define IncorrectImplementation inside the test function
    try:

        class IncorrectImplementation(BaseClass, InterfaceProtocolCheckMixin):
            """Does not implement method_with_params"""

            pass

        IncorrectImplementation()

    except NotImplementedError as exec:
        assert (
            str(exec)
            == "The method 'method_with_params' is inherited from the parent class 'BaseClass' and not overridden/declared."
        )


def test_correct_implementation():
    class CorrectImplementation(BaseClass, InterfaceProtocolCheckMixin):
        @classmethod
        def method_with_params(cls, param1: int, param2: str) -> None:
            pass

    try:
        instance = CorrectImplementation()
        instance.method_with_params(1, "test")
        assert True
    except Exception as e:
        pytest.fail(f"CorrectImplementation raised an exception: {e}")
