from add_issue_number_to_conventional_commit import add_issue_number

INITIAL_COMMIT_MESSAGE = "chore: initial commit (PRE-10)"


def test_add_issue_number_in_simple_conventional_commit():
    new_content = add_issue_number("chore: initial commit", "PRE-10")

    assert new_content == INITIAL_COMMIT_MESSAGE


def test_add_issue_number_between_description_and_body():
    new_content = add_issue_number("chore: initial commit\n\nthis is a body", "PRE-10")

    assert new_content == "chore: initial commit (PRE-10)\n\nthis is a body"


def test_add_issue_number_in_first_line_if_commit_message_contains_git_defaults():
    new_content = add_issue_number("# Please enter the commit message\n\n", "PRE-10")

    assert new_content == "(PRE-10) # Please enter the commit message\n\n"


def test_add_issue_number_is_not_added_if_its_already_there():
    new_content = add_issue_number("chore: initial commit (PRE-10)", "PRE-10")

    assert new_content == INITIAL_COMMIT_MESSAGE


def test_append_issue_number_with_trimmed_trailing_whitespace():
    new_content = add_issue_number("chore: initial commit  ", "PRE-10")

    assert new_content == INITIAL_COMMIT_MESSAGE
