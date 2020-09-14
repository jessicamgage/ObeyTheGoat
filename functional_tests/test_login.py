from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest

TEST_EMAIL = 'onlyforbook61@gmail.com'
SUBJECT = 'Your login link for TheToDoListSite'

class LoginTest(FunctionalTest):
	def test_can_get_email_link_to_log_in(self):
		#Edith goes to the awesome todolistsite
		#and notices a 'login' section in the navbar
		#It's telling her to enter her email address
		
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
		self.browser.find_element_by_name('email').send_keys(Keys.ENTER)
		
		#A message appears telling her an email has been sent

		self.wait_for(lambda: self.assertIn(
			'Check your email',
			self.browser.find_element_by_tag_name('body').text))

		#She checks her email and finds a message
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		#It has a URL link in it
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(f'Could not find url in email body:\n{email.body}')
		url = url_search.group(0)
		self.assertIn(self.live_server_url, url)
	
		#she clicks it
		self.browser.get(url)

		#she is logged in!
		self.wait_to_be_logged_in(email=TEST_EMAIL)

		#Now she logs out
		self.browser.find_element_by_link_text('Log out').click()
		
		#she is logged out
		self.wait_to_be_logged_out(email=TEST_EMAIL)
