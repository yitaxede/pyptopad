#!/usr/bin/python
import xml.etree.ElementTree as ET


#Database format example

db_string = '''
<database>
    <note name='love letter to Jane'>
        <text color='red'>Dear Jane, </text>
        <text fontsize='16'>I LOVE YOU!</text>
    </note>
    <note name='love letter to Molly'>
        <text color='blue'>Dear Molly, </text>
        <text fontsize='22'>I LOVE YOU!</text>
    </note>
    <note name='2buy'>
        <text>red roses</text>
        <text>white wine</text>
        <text>condoms</text>
    </note>
</database>
'''

'''
Usage:
>>> db = Database(db_string)
>>> db.attributes
{}
>>> db.Notes[0].attributes
{'name': 'love letter to Jane'}
>>> db.Notes[0].Texts[0].attributes
{'color': 'red'}
>>> db.Notes[0].Texts[0].content
'Dear Jane, '

'''

class Database:
    Notes = []
    attributes = {}
    
    def __init__(self, xml_string=None):
        if xml_string == None:
            return self
            
        db = ET.fromstring(xml_string)
        self.attributes = db.attrib.copy()
        
        for note in db:
            self.Notes.append(Note(note))
        
        
    def to_xml_string(self):
        xml = ET.Element('database')
        xml.attrib = self.attributes.copy()
        for note in self.Notes:
            xml.append(note.to_xml())
        return ET.tostring(xml)

    
class Note:
    Texts = []
    attributes = {}
    
    def __init__(self, xml=None):
        if xml == None:
            return self
            
        self.attributes = xml.attrib.copy()
            
        for txt in xml:
            self.Texts.append(Text(txt))
    
    def to_xml(self):
        xml = ET.Element('note')
        xml.attrib = self.attributes.copy()
        for text in self.Texts:
            xml.append(text.to_xml())
        return xml
        
        
class Text:
    content = ''
    attributes = {}
    
    def __init__(self, xml=None):
        if xml == None:
            return self
            
        self.attributes = xml.attrib.copy()
        self.content = xml.text
        
    def to_xml(self):
        xml = ET.Element('text')
        xml.text = self.content
        xml.attrib = self.attributes.copy()
        return xml
        
