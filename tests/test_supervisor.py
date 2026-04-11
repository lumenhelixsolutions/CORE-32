import pytest

from core32.supervisor import Core32Supervisor, PolicyError


def test_basic_commit_path_logs_begin_and_commit():
    sup = Core32Supervisor(state=0)
    sup.execute("P_DELTA32", ctx="test")
    kinds = [r.kind for r in sup.log.records]
    assert kinds == ["BEGIN", "COMMIT"]
    assert sup.tick == 1


def test_membrane_blocks_phase_crossing_digit_payload():
    sup = Core32Supervisor(state=0)
    sup.set_membrane(False)
    with pytest.raises(PolicyError):
        sup.execute("P_PI10", ctx="test")


def test_swap_schedule_enforced():
    sup = Core32Supervisor(state=0)
    sup.set_sandbox(True)
    sup.execute("P_SWAPPAIR_0", ctx="test")
    with pytest.raises(PolicyError):
        sup.execute("P_SWAPPAIR_2", ctx="test")
    sup.execute("P_SWAPPAIR_1", ctx="test")
    assert sup.swap_cursor_k == 2
    assert sup.swap_epoch == 2


def test_digit_swap_requires_sandbox():
    sup = Core32Supervisor(state=0)
    with pytest.raises(PolicyError):
        sup.execute("P_SWAPPAIR_0", ctx="test")


def test_rollback_restores_last_payload():
    sup = Core32Supervisor(state=0)
    before = sup.state
    sup.execute("P_DELTA32", ctx="test")
    sup.rollback(reason="test")
    assert sup.state == before
    assert any(r.kind == "ROLLBACK" for r in sup.log.records)
