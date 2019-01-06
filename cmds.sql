
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


