Usage
=====

.. _installation:

Installation
------------

To use demonlist, first install it using pip:

.. code-block:: console

   (.venv) $ pip install demonlist

.. _import:

Import
------

After installation, you need to import the library in to your code:

.. code-block:: python
   :linenos:

   import demonlist

.. _example:

Example
-------

For example, you can call ``demonlist.Demonlist.sign_in()`` function to log in to your account:

.. autofunction:: demonlist.Demonlist.sign_in()

:py:func:`demonlist.Demonlist.sign_in()` will raise an exception.

.. autoexception:: exceptions.WrongCredentials

To do this, write the code below:

.. code-block:: python
   :linenos:

   from demonlist import Demonlist
   import asyncio


   async def main():
       client = Demonlist()
       await client.sign_in(login='SuperMinecrafter228', password='619')

   if __name__ == '__main__':
       asyncio.get_event_loop().run_until_complete(main())
