"""Subscribe to an SNS Topic and write messages to stdout.

Usage: python sns_reader.py inbound-tweets consumer1

"""

import json
import myboto
import sys

def listen(topic_name, listener_name, visibility_timeout=10):
  """Yields new messages published to the specific Topic.

  Creates an SQS queue by the specified listener_name and subscribes it to
  the SNS Topic.

  Take note that you've got at most `visibility_timeout` seconds to handle
  the message before SQS unlocks the message for other readers.

  """
  # Create an SQS if not exists and subscribe it to the Topic.
  qname = listener_name
  sqs_queue = myboto.sns.setup_subscribed_sqs_queue(topic_name, qname)

  # Listen to inbound messages.
  while True:
    sqs_messages = sqs_queue.get_messages(
      visibility_timeout=visibility_timeout,
      wait_time_seconds=20)

    for m in sqs_messages:
      # Note: Messages published through SNS are wrapped in a json structure.
      sns_str = m.get_body()
      sns_dict = json.loads(sns_str)

      yield sns_dict['Message']
      sqs_queue.delete_message(m)

if __name__ == '__main__':
  topic_name = sys.argv[1]
  listener_name = sys.argv[2]
  for message in listen(topic_name, listener_name):
    print listener_name, '>>', message
