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


def get_current_branch_name():
    try:
        branch_name = subprocess.check_output(
            ["git", "symbolic-ref", "--short", "HEAD"]
        )
        return branch_name.strip().decode("utf-8")
    except Exception as e:
        print(e)


def find_issue_number_in_branch_name(branch):
    if branch is None:
        return None
    matches = re.findall("[a-zA-Z0-9]{1,10}-\\d{1,5}", branch)
    if len(matches) > 0:
        return matches[0].upper()


def add_issue_number(commit_message, issue_number):
    if issue_number and issue_number in commit_message:
        return commit_message

    parts = commit_message.split("\n\n", 1)
    title = parts[0].strip()
    body = f"{parts[1]}" if len(parts) > 1 else None

    if body:
        return f"{title} ({issue_number})\n\n{body}"
    else:
        return f"{title} ({issue_number})"


if __name__ == "__main__":
    SystemExit(main())
