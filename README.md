# loginsystem
basic loginsystem

Uses MYSQL as back-end database, main.py has the code to talk to the backend,
connection variables are hardcoded <-- fix soon
Queries are partially hardcoded aswell <-- fix soon
Database design -->
+----+-----------+----------+--------------------+----------+--------+------------------------------------------------------------------------------------------------+
| ID | Firstname | Lastname | EMail              | Salt     | Cookie | Password                                                                                       |
+----+-----------+----------+--------------------+----------+--------+------------------------------------------------------------------------------------------------+
|  1 | testfirst | testlast | test@testmail.test | testSalt | 3      | pbkdf2:sha256:150000$YU6lxMiB$fae00d4016d1e2b51225d2a5708990fdf55e64bd32320a9cd06a84fb0228b99b |
+----+-----------+----------+--------------------+----------+--------+------------------------------------------------------------------------------------------------+

	--	DEPENDENCIES	--
	1.	Flask
	2.	Werkzeug
	3.	pymysql
	4.	random


