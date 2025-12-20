
# closeable

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

ファイル等の閉じる動作を定義するために使えるインターフェイス・クラスを提供します。

## Usage

`ICloseable, Closeable` を使用した簡単な動作例。

`ICloseable` で動作の規定を行い `Closeable` が実際の動作を担当します。

```py
from closeable import ICloseable, Closeable

class Sample (ICloseable):

  def __init__ (self):
    self.closeable = Closeable(self._on_close)

  def _on_close (self):
    print("closed!")

  def close (self):
    self.closeable.close()

  @property
  def closed (self) -> bool:
    return self.closeable.closed

  def put (self, data:str):
    self.closeable.raise_if_closed()
    print("put: {:s}".format(data))

sample = Sample()
sample.closed #False
sample.put("hello!") #put: hello!
sample.close() #closed!
sample.close()
sample.closed #True
sample.put("hello!") #raise CloseableStateError!
```

## Install

```shell
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import closeable

help(closeable)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

closeable licensed under the [AGPLv3](./LICENSE).
