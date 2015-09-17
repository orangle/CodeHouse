south在django1.6中的使用
====================

>django1.7中已经支持数据合并了，所以只能在django1.4 1.5 1.6的版本中使用south。
south的主要作用就是做数据的合并，当我们在django中定义了一个模型之后，使用syncdb同步到数据库中，而后如果
修改了模型的字段，或者字段属性，在使用syncdb就不可以了。 这时候如果要迁移数据就需要重新建库，把原始数据
迁移到新库，south可以帮您自动的完成这些操作。 之前一直没怎么用过，现在用的django版本还是1.6，最近的开发属于
模型不是很稳定的时间，于是就拿来使用下.

##说明
* django1.6
* win7
* 数据库 mysql 5.6

##安装
使用pip安装

    pip install south

如果是升级sourh（1.0应该是最后一版）

    pip install south --upgrade

##django中配置
###1
在你的django项目的settings文件中添加一个新的app (INSTALLED_APPS配置项)

    INSTALLED_APPS = (
        ...
        'south',
    )

###2
然后在项目下使用 python manage.py shell 打开django的shell

    In [1]: import south

如果没有错误，说明安装配置好了。

###3
使用之前先要在数据库中同步south的需要的表。

    python manage.py syncdb

此时数据库中已经多了south_migrationhistory这个表。
##使用

这是一个已经开发的项目，很多表和表结构已经建立好也是用syncdb同步到数据库中。
app的名称是 adsr， 有个模型为

    class AdDailyReport(models.Model):

        ad = models.ForeignKey(Ad, on_delete=models.PROTECT)
        ddate = models.DateField(auto_now=False, auto_now_add=False, verbose_name=u'统计日期')
        pv = models.IntegerField(default=0, verbose_name=u'展现量')
        pc = models.IntegerField(default=0, verbose_name=u'点击量')
        cost = models.DecimalField(null=True,max_digits=10, decimal_places=2, verbose_name=u'花费')
        addtime = models.DateTimeField(auto_now_add=True)

### 初始化合并
south有自动也有手动的合并方式，这里我们使用自动的方式

[新建一个app还没有syncdb的情况下使用south](http://south.readthedocs.org/en/latest/tutorial/part1.html#tutorial-part-1)

[已经存在的app，数据库已经有表的情况](http://south.readthedocs.org/en/latest/convertinganapp.html#converting-an-app)

在没有任何模型变化的时候，对现有初始化：

    E:\hawk>python manage.py convert_to_south  adsr
    This application is already managed by South.

然后才可以和新的app models一样，修改，合并模式，应用合并.

###修改模型
模型最后添加了一个记录更新时间的字段

    updatetime = models.DateTimeField(auto_now=True)

###south 修改模式，应用

    E:\hawk>python manage.py schemamigration adsr --auto

给了一些提示

    E:\hawk>python manage.py schemamigration adsr --auto
     ? The field 'AdDailyReport.updatetime' does not have a default specified, yet i
    s NOT NULL.
     ? Since you are adding this field, you MUST specify a default
     ? value to use for existing rows. Would you like to:
     ?  1. Quit now, and add a default to the field in models.py
     ?  2. Specify a one-off value to use for existing columns now
     ? Please select a choice:

 google下[stackoverflow上的回答](http://stackoverflow.com/questions/18776953/south-schemamigration-asking-for-one-off-value-when-trying-to-mirgate-app), 然后如下的操作

      ? Please select a choice: 2
     ? Please enter Python code for your one-off default value.
     ? The datetime module is available, so you can do e.g. datetime.date.today()
     >>> datetime.datetime.now()
     + Added field updatetime on adsr.AdDailyReport
    Created 0002_auto__add_field_addailyreport_updatetime.py. You can now apply this
     migration with: ./manage.py migrate adsr

这样就把新的数据模型生成了，然后是应用。

    E:\hawk>python manage.py migrate adsr

把表变更和数据合并应用，这样就把新的表结构生成，并且自动迁移数据。


##ref
[高级的应用](http://south.readthedocs.org/en/latest/tutorial/index.html)







