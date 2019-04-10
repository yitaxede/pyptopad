#!/usr/bin/python
'''
Database format example

<database>
    <note name='love letter to Jane'>
        <txt color='red'>Dear Jane, </txt>
        <txt fontsize=16>I LOVE YOU!</txt>
    </note>
    <note name='love letter to Molly'>
        <txt color='blue'>Dear Molly, </txt>
        <txt fontsize=22>I LOVE YOU!</txt>
    </note>
    <note name='2buy'>
        <txt>red roses</txt>
        <txt>white wine</txt>
        <txt>condoms</txt>
    </note>
</database>
'''



class Database:
    Notes = []
    
    
class Note:
    name = None
    Texts = []
    
    def __init__(self, name):
        self.name = name
        
        
class Text:
    content = None
    attributes = None
    
    def __init__(self, content, attributes = {}):
        self.content = content
        self.attributes = attributes
