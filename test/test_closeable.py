
import pytest
from closeable import Closeable, CloseableStateError

def test_closeable ():

  #引数なしで初期化した場合の動作確認です

  closeable = Closeable()
  assert closeable.closed == False
  closeable.close()
  assert closeable.closed == True

def test_closeable_with_handler ():

  #引数ありで初期化した場合の動作確認です

  close_count = 0

  def on_close ():
    nonlocal close_count
    close_count += 1

  closeable = Closeable(on_close)
  assert closeable.closed == False
  closeable.close()
  closeable.close()
  closeable.close()
  assert close_count == 1
  assert closeable.closed == True

def test_closeable_must_be_open ():

  #Closeable.must_be_open() の動作確認です

  closeable = Closeable()
  closeable.must_be_open()
  closeable.close()
  with pytest.raises(CloseableStateError):
    closeable.must_be_open()

def test_closeable_must_be_close ():

  #Closeable.must_be_close() の動作確認です

  closeable = Closeable()
  with pytest.raises(CloseableStateError):
    closeable.must_be_close()
  closeable.close()
  closeable.must_be_close()
