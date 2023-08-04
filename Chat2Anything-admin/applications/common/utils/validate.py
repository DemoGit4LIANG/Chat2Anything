# xss过滤
import validators
from flask import escape
from validators import validator


def str_escape(s):
    if not s:
        return None
    return str(escape(s))


between = validators.between
'''
验证数字是否介于最小值和/或最大值之间。
这将适用于任何类似的类型，如浮点数、小数和日期，而不仅仅是整数。
between(value, min=None, max=None)

    min-数字的最小必需值。如果未提供，则不会检查最小值。
    max-数字的最大值。如果未提供，将不检查最大值。

        >>> from datetime import datetime
        
        >>> between(5, min=2)
        True
        
        >>> between(13.2, min=13, max=14)
        True
        
        >>> between(500, max=400)
        ValidationFailure(func=between, args=...)
        
        >>> between(
        ...     datetime(2000, 11, 11),
        ...     min=datetime(1999, 11, 11)
        ... )
        True
'''

domain = validators.domain
'''
返回给定值是否为有效域
如果值是有效域名，则此函数返回 True ，否则返回 ValidationFailure
domain(value)
    value-要验证的属性域字符串
    
        >>> domain('example.com')
        True
        
        >>> domain('example.com/')
        ValidationFailure(func=domain, ...)
'''

email = validators.email
'''
 验证电子邮件地址。验证成功时返回 True ，验证失败时返回
     
     >>> email('someone@example.com')
    True
    
    >>> email('bogus@@')
    ValidationFailure(func=email, ...)
'''

iban = validators.iban
'''
返回给定值是否为有效的IBAN代码。
如果值是有效的IBAN，则此函数返回 True ，否则返回 ValidationFailure 。

    >>> iban('DE29100500001061045672')
    True
    
    >>> iban('123456')
    ValidationFailure(func=iban, ...)
'''

ipv4 = validators.ipv4
'''
返回给定值是否为有效的IPv4地址。

    >>> ipv4('123.0.0.7')
    True
    
    >>> ipv4('900.80.70.11')
    ValidationFailure(func=ipv4, args={'value': '900.80.70.11'})
'''

ipv6 = validators.ipv6
'''
返回给定值是否为有效的IP版本6地址。
    >>> ipv6('abcd:ef::42:1')
    True
    
    >>> ipv6('abc.0.0.1')
    ValidationFailure(func=ipv6, args={'value': 'abc.0.0.1'})
'''

length = validators.length
'''
返回给定字符串的长度是否在指定范围内。
    >>> length('something', min=2)
    True
    
    >>> length('something', min=9, max=9)
    True
    
    >>> length('something', max=5)
    ValidationFailure(func=length, ...)
'''

mac_address = validators.mac_address
'''
返回给定值是否为有效MAC地址。
如果该值是有效的MAC地址，则此函数返回 True ，否则返回 ValidationFailure 。

    >>> mac_address('01:23:45:67:ab:CD')
    True
    
    >>> mac_address('00:00:00:00:00')
    ValidationFailure(func=mac_address, args={'value': '00:00:00:00:00'})
'''

slug = validators.slug
'''
验证给定值是否为有效的块。
有效的短信息只能包含字母数字字符、连字符和下划线。
    >>> slug('my.slug')
    ValidationFailure(func=slug, args={'value': 'my.slug'})
    
    >>> slug('my-slug-2134')
    True
'''

truthy = validators.truthy
'''
验证给定值不是错误值。
'''

url = validators.url
'''
返回给定值是否为有效URL。
如果值是有效URL，则此函数返回 True ，否则返回 ValidationFailure 。

    >>> url('http://foobar.dk')
    True
    
    >>> url('http://10.0.0.1')
    True
    
    >>> url('http://foobar.d')
    ValidationFailure(func=url, ...)
    
    >>> url('http://10.0.0.1', public=True)
    ValidationFailure(func=url, ...)
'''

uuid = validators.uuid
'''
返回给定值是否为有效UUID。
如果值是有效的UUID，则此函数返回 True ，否则返回 ValidationFailure 。

    >>> uuid('2bc1c94f-0deb-43e9-92a1-4775189ec9f8')
    True
    
    >>> uuid('2bc1c94f 0deb-43e9-92a1-4775189ec9f8')
    ValidationFailure(func=uuid, ...)
'''


@validator
def even(value):
    return not (value % 2)


'''
一个装饰器，它使给定的函数验证器
每当给定函数被调用并返回 False 值时，这个装饰器返回 ValidationFailure 对象。
>>> @validator
... def even(value):
...     return not (value % 2)

>>> even(4)
True

>>> even(5)
ValidationFailure(func=even, args={'value': 5})
'''
