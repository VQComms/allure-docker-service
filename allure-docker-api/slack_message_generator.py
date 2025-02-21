from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

def generate_slack_message(project_name, report_url, project_generation_timestamp, total_test_count, total_pass_count,
                           total_fail_count, overall_pass_rate, total_test_run_period, watchers_list):
    return {
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"Test report generated for project *{project_name}*\n"
                        f"📄 *Report URL:* <{report_url}|View Report>\n"
                        f"🕒 *Generated at:* {project_generation_timestamp}\n"
                        f"📊 *Total number of tests:* {total_test_count}\n"
                        f"✅ *Total Passed:* {total_pass_count}\n"
                        f"❌ *Total Failed:* {total_fail_count}\n"
                        f"📈 *Pass rate overall:* {overall_pass_rate:.2f}%\n"
                        f"⏳ *Time taken for test run:* {total_test_run_period}\n"
                        f"👥 *FAO:* {watchers_list}\n"
                    )
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "See Report",
                            "emoji": True
                        },
                        "url": report_url,  # Makes the button clickable to the report URL
                        "action_id": "see_report"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Add me to Watchers",
                            "emoji": True
                        },
                        "action_id": "add_watcher"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Remove me from Watchers",
                            "emoji": True
                        },
                        "action_id": "remove_watcher"
                    }
                ]
            }
        ]
    }

def send_summary_to_slack_app(report_url, slack_channel_id, bearer_token, logger):
    try:
        project_name = report_url.rsplit('/', 1)[-1]
        pass_count = 2
        fail_count = 1
        total_test_count = pass_count + fail_count
        pass_rate = (float(pass_count) / total_test_count)
        watchers_list = []
        
        slack_message = generate_slack_message(project_name, report_url, "some time ago", total_test_count, pass_count,
                                               fail_count, pass_rate, "ages", watchers_list)
        
        client = WebClient(token=bearer_token)

        response = client.chat_postMessage(
            channel=slack_channel_id,
            blocks=slack_message["blocks"]
        )

        logger.info(response)
    
    except SlackApiError as e:
        logger.info(f"Error sending sumamry to slack app: {e}")

    return