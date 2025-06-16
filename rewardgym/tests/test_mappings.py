import types

from rewardgym._mapping import discover_classes


def test_discover_classes_finds_only_defined_classes():
    # Create a fake module
    fake_module = types.ModuleType("fake_module")

    # Define two classes inside the fake module
    class ClassA:
        pass

    class ClassB:
        pass

    # Manually assign them to the fake module namespace and adjust __module__
    ClassA.__module__ = "fake_module"
    ClassB.__module__ = "fake_module"
    fake_module.ClassA = ClassA
    fake_module.ClassB = ClassB

    # Add an imported class (should be excluded)
    import datetime

    fake_module.ExternalClass = datetime.datetime

    result = discover_classes(fake_module)

    # Should only return ClassA and ClassB
    assert set(result.keys()) == {"ClassA", "ClassB"}
    assert result["ClassA"] is ClassA
    assert result["ClassB"] is ClassB
