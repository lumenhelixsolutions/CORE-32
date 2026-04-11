from core32.schedule import FrozenSwapSchedule


def test_moment_is_strictly_increasing():
    schedule = FrozenSwapSchedule()
    moments = [entry.moment for entry in schedule.entries]
    assert moments == sorted(moments)
    assert len(set(moments)) == 16


def test_schedule_starts_at_zero_and_wraps():
    schedule = FrozenSwapSchedule()
    assert schedule.entries[0].k == 0
    assert schedule.next_after(15) == 0
