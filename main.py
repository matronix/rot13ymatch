#!/usr/local/bin python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import string

def escape_html(s):
    return cgi.escape(s, quote=True)

letters = list(string.ascii_lowercase)
#Given a letter, returns its rot13 complement adjusting for index >25
#which would overflow beyond letter z. For upper-case letters it returns
#the complement in lower=case. For non letter symbols and numbers it returns
#none.
def rot13Complement(letter):
    letterLower = letter.lower()
    if letterLower in letters:
        letterIndex = letters.index(letterLower)
        letterRot13Index = letterIndex+13
        if letterRot13Index>25:
            letterRot13Index = letterRot13Index-1-25
        if letter.islower():
            return letters[letterRot13Index]
        else:
            return letters[letterRot13Index].capitalize()
    else:
        return letter
    
        
        
#A function that returns the rot13 complement of a string
def rot13Encode(s):
    resultString = ''
    for letter in s:
        resultString = resultString+rot13Complement(letter)

    return resultString


form="""
<h2>Enter some text to ROT13:</h2>
<form method="post">
      <textarea name="text" style="height: 100px; width: 400px;">%(encodedString)s</textarea>
      <br>
      <input type="submit">
    </form>
"""



class MainHandler(webapp2.RequestHandler):
    def get(self, encodedString=''):
        self.response.out.write(form%({'encodedString':escape_html(encodedString)}))

    def post(self):
        #encode the typed string that is accessed by
        #self.request.get('text')
        encodedString=rot13Encode(self.request.get('text'))
        #pass encodedString through the escape_html filter to escape
        #html and other special chars
        #encodedString = escape_html(encodedString)
        #pass this encoded text back to the textarea
        self.response.out.write(form%({'encodedString':escape_html(encodedString)}))
#        self.response.out.write(encodedString)
        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
