"""Tests for humanint.parse."""

import pytest

from humanint import HumanIntError, parse


class TestParseHappyPath:
    def test_parse_plain_integer_returns_int(self) -> None:
        assert parse("1500") == 1500

    def test_parse_with_k_suffix_returns_thousands(self) -> None:
        assert parse("1.5k") == 1500

    def test_parse_with_uppercase_k_returns_same_value(self) -> None:
        assert parse("1.5K") == 1500

    def test_parse_with_m_suffix_returns_millions(self) -> None:
        assert parse("2M") == 2_000_000

    def test_parse_with_b_suffix_returns_billions(self) -> None:
        assert parse("3.2B") == 3_200_000_000

    def test_parse_with_t_suffix_returns_trillions(self) -> None:
        assert parse("1T") == 1_000_000_000_000

    def test_parse_negative_with_suffix_returns_negative_int(self) -> None:
        assert parse("-1.5k") == -1500

    def test_parse_with_commas_strips_them(self) -> None:
        assert parse("1,000,000") == 1_000_000

    def test_parse_with_underscores_strips_them(self) -> None:
        assert parse("1_500") == 1500

    def test_parse_with_surrounding_whitespace_strips_it(self) -> None:
        assert parse("  2M  ") == 2_000_000

    def test_parse_zero_returns_zero(self) -> None:
        assert parse("0") == 0

    def test_parse_zero_with_suffix_returns_zero(self) -> None:
        assert parse("0k") == 0


class TestParseEdgeCases:
    def test_parse_empty_string_raises(self) -> None:
        with pytest.raises(HumanIntError, match="empty"):
            parse("")

    def test_parse_whitespace_only_raises(self) -> None:
        with pytest.raises(HumanIntError, match="empty"):
            parse("   ")

    def test_parse_unknown_suffix_raises(self) -> None:
        with pytest.raises(HumanIntError, match="unknown suffix"):
            parse("5x")

    def test_parse_garbage_input_raises(self) -> None:
        with pytest.raises(HumanIntError, match="invalid numeric part"):
            parse("notanumber9")

    def test_parse_only_suffix_raises(self) -> None:
        with pytest.raises(HumanIntError, match="missing numeric part"):
            parse("k")

    def test_parse_non_string_raises(self) -> None:
        with pytest.raises(HumanIntError, match="expected str"):
            parse(123)  # type: ignore[arg-type]

    def test_parse_inexact_value_raises(self) -> None:
        # 1.2345k = 1234.5 -> not an exact integer.
        with pytest.raises(HumanIntError, match="not an exact integer"):
            parse("1.2345k")
