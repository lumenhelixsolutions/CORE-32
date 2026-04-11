"""Small verification helper for the repository scaffold.

This is not a replacement for the full supplementary scripts mentioned in the papers.
It checks basic involution and inverse relations for the implemented CORE-32 primitives.
"""

from core32.primitives import cauldron_l32, cauldron_l32_inv, delta32, pi10, pi10_inv, rho32, rho32_inv


def verify() -> None:
    for x in range(32):
        assert delta32(delta32(x)) == x
        assert rho32_inv(rho32(x)) == x
        assert rho32(rho32_inv(x)) == x
        assert pi10_inv(pi10(x)) == x
        assert pi10(pi10_inv(x)) == x
        assert cauldron_l32_inv(cauldron_l32(x)) == x
        assert cauldron_l32(cauldron_l32_inv(x)) == x
    print("ok")


if __name__ == "__main__":
    verify()
