import argparse
import re
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath

    branch = get_current_branch_name()
    issue_number = find_issue_number_in_branch_name(branch)

    if issue_number:
        with open(commit_msg_filepath, "r+") as f:
            content = f.read()
            new_content = add_issue_number(content, issue_number)
            f.seek(0, 0)
            f.write(new_content)


def get_current_branch_name() -> str:
    try:
        branch_name = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"]
        )
        return branch_name.strip().decode("utf-8")
    except Exception as e:
        print(e)


def find_issue_number_in_branch_name(branch: str) -> str:
    if branch is None:
        return None
    matches = re.findall("[a-zA-Z0-9]{1,6}-\\d{1,5}", branch)
    if len(matches) > 0:
        return matches[0].upper()


def add_issue_number(commit_message: str, issue_number: str) -> str:
    if issue_number and issue_number in commit_message:
        return commit_message.strip()

    if "# Please enter the commit message" in commit_message:
        return f"{issue_number} - {commit_message}"

    parts = commit_message.split("\n\n", 1)
    title = parts[0].strip()
    commit_type, description = tuple(map(str.strip, title.split(":", maxsplit=1)))
    title = f"{commit_type}: {issue_number} - {description}"
    body = f"{parts[1]}" if len(parts) > 1 else None

    if body:
        return f"{title}\n\n{body}"
    else:
        return title


if __name__ == "__main__":
    SystemExit(main())
