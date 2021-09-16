import squirrel
import toolbelt
import configparser
import smartlog
import butterfly

from clientele.client import *


# Clientele interpreter
class ClientInterpreter(squirrel.squish.SquishInterpreter):

    log = smartlog.Smartlog();

    def __init__(self):
        super().__init__();
        self.initialize_configs();
        self.initialize_squids();
        self.initialize_autocomplete();


    def initialize_autocomplete(self):
        ts = {
          'client'     : ['user'],
          'exercise'   : ['name'],
        }
        objects = list(self.squids.keys());
        self.auto.words += objects;
        self.auto.words += list(self.aliases.values());
        self.auto.words += ['where', 'order', 'by'];
        for key in objects:
            self.auto.words += self.squids[key].describe().keys();
        for t in ts:
            self.squids[t].query(
               'select %s from %s' % (",".join(ts[t]), t)
            );
            for row in self.squids[t].data:
                for f in ts[t]:
                    self.auto.words += [row[f]];



    def initialize_configs(self):
        configs = {};
        configs['clientele'] = configparser.ConfigParser()
        configs['clientele'].read(
          '/home/dominic/src/clientele/clientele.cfg'
        )
        self.configs = configs;


    def initialize_squids(self):
        self.aliases = {
           'exercise_set' : 'set',
           'snacklog'     : 'log',
        }
        squids= {}
        squids['client']              = Client(self.configs['clientele'], 'client')
        squids['exercise']            = Exercise(self.configs['clientele'], 'exercise')
        squids['set']                 = ExerciseSet(self.configs['clientele'], 'exercise_set')
        squids['session']             = Session(self.configs['clientele'], 'session')
        squids['recipe']              = Recipe(self.configs['clientele'], 'recipe')
        squids['ingredient']          = Ingredient(self.configs['clientele'], 'ingredient')
        squids['snacklog']            = Snacklog(self.configs['clientele'], 'snacklog')
        squids['recipe_ingredient']   = RecipeIngredient(self.configs['clientele'], 'recipe_ingredient')
        squids['snacklog_ingredient'] = SnacklogIngredient(self.configs['clientele'], 'snacklog_ingredient')
        squids['snacklog_recipe']     = SnacklogRecipe(self.configs['clientele'], 'snacklog_recipe')
        self.squids = squids;


    def help(self):
        self.log.info("syntax: [command] ...\n");
        super().help();
        objects = [
          'client', 'exercise', 'set', 'session', 'snacklog', 'recipe', 'ingredient'
        ]
        self.log.outfile.write("\n");
        self.log.info("objects:");
        for obj in objects:
            self.log.info("  "+obj);
        self.log.outfile.write("\n");

