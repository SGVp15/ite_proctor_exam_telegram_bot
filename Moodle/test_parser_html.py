from Moodle.parser_html import create_all_report


def test_create_all_report():
    create_all_report(is_only_new_report=False)
