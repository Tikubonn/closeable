
from abc import ABC, abstractmethod
from typing import Callable

"""閉じる機能をもつオブジェクトを定義するためのインタフェイス・クラスを提供します。

Examples
--------
>>> from closeable import ICloseable, Closeable
>>> 
>>> class Sample (ICloseable):
>>>   def __init__ (self):
>>>     self.closeable = Closeable(self._on_close)
>>> 
>>>   def _on_close (self):
>>>     print("closed!")
>>> 
>>>   def close (self):
>>>     self.closeable.close()
>>> 
>>>   @property
>>>   def closed (self) -> bool:
>>>     return self.closeable.closed
>>> 
>>>   def put (self, data:str):
>>>     self.closeable.raise_if_closed()
>>>     print("put: {:s}".format(data))
>>> 
>>> sample = Sample()
>>> sample.closed
False
>>> sample.put("hello!")
put: hello!
>>> sample.close()
closed!
>>> sample.close()
>>> sample.closed
True
>>> sample.put("hello!")
CloseableStateError: Object has already closed: <...>
"""

class ICloseable (ABC):

  """閉じる機能の規格を提供します。
  """

  @property
  @abstractmethod
  def closed (self) -> bool:

    """オブジェクトが閉じられた状態なのかを判定します。

    Returns
    -------
    bool
      オブジェクトが閉じられていれば `True` そうでなければ `False` を返します。
    """

    pass

  @abstractmethod
  def close (self, *args, **kwargs):

    """オブジェクトを閉じます。"""

    pass

class CloseableStateError (Exception):

  """オブジェクトの状態が許容しない操作が行われた際に送出される例外です。"""

  pass

class Closeable (ICloseable):

  """閉じる機能を提供します。

  新規のクラスに閉じる機能を追加するために定義されました。
  対象のクラスに `ICloseable` を継承させ、各種処理を本インスタンスから委譲してもらう方法を想定しています。

  Examples
  --------
  >>> class Sample (ICloseable):
  >>>   def __init__ (self):
  >>>     self._closeable = Closeable(self._on_close)
  >>>   def _on_close (self):
  >>>     print("closed!")
  >>>   @property
  >>>   def closed (self) -> bool:
  >>>     return self._closeable.closed
  >>>   def close (self):
  >>>     self._closeable.close()
  >>> sample = Sample()
  >>> sample.closed
  False
  >>> sample.close()
  closed!
  >>> sample.close()
  >>> sample.closed
  True
  """

  def __init__ (self, close_func:Callable=None):

    """インスタンスの初期化を行います。

    Parameters
    ----------
    close_func : Callable
      オブジェクトが閉じられる時に一度だけ実行される関数です。
      未指定ならば `None` が設定され、何も実行されません。
    """

    self._close_func = close_func
    self._closed = False

  @property
  def closed (self) -> bool:
    return self._closed

  def close (self, *args, **kwargs):

    """オブジェクトを閉じます。

    Notes
    -----
    オブジェクトが閉じられる時に一度だけ設定された `close_func` 関数が実行されます。
    本メソッドを実行時、任意の引数を指定することができ、それらは `close_func` 関数の実行時に渡されます。

    Parameters
    ----------
    args : tuple[Any, ...]
      `close_func` に渡される任意の引数です。
    kwargs : dict[str, Any]
      `close_func` に渡される任意のキーワード引数です。
    """

    if not self._closed:
      if self._close_func:
        self._close_func(*args, **kwargs)
      self._closed = True

  def must_be_open (self):

    """オブジェクトが開かれた状態でなければ例外を送出します。

    Raises
    ------
    CloseableStateError
      オブジェクトが既に閉じられた状態で本メソッドが呼ばれた場合に送出されます。
    """

    if self._closed:
      raise CloseableStateError("Object has already closed: {:s}".format(repr(self)))

  def must_be_close (self):

    """オブジェクトが閉じられた状態でなければ例外を送出します。

    Raises
    ------
    CloseableStateError
      オブジェクトが開かれた状態で本メソッドが呼ばれた場合に送出されます。
    """

    if not self._closed:
      raise CloseableStateError("Object has never closed yet: {:s}".format(repr(self)))
