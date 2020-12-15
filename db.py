import pymysql
from pymysql import connect

db = connect("us-cdbr-east-02.cleardb.com", "bed556e7305b73", "df0e3315", "heroku_80ac70680d841f5")
c = db.cursor()

#database data
#-------------------------------------
#user: bed556e7305b73
#password: df0e3315
#host: us-cdbr-east-02.cleardb.com
#database_name: heroku_80ac70680d841f5

#create main table
c.execute("CREATE TABLE `heroku_80ac70680d841f5`.`user` ( `id` VARCHAR(255) NOT NULL , `anime` LONGTEXT NOT NULL , UNIQUE (`id`))")
db.commit()












