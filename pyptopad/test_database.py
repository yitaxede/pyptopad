#!/usr/bin/python
import unittest
import xml.etree.ElementTree as ET
from database import Database, Note, Text


class TestSum(unittest.TestCase):
    def test_text(self):
        s = b'<text color="red">Dear Jane, </text>'
        xml = ET.fromstring(s)
        t = Text(xml)
        self.assertEqual(t.attributes, {'color':'red'})
        self.assertEqual(t.content, 'Dear Jane, ')
        self.assertEqual(ET.tostring(t.to_xml()), s)
        
    def test_note(self):
        s = b'<note name="love letter to Jane"><text color="red">Dear Jane, </text><text fontsize="16">I LOVE YOU!</text></note>'
        xml = ET.fromstring(s)
        n = Note(xml)
        self.assertEqual(n.attributes, {'name':'love letter to Jane'})
        self.assertEqual(ET.tostring(n.to_xml()), s)
        self.assertEqual(len(n.Texts), 2)

        
    def test_database(self):
        s = b'<database><note name="love letter to Jane"><text color="red">Dear Jane, </text><text fontsize="16">I LOVE YOU!</text></note><note name="love letter to Molly"><text color="blue">Dear Molly, </text><text fontsize="22">I LOVE YOU!</text></note><note name="2buy"><text>red roses</text><text>white wine</text><text>condoms</text></note></database>'
        db = Database(s)
        self.assertEqual(db.attributes, {})
        self.assertEqual(db.to_xml_string(), s)
        self.assertEqual(len(db.Notes), 3)


if __name__ == '__main__':
    unittest.main()
