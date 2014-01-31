--------
pyrelite
--------
.. _Postgres: http://www.postgresql.org/
.. _SimpleDB: http://aws.amazon.com/simpledb/
.. _FQL: http://developers.facebook.com/docs/technical-guides/fql/

A lightweight toolkit for generating SQL strings from simple relational expressions.

Right now only supports `Postgres`_, `SimpleDB`_ and `FQL`_.

Installation
------------

.. code-block::

    $ python setup.py install
    $ make clean
    
Postgres Example
----------------
Here's how to build a couple of simple Postgres queries::

    >>> from pyrelite import postgres
    >>> d = postgres.Domain('mydomain')
    >>> d.select(postgres.Star()).where((d['first_name'] == 'Charlie') | (d['first_name'] == 'Delta')).to_sql()
    "select * from mydomain where (first_name = 'Charlie') or (firt_name = 'Delta')"
    
    >>> col_names = ['id', 'first_name', 'last_name', 'city']
    >>> ids = [1, 2, 3, 4]
    >>> stmt = d.select(*map(d.column, col_names))
    >>> stmt.where(d.column('id').in_(*ids)).to_sql()
    'select id, first_name, last_name, city from mydomain where id in (1, 2, 3, 4)'

SimpleDB Example
----------------

Here's how to build a simple query for SimpleDB, in a couple different ways::

    >>> from pyrelite import simpledb
    >>> d = simpledb.Domain('mydomain')
    >>> d.select(simpledb.Star()).where(d['city'] == 'Seattle').to_sql()
    'select * from mydomain where city = "Seattle"'

    >>> from pyrelite import project, select
    >>> expr = select(project(d, [simpledb.Star()]), d['city'] == 'Seattle')
    >>> simpledb.Compiler().compile(expr)
    'select * from mydomain where city = "Seattle"'


FQL Example
-----------

Here's how to build a simple FQL query::

    >>> from pyreqlite import fql
    >>> u = fql.Table('user')
    >>> u.select(u['name']).where(u['uid'] == fql.Me()).to_sql()
    'select name from user where uid = me()'

Running Tests
-------------

Run the tests by invoking the ``make`` task::

    $ make test
