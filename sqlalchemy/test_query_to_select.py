import re
import pytest

from query_to_select import QueryToSelect


@pytest.mark.parametrize(
    "input_line, expected_line",
    [
        (
            "res = session.query(User).all()\n",
            "res = session.scalars(select(User)).all()\n",
        ),
        (
            "session.query(User).filter_by(name='some user').one()\n",
            "session.execute(select(User).filter_by(name='some user')).scalar_one()\n",
        ),
        (
            "session.query(User).count()\n",
            "session.scalars(select(func.count()).select_from(select(User))).one()\n",
        ),
        (
            "session.query(User).filter_by(name='some user').first()\n",
            "session.scalars(select(User).filter_by(name='some user').limit(1)).first()\n",
        ),
        ("line without query\n", "line without query\n"),
        ("some other line\n", "some other line\n"),
    ],
)
def test_process_line(input_line, expected_line):
    obj = QueryToSelect()
    p = re.compile(obj.pattern)
    result = obj.process_one_line(input_line, p)

    assert result == expected_line
