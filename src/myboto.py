"""A collection of convenience methods for accessing AWS.

"""
import boto.sns
import boto.sns
import boto.sqs.connection
from boto.sqs.message import RawMessage
import os

ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

assert ACCESS_KEY, 'Requires environment variable AWS_ACCESS_KEY'
assert SECRET_KEY, 'Requires environment variable AWS_SECRET_KEY'

_sqs = None
_sns = None

def SQSConnection():
  """Returns an SQSConnection.

  This is a convenience function that encapsulates the AWS keys.

  """
  global _sqs
  if _sqs is None:
    _sqs = boto.sqs.connection.SQSConnection(ACCESS_KEY, SECRET_KEY)
  return _sqs

def SNSConnection():
  """Returns an SNSConnection.

  This is a convenience function that encapsulates the AWS keys.

  """
  global _sns
  if _sns is None:
    _sns = boto.sns.SNSConnection(ACCESS_KEY, SECRET_KEY)
  return _sns

class SNS(object):
  """SNS is a higher level construct than SNSConnection.

  To improve readability of client code, it is based on the Topic object instead
  of the Topic-ARN string.

  """

  def publish(self, topic, message):
    """Publishes the message to the specified Topic."""
    return SNSConnection().publish(topic.arn, message)

  def setup_subscribed_sqs_queue(self, topic_name, sqs_qname):
    """Return SQS queue.

    This is a convenience function that creates an SQS queue and subscribes
    it to the specified Topic.

    """
    topic = self.create_topic(topic_name)

    # Create an SQS and subscribe it to the Topic.
    sqs_queue = SQSConnection().create_queue(sqs_qname)
    SNSConnection().subscribe_sqs_queue(topic.arn, sqs_queue)

    # SQS queues that are subscribed to SNS require a special configuration.
    sqs_queue.set_message_class(RawMessage)

    print 'Subscribed queue to SNS topic'
    print '  queue: ', sqs_qname
    print '  topic: ', topic.name
    print '  topic arn: ', topic.arn

    return sqs_queue

  def create_topic(self, topic_name):
    """Return the Topic.

    create_topic is a convenience function connects to SNS that encapsulates
    some of the dirty work involved with creating a topic.

    Examples:
      topic name = 'inbound-tweet'
      topic ARN  = 'arn:aws:sns:us-east-1:070761879279:inbound-tweet'

    """
    # Create the Topic.
    topic_response_dict = SNSConnection().create_topic(topic_name)

    # Parse the SNS response for the Topic ARN.
    topic_arn = topic_response_dict \
      ['CreateTopicResponse'] \
      ['CreateTopicResult'] \
      ['TopicArn']

    return Topic(name=topic_name, arn=topic_arn)

class Topic(object):
  """Topic is an object-oriented representation of an SNS Topic.  The
  boto.SNSConnection module passes simple strings which I find more difficult
  for a reader.

  """
  def __init__(self, name, arn):
    self.name = name
    self.arn = arn

sns = SNS()
