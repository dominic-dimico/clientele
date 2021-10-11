import squirrel
import toolbelt
import configparser
import smartlog
import butterfly
format_ = format


# Clientele interpreter
class ClientInterpreter(squirrel.squish.SquishInterpreter):

    log = smartlog.Smartlog();

    def __init__(self):
        super().__init__();
        self.objects = ['client', 'set', 'session', 'exercise', 'food', 'ingredient', 'snack']
        self.initialize_squids();
        self.initialize_autocomplete();
        super().initialize_autocomplete();

    def initialize_autocomplete(self):
        """ Autocomplete and argspect initialization

            First do commands, objects, fields, then
            particular values of particular fields
        """ 
        # Fields of particular tables
        self.ts = {
          'client'     : ['user'],
          'exercise'   : ['name'],
        }


    def initialize_squids(self):
        cc = Clientele();        
        self.squids = cc.squids;


    def help(self):
        self.log.info("syntax: [command] ...\n");
        super().help();
        objects = [
          'client', 'exercise', 'set', 'session', 'snack', 'food', 'ingredient'
        ]
        self.log.outfile.write("\n");
        self.log.info("objects:");
        for obj in objects:
            self.log.info("  "+obj);
        self.log.outfile.write("\n");



class ClienteleSquid(squirrel.squid.Squid):
      def __init__(self):
          configs = {};
          configs = configparser.ConfigParser()
          configs.read(
              '/home/dominic/.config/clientele/clientele.cfg'
          )
          self.config = configs['main'];
          self.log = smartlog.Smartlog();
     


# more search options, such as 'like' 
class ClientSquid(ClienteleSquid):
  table = 'client';
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.format = {
        'fields'  : ['id', 'user', 'name', 'phone', 'email', 'skype', 'tags', 'note'],
        'list'    : { 
          'order'  : 'order by user',
        },
        'join'    : [
            {
              'type'       : 'many',
              'conditions' : [{
                  'table'     : 'session',
                  'type'      : 'where',
                  'condition' : 'session.clientid=%s and client.id=%s',
                  'variables' : ['id', 'id']
              },],
              'view' : {
                    'order'  : "order by session.time desc",
                    'number' : 10,
                    'fields' : [
                         'session.id', 
                         'session.time', 
                         'session.tags', 
                         'session.payment', 
                         'session.notes', 
                    ],
              },
            },
        ],
      };
      self.configure();

  def randomize_contact(self):  
      self.query('select * from client'); 
      for c in self.data:
          qd = toolbelt.quickdate.QuickDate();
          d = qd.random_date("a month ago", "now");
          c['contact'] = d;
          self.log.exself.log(self.update, c, {
            'self.log' : "Setting %s last contact to %s" % (c['user'], c['contact']),
            'ok'  : "Success!",
            'fail': "Something went wrong"
          },);

  def message(self, args):
      data = args['data'];
      for c in data:
          self.log.info("Hello %s" % (c["user"]));

  def postproc(self, args):
      return args;




class ExerciseSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.table = 'exercise'
      self.format = {
        'search' : {
           'defaults' : ['name',]
        },
        'new' : {
            'fields' : ['name'],
            'preset' : {
             },
        },
        'edit' : {
            'fields' : ['name'],
            'preset' : {
             },
        },
        'list' : {
            'fields' : ['name', 'muscle_groups'],
            'preset' : {
             },
        },
        'view' : {
            'fields' : ['name', 'muscle_groups'],
            'preset' : {
             },
        },
      };
      self.configure();


class ExerciseSetSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.table = 'exercise_set';
      self.aliases = ['set'];
      self.format = {
        'search' : {
           'defaults' : ['session.time', 'client.user', 'exercise_set.time'],
           'order'    : 'order by exercise_set.time desc',
        },
        'new' : {
            'fields' : ['resistance', 'reps', 'time', 'clientid', 'sessionid', 'exerciseid'],
            'preset' : {
             },
        },
        'edit' : {
            'fields' : ['resistance', 'reps', 'time'],
            'preset' : {
             },
        },
        'list' : {
            'fields' : ['resistance', 'reps', 'time', 'client.user', 'session.time', 'exercise.name'],
            'preset' : {
             },
        },
        'view' : {
            'fields' : ['resistance', 'reps', 'time', 'client.user', 'session.time', 'exercise.name'],
            'preset' : {
             },
        },
        'join' : [
            {
              'type'       : 'one',
              'foreignkey' : 'clientid',
              'table'      : 'client',
              'primarykey' : 'id',
              'pseudonym'  : 'client',
              'fields'     : ['user', 'name']
            },
            {
              'type'       : 'one',
              'foreignkey' : 'sessionid',
              'table'      : 'session',
              'primarykey' : 'id',
              'pseudonym'  : 'session',
              'fields'     : ['time']
            },
            {
              'type'       : 'one',
              'foreignkey' : 'exerciseid',
              'table'      : 'exercise',
              'primarykey' : 'id',
              'pseudonym'  : 'exercise',
              'fields'     : ['name']
            },
        ]
      };
      self.configure();



class SessionSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.table = 'session';
      self.format = {
        'search' : {
           'fields'   : ['session.id', 'client.user', 'session.time'],
           'order'    : 'order by session.time desc',
        },
        'new' : {
            'fields' : ['clientid', 'tags', 'payment', 'time', 'duration', 'notes'],
            'preset' : {
               'time'     : 'now',
               'duration' : '1 hour',
               'tags'     : 'workout;green',
               'payment'  : 0,
             },
             'postprocessor' : self.postproc,
        },
        'list' : {
            'fields' : ['session.id', 'client.user', 'tags', 'time', 'duration', 'payment', 'client.tags'],
            'preset' : {
             },
        },
        'edit' : {
            'fields' : ['id', 'time', 'duration', 'tags', 'payment', 'clientid', 'notes'],
            'preset' : {
             },
        },
        'view' : {
            'fields' : ['session.id', 'time', 'duration', 'tags', 'payment',  'client.user', 'client.name', 'client.id', 'session.notes'],
            'preset' : {
             },
        },
        'join' : [
            {
              'type'       : 'one',
              'foreignkey' : 'clientid',
              'table'      : 'client',
              'primarykey' : 'id',
              'pseudonym'  : 'client',
              'fields'     : ['id', 'user', 'name']
            },
            {
              'type'       : 'many',
              'conditions' : [{
                  'table'     : 'exercise_set',
                  'type'      : 'where',
                  'condition' : 'exercise_set.sessionid=%s',
                  'variables' : ['id']
                },{
                  'table'     : 'exercise',
                  'type'      : 'join',
                  'condition' : 'exercise_set.exerciseid=exercise.id',
              }],
              'new'  : {
                     'number'    : -1,
                     'condition' : 'tags like "%workout%"',
                     'table'     : 'exercise_set',
                     'fields'    : ['reps', 'resistance', 'exerciseid'],
                     'preset'    : {
                         'time'      : 'now',
                         'clientid'  : 'clientid',
                         'sessionid' : 'id',
                      },
              },
              'view' : {
                    'number' : 10,
                    'fields' : [
                         'session.id', 
                         'exercise.name', 
                         'exercise.id', 
                         'exercise_set.time', 
                         'exercise_set.reps', 
                         'exercise_set.resistance',
                    ],
                    'preset' : {
                    },
              },
            },
          ],
      };
      self.configure();



  def postproc(self, args):
      id = args['data']['clientid']
      s  = args['squids']['client'];
      client = s.singular(s.query(
            'select * from client where id=%s' % (id,)
      ));
      if   client['data']['nickname']: who = client['data']['nickname'];
      elif client['data']['name']:     who = client['data']['name'];
      elif client['data']['user']:     who = client['data']['user'];
      g = butterfly.gcalendar.GoogleCalendarAgent();
      g.insert_event(
        g.prepare_client_event({
         'who'      : who,
         'when'     : args['data']['time'],
         'duration' : args['data']['duration'],
         'service'  : args['data']['services'],
         'email'    : client['data']['email'],
         'phone'    : client['data']['phone'],
         'skype'    : client['data']['skype'],
        })
      );
      return args;





class IngredientSquid(ClienteleSquid):
  table = 'ingredient'
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.format = {
          'fields' : ['id', 'servingsize', 'recipeid', 'ingredientid'],
          'view'  : {'fields': ['id', 'servingsize', 'recipe.name', 'ing.name']},
          'list'  : {'fields': ['id', 'servingsize', 'recipe.name', 'ing.name']},
          'join' : [
            {
              'type'       : 'one',
              'foreignkey' : 'recipeid',
              'table'      : 'food',
              'alias'      : 'recipe',
              'primarykey' : 'id',
              'pseudonym'  : 'recipe',
              'fields'     : ['name']
            },
            {
              'type'       : 'one',
              'foreignkey' : 'ingredientid',
              'table'      : 'food',
              'alias'      : 'ing',
              'primarykey' : 'id',
              'pseudonym'  : 'ing',
              'fields'     : ['name']
            },
            ]
      };
      self.table = 'ingredient'
      self.configure();



class FoodSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.table = 'food'
      self.format = {
        'fields' : ['id', 'name', 'calories', 'fat', 'carbs', 'protein', 'servingsize'],
        'search' : {
            'fields' : ['name'],
        },
        'list' : {
             'preprocessor' : self.listpreproc,
        },
        'join' :
          [
            {
             'type'       : 'many',
             'conditions' : [
               {
                 'table'     : 'food',
                 'alias'     : 'f',
               },
               {
                 'table'     : 'ingredient',
                 'type'      : 'where',
                 'condition' : 'ingredient.recipeid=%s and f.id=ingredient.ingredientid and food.id=f.id',
                 'variables' : ['id'],
               },],
             'new'       : {
                 'table'     : 'ingredient',
                 'fields'    : ['ingredientid', 'servingsize'],
                 'preset'    : {
                    'recipeid' : 'id',
                 },
             },
             'view' : {
                'fields' : [
                    'f.id', 
                    'f.name', 
                    'f.servingsize', 
                    'f.fat',
                    'f.carbs',
                    'f.protein',
                ],
             },
            },
          ],
      };
      self.configure();

  def listpreproc(self, args):
      save = self.data;
      s = args['squids']['ingredient'];
      for d in args['data']:
          sql =("select * from food inner join ingredient on"
              + " food.id=ingredient.ingredientid"
              + " where ingredient.recipeid=%d" % d['id']);
          s.query(sql)
          d['calories'] = 0;
          d['fat']      = 0;
          d['carbs']    = 0;
          d['protein']  = 0;
          if not s.data: continue;
          for i in s.data:
              d['calories'] +=  i['calories'];
              d['fat'     ] +=  i['fat'     ];
              d['carbs'   ] +=  i['carbs'   ];
              d['protein' ] +=  i['protein' ];
          self.update(d);
      self.data = save;
      return args;



class SnacklogSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      self.table = 'snacklog'
      self.aliases = ['snack'];
      self.format = {
        'fields' : {'id', 'date', 'clientid', 'foodid'},
        'search' : {
           'defaults': ['date', 'client.user'],
           'order'   : 'order by date desc',
        },
        'new' : { 'fields' : ['date', 'clientid'], },
        'edit' : { 'fields' : ['date', 'clientid'], },
        'view' : { 'fields' : ['id', 'date', 'client.user'], },
        'list' : { 'fields' : ['date', 'client.user'], },
        'join' : [
           {
              'type'       : 'one',
              'foreignkey' : 'clientid',
              'table'      : 'client',
              'primarykey' : 'id',
              'pseudonym'  : 'client',
              'fields'     : ['id', 'user', 'name']
           },
           {
             'type'       : 'many',
             'conditions' : [ {
                 'table'     : 'food',
               }, {
                 'table'     : 'snacklog_food',
                 'type'      : 'where',
                 'condition' : 'snacklog_food.foodid=food.id '          +
                               ' and snacklog_food.snacklogid=snacklog.id ' +
                               ' and snacklog_food.snacklogid=%s',
                 'variables' : ['id'],
               }, 
             ],
             'new'       : {
                 'table'     : 'snacklog_food',
                 'fields'    : ['foodid', 'servingsize'],
                 'preset'    : {
                    'snacklogid' : 'id',
                 },
             },
             'view' : {
                'fields' : [
                    'food.id', 
                    'food.name', 
                    'food.fat',
                    'food.carbs',
                    'food.protein',
                ],
             },
          }, 
        ],
      };
      self.configure();



class SnacklogFoodSquid(ClienteleSquid):
  def __init__(self):
      ClienteleSquid.__init__(self);
      table = 'snacklog_food'
      format = {
        'fields' : ['foodid', 'snacklogid'],
        'join'  : [
              {
                'type'       : 'one',
                'foreignkey' : 'foodid',
                'table'      : 'food',
                'primarykey' : 'id',
                'pseudonym'  : 'food',
                'fields'     : ['name']
              },
              {
                'type'       : 'one',
                'foreignkey' : 'snacklogid',
                'table'      : 'snacklog',
                'primarykey' : 'id',
                'pseudonym'  : 'snacklog',
                'fields'     : ['id']
              },
          ]
      }; 
      self.configure();


class Food(squirrel.squish.Squish, FoodSquid):
      def __init__(self):
          FoodSquid.__init__(self);
class Client(squirrel.squish.Squish, ClientSquid):
      def __init__(self):
          ClientSquid.__init__(self);
class ExerciseSet(squirrel.squish.Squish, ExerciseSetSquid):
      def __init__(self):
          ExerciseSetSquid.__init__(self);
class Snacklog(squirrel.squish.Squish, SnacklogSquid):
      def __init__(self):
          SnacklogSquid.__init__(self);
class Ingredient(squirrel.squish.Squish, IngredientSquid):
      def __init__(self):
          IngredientSquid.__init__(self);
class Session(squirrel.squish.Squish, SessionSquid):
      def __init__(self):
          SessionSquid.__init__(self);
class Exercise(squirrel.squish.Squish, ExerciseSquid):
      def __init__(self):
          ExerciseSquid.__init__(self);


class Clientele():

      def __init__(self):
          self.aliases = {
             'exercise_set' : 'set',
             'snacklog' : 'snack',
          }

          self.squids     = {}
          self.client     = Client()
          self.exercise   = Exercise()
          self.exset      = ExerciseSet()
          self.session    = Session()
          self.food       = Food()
          self.ingredient = Ingredient()
          self.snacklog   = Snacklog()

          self.squids['client']              = self.client
          self.squids['exercise']            = self.exercise
          self.squids['set']                 = self.exset
          self.squids['session']             = self.session
          self.squids['food']                = self.food
          self.squids['ingredient']          = self.ingredient
          self.squids['snack']            = self.snacklog
          for squid in self.squids:
              self.squids[squid].db = self;
