from setuptools import setup

setup(
	name='cafemenu',
	version='1.0',
	description='Barisca cafe management system',
	author='Erfan Naeini',
	author_email='erfannaeini2@gmail.com',
	packages=['cafemenu'],
	install_requires=[
		'django-channels',
		'psycopg2',
	],
)