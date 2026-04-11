from core32.constants import DIGIT_CODES
from core32.primitives import cauldron_l32, cauldron_l32_inv, delta32, pi10, pi10_inv, rho32, rho32_inv


def test_delta_is_involution():
    for x in range(32):
        assert delta32(delta32(x)) == x


def test_rho_inverse_roundtrip():
    for x in range(32):
        assert rho32_inv(rho32(x)) == x
        assert rho32(rho32_inv(x)) == x


def test_pi10_respects_digit_codes_only():
    for x in range(32):
        y = pi10(x)
        if x in DIGIT_CODES:
            assert y in DIGIT_CODES
        else:
            assert y == x
        assert pi10_inv(pi10(x)) == x


def test_l32_roundtrip():
    for x in range(32):
        assert cauldron_l32_inv(cauldron_l32(x)) == x
