import squirrel
import toolbelt
import configparser
import smartlog
import butterfly


class Client(squirrel.squid.Squid):
  form = {
    'search' : {
      'defaults' : ['user', 'phone', 'email', 'name'],
    },
    'new' : {
        'fields' : ['user',  'name',  'phone', 'email', 'skype', 'tags', 'note'],
    },
    'edit' : {
        'fields' : ['user',  'name',  'phone', 'email', 'skype', 'tags', 'note'],
    },
    'list' : {
        'fields' : ['id', 'user', 'name', 'phone', 'freq', 'email', 'tags', 'skype', 'contact'],
    },
    'view' : {
        'fields' : ['id', 'user', 'name', 'phone', 'freq', 'email', 'tags', 'skype', 'contact', 'note'],
    },
    'join'  : [
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
                     'session.services', 
                     'session.payment', 
                ],
                'preset' : {
                },
          },
        },
    ],
  };

  def __init__(self, config, table="client"):
    super().__init__(config, table);

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





class Exercise(squirrel.squid.Squid):
  form = {
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
  def __init__(self, config, table):
    super().__init__(config, table);



class ExerciseSet(squirrel.squid.Squid):
  form = {
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
  def __init__(self, config, table):
    super().__init__(config, table);



class Session(squirrel.squid.Squid):

  def __init__(self, config, table):
      super().__init__(config, table);
      self.form = {
        'search' : {
           'defaults' : ['client.user', 'session.time'],
           'order'    : 'order by session.time desc',
        },
        'new' : {
            'fields' : [      'time', 'duration', 'services', 'payment',     'clientid'],
            'preset' : {
             },
             'postprocessor' : self.postproc,
        },
        'list' : {
            'fields' : ['session.id', 'time', 'duration', 'payment',  'client.user', 'client.name'],
            'preset' : {
             },
        },
        'edit' : {
            'fields' : [      'time', 'duration', 'services', 'payment',     'clientid'],
            'preset' : {
             },
        },
        'view' : {
            'fields' : ['session.id', 'time', 'duration', 'payment',  'client.user', 'client.name', 'client.id', 'session.notes'],
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
                     'table'  : 'exercise_set',
                     'gather' : ['reps', 'resistance', 'exerciseid'],
                     'preset' : {
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





class Ingredient(squirrel.squid.Squid):
  form = {
    'search' : {
        'defaults' : ['name'],
    },
    'new' : {
        'fields' : ['name', 'servingsize', 'calories', 'fat', 'carbs', 'protein'],
        'preset' : {
         },
    },
    'view' : {
        'fields' : ['name', 'servingsize', 'calories', 'fat', 'carbs', 'protein'],
        'preset' : {
         },
    },
    'list' : {
        'fields' : ['name', 'servingsize', 'calories', 'fat', 'carbs', 'protein'],
        'preset' : {
         },
    },
    'edit' : {
        'fields' : ['name', 'servingsize', 'calories', 'fat', 'carbs', 'protein'],
        'preset' : {
         },
    },
  };
  def __init__(self, config, table):
      super().__init__(config, table);



class Recipe(squirrel.squid.Squid):

  def __init__(self, config, table):
      super().__init__(config, table);
      self.form = {
        'search' : {
            'defaults' : ['name'],
        },
        'new' : {
            'fields' : ['name', 'servingsize'],
            'preset' : {
             },
             'postpostprocessor' : self.postpostproc,
        },
        'edit' : {
            'fields' : ['name'],
            'preset' : {
             },
        },
        'view' : {
            'fields' : ['id', 'name', 'calories', 'fat', 'carbs', 'protein'],
            'preset' : {
             },
        },
        'list' : {
            'fields' : ['id', 'name', 'calories', 'fat', 'carbs', 'protein'],
            'preset' : {
             },
        },
        'join' :
          [
            {
             'type'       : 'many',
             'conditions' : [
               {
                 'table'     : 'ingredient',
               },
               {
                 'table'     : 'recipe_ingredient',
                 'type'      : 'where',
                 'condition' : 'recipe_ingredient.recipeid=%s '                    +
                               ' and recipe_ingredient.ingredientid=ingredient.id' +
                               ' and recipe_ingredient.recipeid=recipe.id',
                 'variables' : ['id'],
               }, 
             ],
             'new'       : {
                 'table'     : 'recipe_ingredient',
                 'gather'    : ['ingredientid', 'servingsize'],
                 'preset'    : {
                    'recipeid' : 'id',
                 },
             },
             'view' : {
                'fields' : [
                    'ingredient.id', 
                    'ingredient.name', 
                    'ingredient.servingsize', 
                    'ingredient.fat',
                    'ingredient.carbs',
                    'ingredient.protein',
                ],
                'preset' : {
                },
             },
            },
          ],
      };

  def postpostproc(self, args):
      s = args['squids']['ingredient'];
      id = args['data']['id'];
      s.query(
      )




class Snacklog(squirrel.squid.Squid):
  form = {
    'search' : {
       'defaults': ['date', 'client.user'],
       'order'   : 'order by date desc',
    },
    'new' : {
        'fields' : ['date', 'clientid'],
        'preset' : {
         },
    },
    'edit' : {
        'fields' : ['date', 'clientid'],
        'preset' : {
         },
    },
    'view' : {
        'fields' : ['id', 'date', 'client.user'],
        'preset' : {
         },
    },
    'list' : {
        'fields' : ['date', 'client.user'],
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
         'conditions' : [
           {
             'table'     : 'recipe',
           },
           {
             'table'     : 'snacklog_recipe',
             'type'      : 'where',
             'condition' : 'snacklog_recipe.recipeid=recipe.id '          +
                           ' and snacklog_recipe.snacklogid=snacklog.id ' +
                           ' and snacklog_recipe.snacklogid=%s',
             'variables' : ['id'],
           }, 
         ],
         'new'       : 
         {
             'table'     : 'snacklog_recipe',
             'gather'    : ['recipeid', 'servingsize'],
             'preset'    : {
                'snacklogid' : 'id',
             },
         },
         'view' : {
            'fields' : [
                'recipe.id', 
                'recipe.name', 
                'recipe.fat',
                'recipe.carbs',
                'recipe.protein',
            ],
            'preset' : {
            },
         },
      }, {
         'type'       : 'many',
         'conditions' : [
           {
             'table'     : 'ingredient',
           },
           {
             'table'     : 'snacklog_ingredient',
             'type'      : 'where',
             'condition' : 'snacklog_ingredient.ingredientid=ingredient.id '  +
                           ' and snacklog_ingredient.snacklogid=snacklog.id ' +
                           ' and snacklog_ingredient.snacklogid=%s',
             'variables' : ['id'],
           }, 
         ],
         'new'       : 
         {
             'table'     : 'snacklog_ingredient',
             'gather'    : ['ingredientid', 'servingsize'],
             'preset'    : {
                'snacklogid' : 'id',
             },
         },
         'view' : {
            'fields' : [
                'ingredient.id', 
                'ingredient.name', 
                'ingredient.fat',
                'ingredient.carbs',
                'ingredient.protein',
            ],
            'preset' : {
            },
         },
      },

    ],
  };
  def __init__(self, config, table):
      super().__init__(config, table);



class SnacklogIngredient(squirrel.squid.Squid):
  form = {
    'new' : {
        'fields' : ['ingredientid', 'snacklogid'],
        'preset' : {
         },
    },
    'edit' : {
        'fields' : ['ingredientid', 'snacklogid'],
        'preset' : {
         },
    },
    'list' : {
        'fields' : ['ingredient.name', 'snacklog.id'],
        'preset' : {
         },
    },
    'view' : {
        'fields' : ['ingredient.name', 'snacklog.id'],
        'preset' : {
         },
    },
    'join'  : [
        {
          'type'       : 'one',
          'foreignkey' : 'ingredientid',
          'table'      : 'ingredient',
          'primarykey' : 'id',
          'pseudonym'  : 'ingredient',
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
  def __init__(self, config, table):
      super().__init__(config, table);



class SnacklogRecipe(squirrel.squid.Squid):
  form = {
    'new' : {
        'fields' : ['recipeid', 'snacklogid'],
        'preset' : {
         },
    },
    'edit' : {
        'fields' : ['recipeid', 'snacklogid'],
        'preset' : {
         },
    },
    'list' : {
        'fields' : ['recipe.name', 'snacklog.id'],
        'preset' : {
         },
    },
    'view' : {
        'fields' : ['recipe.name', 'snacklog.id'],
        'preset' : {
         },
    },
    'join'  : [
        {
          'type'       : 'one',
          'foreignkey' : 'recipeid',
          'table'      : 'recipe',
          'primarykey' : 'id',
          'pseudonym'  : 'recipe',
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
  def __init__(self, config, table):
      super().__init__(config, table);



class RecipeIngredient(squirrel.squid.Squid):
  form = {
    'new' : {
        'fields' : ['ingredientid', 'recipeid'],
        'preset' : {
         },
    },
    'edit' : {
        'fields' : ['ingredientid', 'recipeid'],
        'preset' : {
         },
    },
    'list' : {
        'fields' : ['ingredient.name', 'recipe.name'],
        'preset' : {
         },
    },
    'view' : {
        'fields' : ['recipe_ingredient.id', 'ingredient.id', 'recipe.id', 'ingredient.name', 'recipe.name'],
        'preset' : {
         },
    },
    'join'  : [
        {
          'type'       : 'one',
          'foreignkey' : 'ingredientid',
          'table'      : 'ingredient',
          'primarykey' : 'id',
          'pseudonym'  : 'ingredient',
          'fields'     : ['name']
        },
        {
          'type'       : 'one',
          'foreignkey' : 'recipeid',
          'table'      : 'recipe',
          'primarykey' : 'id',
          'pseudonym'  : 'recipe',
          'fields'     : ['name']
        },
    ]
  };
  def __init__(self, config, table):
      super().__init__(config, table);
