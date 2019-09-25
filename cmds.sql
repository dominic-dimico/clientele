
create table client (
  id integer primary key not null auto_increment,
  user varchar(64),
  name varchar(128),
  dob datetime,
  phone varchar(10),
  email varchar(256),
  services varchar(256),
  lastcontact datetime,
  sex boolean,
  notes text
);


# create table status (
#   id integer primary key autoincrement,
#   time datetime,
#   weight smallint,
#   height tinyint,
#   neck tinyint,
#   waist tinyint
# );
# 
# 
# create table exercise (
#   id integer primary key autoincrement,
#   muscles bit(16),
#   contractions bit(3)
# );
# 
# 
# create table tempo (
#   id integer primary key autoincrement,
#   nickname varchar(16),
#   eccentric tinyint,
#   midpoint tinyint,
#   concentric tinyint,
#   pause tinyint 
# );
# 
# create table exset (
#   id integer primary key autoincrement,
#   time datetime,
#   reps smallint,
#   exerciseid int,
#   tempoid int,
#   clientid int,
#   foreign key (exerciseid) references exercise(id),
#   foreign key (tempoid) references tempo(id),
#   foreign key (clientid) references client(id)
# );


create table session (
  id integer primary key not null auto_increment,
  time datetime,
  payment smallint,
  notes text,
  clientid int,
  foreign key (clientid) references client(id)
); 



# media: can be 'email', 'text', 'skype', 'any'
create table message (
  id integer primary key not null auto_increment,
  media varchar(64),
  subject varchar(64),
  body text,
  attachments text,
  tags text
); 


# timestamp can be set for future
create table delivery (
  id integer primary key not null auto_increment,
  timestamp datetime,
  client_id integer,
  message_id integer,
  foreign key (client_id) references client(id),
  foreign key (message_id) references message(id)
); 


create table fooditem (
  id integer primary key not null auto_increment,
  name varchar(256),
  servingsize int,
  calories int,
  fat int,
  carbs int,
  protein int
);


create table foodsummary (
  id integer primary key not null auto_increment,
  name varchar(256),
  date datetime,
  calories int,
  fat int,
  carbs int,
  protein int,
  notes text
);


create table foodconsumption (
  id integer primary key not null auto_increment,
  date datetime,
  servings float,
  notes text,
  clientid int,
  fooditemid int,
  foreign key (clientid) references client(id),
  foreign key (fooditemid) references fooditem(id)
);
