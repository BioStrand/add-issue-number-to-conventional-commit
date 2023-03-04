import pytest as pytest

from add_issue_number_to_conventional_commit import find_issue_number_in_branch_name


@pytest.mark.parametrize(
    "issue_number,expected_issue_number",
    [
        ("pre-10", "PRE-10"),
        ("abcde-1234", "ABCDE-1234"),
        ("A2B5G-123", "A2B5G-123"),
        ("a0b1c-1", "A0B1C-1"),
    ],
)
def test_find_issue_number_in_branch_name(issue_number, expected_issue_number):
    parsed_number = find_issue_number_in_branch_name(f"feat/{issue_number}-new-feature")

    assert parsed_number == expected_issue_number


@pytest.mark.parametrize("invalid_issue_number", ["unknown", "", "A-"])
def test_return_none_if_no_issue_number_in_branch_name(invalid_issue_number):
    branch_name = f"feat/{invalid_issue_number}-new-feature"
    assert find_issue_number_in_branch_name(branch_name) is None


def test_return_none_if_branch_is_none():
    assert find_issue_number_in_branch_name(None) is None
