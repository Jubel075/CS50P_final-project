import pytest

import project
from project import rectifying_line, stripping_line, feed_intersec


# ---------------------------------------------------------------------------
# CoolProp user input: get_component
#
# get_component() loops on input() until PropsSI() accepts the fluid name.
# We monkeypatch both so the tests never block on real keyboard input or
# depend on the CoolProp fluid database.
# ---------------------------------------------------------------------------

def make_input(responses):
    """Return a fake input() that yields the given responses in order."""
    it = iter(responses)
    return lambda prompt="": next(it)


def test_get_component_valid(monkeypatch):
    # PropsSI accepts anything -> first valid name is returned, stripped.
    monkeypatch.setattr("builtins.input", make_input(["  Benzene  "]))
    monkeypatch.setattr(project, "PropsSI", lambda *args, **kwargs: 562.0)
    assert project.get_component("light") == "Benzene"


def test_get_component_rejects_then_accepts(monkeypatch):
    # First name raises (unknown fluid), second is accepted.
    monkeypatch.setattr("builtins.input", make_input(["Nonsense", "Toluene"]))

    def fake_propssi(prop, name):
        if name == "Toluene":
            return 591.0
        raise ValueError("unknown fluid")

    monkeypatch.setattr(project, "PropsSI", fake_propssi)
    assert project.get_component("heavy") == "Toluene"


def test_get_component_handles_runtimeerror(monkeypatch):
    # CoolProp can raise RuntimeError too; it should keep prompting.
    monkeypatch.setattr("builtins.input", make_input(["Bad", "Benzene"]))

    def fake_propssi(prop, name):
        if name == "Benzene":
            return 562.0
        raise RuntimeError("bad input")

    monkeypatch.setattr(project, "PropsSI", fake_propssi)
    assert project.get_component("light") == "Benzene"


# ---------------------------------------------------------------------------
# Operating lines: rectifying_line, stripping_line, feed_intersec
# ---------------------------------------------------------------------------

def test_rectifying_line_passes_through_xD():
    # The rectifying line always passes through (xD, xD) on the y = x diagonal.
    xD, R = 0.95, 2.0
    assert rectifying_line(xD, R, xD) == pytest.approx(xD)


def test_rectifying_line_value():
    # y = R/(R+1) * x + xD/(R+1)  ->  with R=3, xD=0.9, x=0.5
    # = 0.75 * 0.5 + 0.225 = 0.6
    assert rectifying_line(0.5, 3.0, 0.9) == pytest.approx(0.6)


def test_stripping_line_passes_through_xB():
    # The stripping line passes through the bottoms point (xB, xB).
    xB = 0.05
    assert stripping_line(xB, 0.5, 0.6, xB) == pytest.approx(xB)


def test_stripping_line_passes_through_intersection():
    # By construction it also passes through (x_int, y_int).
    x_int, y_int, xB = 0.5, 0.6, 0.05
    assert stripping_line(x_int, x_int, y_int, xB) == pytest.approx(y_int)


def test_feed_intersec_saturated_liquid():
    # q = 1 -> vertical q-line at x = zF, y on the rectifying line.
    zF, q, R, xD = 0.5, 1.0, 2.0, 0.95
    x, y = feed_intersec(zF, q, R, xD)
    assert x == pytest.approx(zF)
    assert y == pytest.approx(rectifying_line(zF, R, xD))


def test_feed_intersec_lies_on_both_lines():
    # For a general q, the point must satisfy the rectifying line and the
    # q-line:  y = q/(q-1) * x - zF/(q-1).
    zF, q, R, xD = 0.5, 0.6, 2.0, 0.95
    x, y = feed_intersec(zF, q, R, xD)
    assert y == pytest.approx(rectifying_line(x, R, xD))
    assert y == pytest.approx(q / (q - 1) * x - zF / (q - 1))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
