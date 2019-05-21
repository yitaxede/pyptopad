#!/usr/bin/python
import xml.etree.ElementTree as ET

class Database:
    """
    Database format example
    
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
    """
    def __init__(self, xml_string=None):
        """
        Initialize the database

        Parameters
        ----------
        xml_string :  string
            A string containing the XML representation of the database.
            Look above for database format details.
            If not specified, create an empty database.
        """
        self.Notes = []
        self.attributes = {}

        if xml_string is None:
            return

        db = ET.fromstring(xml_string)
        self.attributes = db.attrib.copy()

        for note in db:
            self.Notes.append(Note(note))

    def to_xml_string(self):
        """
        Convert the database to its string representation.

        Returns:
        ----------
        bytes :
            String containing the XML representation of the database.
        """
        xml = ET.Element('database')
        xml.attrib = self.attributes.copy()
        for note in self.Notes:
            xml.append(note.to_xml())
        return ET.tostring(xml)


class Note:
    """
    Note format example
    <note name='love letter to Jane'>
        <text color='red'>Dear Jane, </text>
        <text fontsize='16'>I LOVE YOU!</text>
    </note>
    """
    def __init__(self, xml=None):
        """
        Initialize the note

        Parameters
        ----------
        xml :  xml.etree.ElementTree.Element
            XML object <note>.
            Look above for note format details.
            If not specified, create an empty note.
        """
        self.Texts = []
        self.attributes = {}

        if xml is None:
            return

        self.attributes = xml.attrib.copy()

        for txt in xml:
            self.Texts.append(Text(txt))

    def to_xml(self):
        """
        Convert the note to its XML representation.

        Returns:
        ----------
        xml.etree.ElementTree.Element :
            XML representation of the note.
        """
        xml = ET.Element('note')
        xml.attrib = self.attributes.copy()
        for text in self.Texts:
            xml.append(text.to_xml())
        return xml


class Text:
    """
    Text format example
        <text color='red' fontsize='16'>Dear Jane, </text>
    """
    def __init__(self, xml=None):
        """
        Initialize the Text

        Parameters
        ----------
        xml :  xml.etree.ElementTree.Element
            XML object <text>.
            Look above for text format details.
            If not specified, create an empty text.
        """
        self.content = ''
        self.attributes = {}

        if xml is None:
            return

        self.attributes = xml.attrib.copy()
        self.content = xml.text

    def to_xml(self):
        """
        Convert the text to its XML representation.

        Returns:
        ----------
        xml.etree.ElementTree.Element :
            XML representation of the text element.
        """
        xml = ET.Element('text')
        xml.text = self.content
        xml.attrib = self.attributes.copy()
        return xml
