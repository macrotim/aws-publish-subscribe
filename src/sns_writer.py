"""Publish a message to an SNS Topic.

Usage: python sns_writer.py inbound-tweets hello!

"""

import myboto
import sys

if __name__ == '__main__':
  topic_name = sys.argv[1]
  message = sys.argv[2]
  topic_arn = myboto.sns.create_topic(topic_name)
  myboto.sns.publish(topic_arn, message)
