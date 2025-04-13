import subprocess

import pytest

from add_issue_number_to_conventional_commit import (
    find_issue_number_in_branch_name,
    get_current_branch_name,
)


def test_get_current_branch_name_success(mocker):
    mocker.patch("subprocess.check_output", return_value=b"feature/TEST-123\n")
    branch_name = get_current_branch_name()
    assert branch_name == "feature/TEST-123"


def test_get_current_branch_name_failure(mocker):
    mocker.patch(
        "subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, "git symbolic-ref --short HEAD"),
    )
    branch_name = get_current_branch_name()
    assert branch_name is None


def test_get_current_branch_name_empty_output(mocker):
    mocker.patch("subprocess.check_output", return_value=b"")
    branch_name = get_current_branch_name()
    assert branch_name == ""


@pytest.mark.parametrize(
    "issue_number,expected_issue_number",
    [
        ("pre-10", "PRE-10"),
        ("abcde-1234", "ABCDE-1234"),
        ("A2B5G-123", "A2B5G-123"),
        ("a0b1c-1", "A0B1C-1"),
    ],
)
@pytest.mark.parametrize("description_separator", ["-", ":"])
def test_find_issue_number_in_branch_name(
    issue_number: str,
    expected_issue_number: str,
    description_separator: str,
) -> None:
    parsed_number = find_issue_number_in_branch_name(
        f"feat/{issue_number}{description_separator}new-feature"
    )

    assert parsed_number == expected_issue_number


@pytest.mark.parametrize(
    "issue_number,expected_issue_number",
    [
        ("pre-10", "PRE-10"),
        ("abcde-1234", "ABCDE-1234"),
        ("A2B5G-123", "A2B5G-123"),
        ("a0b1c-1", "A0B1C-1"),
    ],
)
@pytest.mark.parametrize("description_separator", ["-", ":"])
def test_find_issue_number_in_branch_name_without_commit_type(
    issue_number: str,
    expected_issue_number: str,
    description_separator: str,
) -> None:
    parsed_number = find_issue_number_in_branch_name(
        f"{issue_number}{description_separator}new-feature"
    )

    assert parsed_number == expected_issue_number


@pytest.mark.parametrize("invalid_issue_number", ["unknown", "", "A-"])
@pytest.mark.parametrize("description_separator", ["-", ":"])
def test_return_none_if_no_issue_number_in_branch_name(
    invalid_issue_number: str,
    description_separator: str,
) -> None:
    branch_name = f"feat/{invalid_issue_number}{description_separator}new-feature"
    assert find_issue_number_in_branch_name(branch_name) is None


def test_return_none_if_branch_is_none() -> None:
    assert find_issue_number_in_branch_name(None) is None
