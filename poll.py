import squirrel
import butterfly
import configparser
import time
import toolbelt


config = configparser.ConfigParser();
config.read('clientele.cfg');

global client 
global message
global delivery
clientdb = squirrel.Squid(config, 'client')
messagedb = squirrel.Squid(config, 'message')
deliverydb = squirrel.Squid(config, 'delivery')



# Same message should not have been sent more than a year ago?
def messages(client):
    client_id = client['id'];
    sql = "select * from message left outer join delivery on "        \
        + "message.id = delivery.message_id where "                   \
        + "(delivery.client_id<>'%s' or delivery.client_id is null)" % (
            client_id
    )
    messagedb.query(sql);
    if messagedb.data:
       for message in messagedb.data:
           print client['phone'], message['body'].rstrip('\n');
       return messagedb.data[1];
    return None




def alert(clients):
    contact = toolbelt.converters.date("thirty seconds from now");
    for client in clients:
        message = messages(client);
        if message:
           #butterfly.text(client['phone'], message['body']);
           delivery = {
             'client_id': client['id'],
             'message_id': message['id'],
             'timestamp': str(toolbelt.converters.date('now'));
           };
           #deliverydb.insert(delivery);
        client['contact'] = contact;
        #clientdb.update(client);


data = [(10, 'contact', 'thirty minutes ago', 'now', alert)] 
threads = clientdb.polls(data);


while True:
      time.sleep(10);


