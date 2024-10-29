import os
from slack_webhook import Slack

ops = Slack(url=os.environ.get("OPS_WEBHOOK"))
noise = Slack(url=os.environ.get("NOISE_WEBHOOK"))


def post_to_ops(text):
    if os.environ.get("ENV") == "PROD":
        try:
            ops.post(text=text)
        except:
            pass
    print(f"[OPS:] {text}")

def post_to_noise(text):
    if os.environ.get("ENV") == "PROD":
        try:
            noise.post(text=text)
        except:
            pass
    print(f"[NOISE:] {text}")
