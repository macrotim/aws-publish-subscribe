The purpose of this prototype was to solve this problem:

* Notify N web servers of an update.

I considered running a cron on each web server that checks a central location for updates.  But this is a polling solution and carries with it the downsides of a polling solution.

Next, I considered using a message queue, and naturally, being a lazy programmer, I began to explore AWS immediately.  I developed a working prototype that uses SNS (Simple Notification Service) to fanout messages to N SQS queues.  It worked!  Here is an example of the prototype.

Example: Publish the string "hello!" to three consumers.

$ export AWS_ACCESS_KEY=:your_access
$ export AWS_SECRET_KEY=:your_secret
$ cd src
$ python sns_reader.py inbound-tweets consumer1 &
$ python sns_reader.py inbound-tweets consumer2 &
$ python sns_reader.py inbound-tweets consumer3 &
$ python sns_writer.py inbound-tweets hello!

The last command publishes a message to SNS which fanouts out to three SQS queues, each bound to one of three consumers.  Because I configured long-polling in SQS.get_messages, each consumer receives and outputs the message in real-time!  Polling solution, you lose!
