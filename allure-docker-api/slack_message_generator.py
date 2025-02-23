from dataclasses import fields
from re import search
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import datetime

#todo: add standard text representation for good practice - see docker api container logs at point of sending request
def generate_slack_message(project_name, report_url, project_generation_timestamp, total_test_count, total_pass_count,
                           total_fail_count, total_skipped_count, overall_pass_rate, total_test_run_period, watchers_list):
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
                        f"📄 *Report URL:* {report_url}\n"
                        f"🕒 *Generated at:* {project_generation_timestamp}\n"
                        f"📊 *Total number of tests:* {total_test_count}\n"
                        f"✅ *Total Passed:* {total_pass_count}\n"
                        f"❌ *Total Failed:* {total_fail_count}\n"
                        f"💨 *Total Skipped:* {total_skipped_count}\n"
                        f"📈 *Pass rate overall:* {overall_pass_rate:.2f}%\n"
    #todo:                   f"⏳ *Time taken for test run:* {total_test_run_period}\n"
    #todo:                   f"👥 *FAO:* {watchers_list}\n"
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
                    }
                    #todo: {
                    #     "type": "button",
                    #     "text": {
                    #         "type": "plain_text",
                    #         "text": "Add me to Watchers",
                    #         "emoji": True
                    #     },
                    #     "action_id": "add_watcher"
                    # },
                    # {
                    #     "type": "button",
                    #     "text": {
                    #         "type": "plain_text",
                    #         "text": "Remove me from Watchers",
                    #         "emoji": True
                    #     },
                    #     "action_id": "remove_watcher"
                    # }
                ]
            }
        ]
    }

def send_summary_to_slack_app(report_url, slack_channel_id, bearer_token, logger, passed_count, failed_count,
                              skipped_count, total_count):
    try:
        project_name = search(r'/projects/([^/]+)/reports/', report_url).group(1)
        
        if int(total_count) == 0:
            pass_rate = 0
        else:
            pass_rate = (float(passed_count) / float(total_count)) * 100

        watchers_list = []
        project_generation_timestamp = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        
        #todo: add skip_count
        slack_message = generate_slack_message(project_name, report_url, project_generation_timestamp, total_count, passed_count,
                                               failed_count, skipped_count, pass_rate, "ages", watchers_list)
        
        client = WebClient(token=bearer_token)

        response = client.chat_postMessage(
            channel=slack_channel_id,
            blocks=slack_message["blocks"]
        )

        logger.info(response)
        
        #todo: tidy up 
        report_summary_fields = {
            "Test Project": f"{project_name}",
            "Url": f"{report_url}",
            "Generated at": f"{project_generation_timestamp}",
            "Total": f"{total_count}",
            "Passed": f"{passed_count}",
            "Failed": f"{failed_count}",
            "Skipped": f"{skipped_count}",
            "Pass Rate": f"{pass_rate:2f}%",
        }

        logger.info("summary json: " + str(report_summary_fields))
    

        #todo - improvement: send to new canvas if new project - populate existing one if not  
        client.api_call(
            api_method="canvas.listItems.add",
            json={
                "list": "T03C23TQH", #list id for slack channel with test summaries todo: make env var
                "title": f"{report_url}", #todo: assign title and desc dynamically based on report passed 
                "description": f"description for report {project_name}",
                "fields": report_summary_fields
            }
        )
    
    except SlackApiError as e:
        logger.info(f"Slack API error: {e}")

    return