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
import string
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


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



class MainHandler(webapp2.RequestHandler):
    
    def render(self, template, **kwargs):
        t = jinja_env.get_template(template)
        self.response.out.write(t.render(kwargs))

    #when browser sends a get request, the get method responds with
    #the required document. This generally has a response object to
    #provide browser with HTML to be rendered. If the request has parameters
    #supplied in the for ?param='someValue' then a self.request.get line might
    #be defined to handle that request
    #Remember, browser makes a GET REQUEST and server RESPONDS
    #with a GET RESPONSE, which is usually HTML
    def get(self, encodedString=''):
        self.render('rot13-form.html', text='')
                                

    #def post(self):
        #encode the typed string that is accessed by
        #self.request.get('text')
        #encodedString=rot13Encode(self.request.get('text'))
        #pass this encoded text back to the textarea
        #self.render('rot13-form.html', text=encodedString)
        #self.redirect('/output?encodedString='+encodedString)

class Rot13Handler(MainHandler):
    def post(self):
        #encode the typed string that is accessed by
        #self.request.get('text')
        #encodedString=rot13Encode(self.request.get('text'))
        #pass this encoded text back to the textarea
        #self.render('rot13-form.html', text=encodedString)
        encodedString = rot13Encode(self.request.get('text'))
        self.response.out.write(encodedString)
        self.response.out.write(self.response)

 #In this example, instead of redirecting which requires that the parameter be
#passed in the URL, I am setting the redirect target by using the "action" attribute in the form
        #tag and then defining post method in the handler for the "action" attr. The post
        #method use the request.get to obtain the text from the <textfield>, encodes it
        #and then send response by response.out.write to browser to displat the text

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/output', Rot13Handler)
], debug=True)
