import squirrel
import toolbelt
import configparser
import smartlog


log = smartlog.Smartlog();



class ClientInterpreter(squirrel.squish.SquishInterpreter):


    def __init__(self):
        self.initialize_configs();
        self.initialize_squids();
        super().__init__();

    def initialize_configs(self):
        configs = {};
        configs['clientele'] = configparser.ConfigParser()
        configs['clientele'].read('/home/dominic/src/clientele/clientele.cfg')
        self.configs = configs;

    def initialize_squids(self):
        squids= {}
        squids['client'] = Client(self.configs['clientele'], 'client')
        squids['exercise'] = Exercise(self.configs['clientele'], 'exercise')
        squids['exercise_set'] = ExerciseSet(self.configs['clientele'], 'exercise_set')
        squids['session'] = Session(self.configs['clientele'], 'session')
        squids['message'] = Message(self.configs['clientele'], 'message')
        self.squids = squids;


    def add_commands(self):
        self.commands['schedule'] = { 
            'func' : self.schedule,
            'args' : [ 'client', 'service', 'time' ] 
        }


    # use butterfly
    def schedule(self):
        pass



class Client(squirrel.squid.Squid):

  list_formatting = ['user', 'name', 'phone', 'email', 'skype', 'contact'];
  view_formatting = [];
  join_formatting = [];

  def __init__(self, config, table):
    super().__init__(config, table);

  def randomize_contact(self):  
      self.query('select * from client'); 
      for c in self.data:
          random_date = toolbelt.dates.randdate("a month ago", "now");
          c['contact'] = random_date;
          log.exlog(self.update, c, {
            'log' : "Setting %s last contact to %s" % (c['user'], c['contact']),
            'ok'  : "Success!",
            'fail': "Something went wrong"
          });

  def message(self, args):
      data = args['data'];
      for c in data:
          log.info("Hello %s" % (c["user"]));

  def poll_contact(self):
      polldatum = {
          'interval' : "5 seconds",
          'start'    : "four weeks ago",
          'end'      : "three weeks ago",
          'field'    : "contact",
          'handler'  : self.message,
          'args'     : { }
      }
      self.poll( polldatum );

  # butterfly
  def sendmail(self, args):
      pass



class Exercise(squirrel.squid.Squid):

  list_formatting = [];
  view_formatting = [];
  join_formatting = [];

  def __init__(self, config, table):
    super().__init__(config, table);



class ExerciseSet(squirrel.squid.Squid):

  list_formatting = ['resistance', 'reps'];
  view_formatting = [];
  join_formatting = [
    {
      'foreignkey' : 'clientid',
      'table'      : 'client',
      'primarykey' : 'id',
      'fields'     : ['user', 'name']
    },
    {
      'foreignkey' : 'sessionid',
      'table'      : 'session',
      'primarykey' : 'id',
      'fields'     : ['time']
    },
    {
      'foreignkey' : 'exerciseid',
      'table'      : 'exercise',
      'primarykey' : 'id',
      'fields'     : ['name']
    }
  ];

  def __init__(self, config, table):
    super().__init__(config, table);



class Session(squirrel.squid.Squid):

  list_formatting = [];
  view_formatting = [];
  join_formatting = [
    {
      'foreignkey' : 'clientid',
      'table'      : 'client',
      'primarykey' : 'id',
      'fields'     : ['user', 'name']
    }
  ];

  def __init__(self, config, table):
      super().__init__(config, table);

  def editnote(self): 
      toolbelt.editors.vim


class Message(squirrel.squid.Squid):
  list_formatting = [];
  view_formatting = [];
  join_formatting = [];
  def __init__(self, config, table):
    super().__init__(config, table);

