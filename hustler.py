#import butterfly
from squirrel import squid
import configparser
import time
import toolbelt
import pprint
import smartlog
import signal
import sys
import code

# ToDo: 
#   * analyze this code in more detail
#   * make message tags work with client tags
#   * more messages in database

POLL_START = "one hour ago"
POLL_END   = "one hour"

pprint = pprint.pprint

config = configparser.ConfigParser();
config.read('clientele.cfg');

global client 
global message
global delivery
 
clientdb   = squid.Squid(config, 'client')
messagedb  = squid.Squid(config, 'message')
deliverydb = squid.Squid(config, 'delivery')

global voice;
#voice = butterfly.comms.text_login();

out = smartlog.Smartlog();


# Same message should not have been sent more than a year ago?
def messages(client):

    client_id = client['id'];
    tokens = toolbelt.converters.tokenize_var_tags(client['tags']);
    pprint(tokens);

    # Obtain messages which are inviable due to last delivery date
    sql = "select * from delivery order by timestamp desc";
    deliverydb.query(sql);
    inviable = [];
    for i in range(0, 2):
       if len(deliverydb.data) > i:
          inviable.append(deliverydb.data[i]['message_id']);


    # Obtain messages which are inviable due to having been sent to the
    # client already
    sql = "select * from delivery where client_id=%s order by timestamp desc" % (client_id);
    deliverydb.query(sql);
    if deliverydb.data:
       for i in range(0, 3):
           if len(deliverydb.data) > i:
              if deliverydb.data[i]['message_id'] not in inviable:       
                 inviable.append(deliverydb.data[i]['message_id']);

    # Obtain messages which are viable
    sql = "select * from message";
    viable = [];
    messagedb.query(sql);
    if messagedb.data:
       for message in messagedb.data:
           if message['id'] not in inviable:       
              viable.append(message);

    if len(viable) < 1:
       return None;

    # Ideally, sort by specificity, then select most specific message
    index = toolbelt.randoms.random_index(len(viable));
    message = viable[index];
    #pprint(message);
    body = message['body'];
    body = toolbelt.converters.replace_vars(body, tokens);
    message['body'] = body;
    return message



def alert(clients):

    client_index = 0;

    for client in clients:
        message = messages(client);
        if message:
           if client['phone']:
             out.logok(client['phone'] + ' -> ' + message['body'])
             #butterfly.text(client['phone'], message['body'], voice);
           else: out.warn("No phone number for {}".format(client['name']));
           delivery = {
             'client_id': client['id'],
             'message_id': message['id'],
             'timestamp': str(toolbelt.converters.date('now'))
           };
           deliverydb.insert(delivery);
           contact = toolbelt.converters.date(client['freq']);
           client['contact'] = contact;
           clientdb.update(client);
           break
        # Not having a message is a problem!
        else: print "No message for %s!" % (client['phone'])
        client_index = client_index + 1;

    # Update contact for other clients, catch them next time
    for index in range(client_index+1, len(clients)):
        clients[index]['contact'] = str(toolbelt.converters.date(POLL_END));
        clientdb.update(clients[index]);



data = [
  (6, 'contact', POLL_START, POLL_END, alert)
]


threads = clientdb.polls(data);



#############################################################################
# Misc stuff
#############################################################################

class ThreadExit(Exception):
      pass

def stop_threads(signum, frame):
    print('Caught signal %d' % signum)
    raise ThreadExit

signal.signal(signal.SIGTERM, stop_threads);
signal.signal(signal.SIGINT, stop_threads);

while True:
      try: time.sleep(10);
      except ThreadExit:
             sys.exit(0);
             #for thread in threads:
             #    thread.shutdown_flag.set();
             #for thread in threads:
             #    thread.join();
             #break;
        
