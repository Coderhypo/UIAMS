SDUT-UIAMS
=========

山东理工大学-大学生创新活动管理系统

  How to use it?

    1.virtualenv venv
    2.source venv/bin/activate
    3.pip2 install -r requirenments.txt
	4.mysql
	- database dev_db root:password
	- create database dev_db default CHARSET=UTF8;
    5.python manage.py deploy
	6.python manage.py runserver
