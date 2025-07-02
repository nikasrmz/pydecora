import pytest
from unittest.mock import Mock, patch 
from pydeco.decorators.retry import retry


def test_succeed_first_try() -> None:
    mock_func = Mock(return_value="ok")

    @retry(times=3)
    def wrapped() -> str:
        return mock_func()
    
    result = wrapped()
    assert result == "ok"
    assert mock_func.call_count == 1


def test_succeed_third_try() -> None:
    mock_func = Mock(side_effect=[Exception(), Exception(), "ok"])

    @retry(times=3)
    def wrapped() -> str:
        return mock_func()
    
    result = wrapped()
    assert result == "ok"
    assert mock_func.call_count == 3


def test_all_attempts_fail() -> None:
    mock_func = Mock(side_effect=Exception("fail"))

    @retry(times=3)
    def wrapped() -> None:
        return mock_func()
    
    with pytest.raises(Exception, match="fail"):
        wrapped()

    assert mock_func.call_count == 3


def test_custom_exception_filtering() -> None:
    mock_func = Mock(side_effect=[ValueError(), KeyError(), Exception("fail")])

    @retry(times=3, exceptions=(ValueError, KeyError))
    def wrapped() -> None:
        return mock_func()
    
    with pytest.raises(Exception, match="fail"):
        wrapped()

    assert mock_func.call_count == 3


@patch("time.sleep")
def test_delay_and_backoff(mock_sleep) -> None:
    mock_func = Mock(side_effect=[Exception(), Exception(), "ok"])

    @retry(times=3, delay=1, backoff_multiplier=2)
    def wrapped() -> str:
        return mock_func()
    
    result = wrapped()

    assert result == "ok"
    assert mock_func.call_count == 3
    assert mock_sleep.call_args_list == [((1,),), ((2,),)]

test_delay_and_backoff()