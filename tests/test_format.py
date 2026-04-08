"""Tests for humanint.format."""

import pytest

from humanint import HumanIntError, format


class TestFormatHappyPath:
    def test_format_zero_returns_zero_string(self) -> None:
        assert format(0) == "0"

    def test_format_small_number_returns_plain_string(self) -> None:
        assert format(42) == "42"

    def test_format_thousand_returns_k_suffix(self) -> None:
        assert format(1500) == "1.5K"

    def test_format_million_returns_m_suffix(self) -> None:
        assert format(2_000_000) == "2.0M"

    def test_format_billion_returns_b_suffix(self) -> None:
        assert format(3_200_000_000) == "3.2B"

    def test_format_trillion_returns_t_suffix(self) -> None:
        assert format(1_000_000_000_000) == "1.0T"

    def test_format_negative_returns_signed_string(self) -> None:
        assert format(-1500) == "-1.5K"

    def test_format_with_precision_zero_truncates_decimals(self) -> None:
        assert format(1500, precision=0) == "2K"

    def test_format_with_precision_three_keeps_three_decimals(self) -> None:
        assert format(1234, precision=3) == "1.234K"


class TestFormatEdgeCases:
    def test_format_non_int_raises(self) -> None:
        with pytest.raises(HumanIntError, match="expected int"):
            format("100")  # type: ignore[arg-type]

    def test_format_bool_raises(self) -> None:
        with pytest.raises(HumanIntError, match="expected int"):
            format(True)  # type: ignore[arg-type]

    def test_format_negative_precision_raises(self) -> None:
        with pytest.raises(HumanIntError, match="non-negative"):
            format(1000, precision=-1)

    def test_format_non_int_precision_raises(self) -> None:
        with pytest.raises(HumanIntError, match="non-negative"):
            format(1000, precision=1.5)  # type: ignore[arg-type]


class TestRoundTrip:
    @pytest.mark.parametrize("value", [0, 1, 999, 1000, 1_500, 1_000_000, -2_500_000])
    def test_format_then_parse_round_trips_for_clean_values(self, value: int) -> None:
        assert parse_safely(format(value, precision=3)) == value


def parse_safely(text: str) -> int:
    from humanint import parse

    return parse(text)
