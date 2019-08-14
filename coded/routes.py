import os
import secrets
from PIL import Image
from collections import OrderedDict 
from flask import render_template, url_for, flash, redirect, request, abort
from coded import app, db, bcrypt

courses = {
	'iOS-Dev': {
		'title': 'iOS-Dev',
		'desc': 'In the iOS course, instructor Sanaan Akhter will be \
				 introducing you to the development of iOS applications \
				 through the creation of an application of your own!',
		'author': 'Sanaan Akhter',
		'playlists': {
			'Your First App': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2017 Promo': '14-j4CvRGIg',
				'THON 2017 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2018 Promo': '14-j4CvRGIg'
			},
			'Swift Basics': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U'
			},
			'iOS Game App': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2017 Promo': '14-j4CvRGIg',
				'This Is ichigan': 'UqoJmSF235E',
				'THON 2018 Promo': 'z-Bk09yXVBo',
				'THON 2017 Weekend Recap': 'oh3vsFDIa7U'
			}
		},
		'sizes': {
			'Your First App': '6',
			'Swift Basics': '3',
			'iOS Game App': '7'
		}
	},
	'Web-Dev': {
		'title': 'Web-Dev',
		'desc': 'In the web course, instructor Chinmay Savanur will be \
				 introducing you to the development of website based \
				 applications through a series of lessons ending in your \
				 own first responsive website!',
		'author': 'Chinmay Savanur',
		'playlists': {
			'Your First Website':  {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2017 Promo': '14-j4CvRGIg',
				'THON 2017 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2018 Promo': '14-j4CvRGIg'
			},
			'HTML Basics': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2020 Weekend Recap': 'oh3vsFDIa7U'
			},
			'CSS Basics': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U'
			},
			'Blog Website': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2017 Promo': '14-j4CvRGIg',
				'This Is ichigan': 'UqoJmSF235E',
				'THON 2018 Promo': 'z-Bk09yXVBo',
				'THON 2017 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2019 Promo': '14-j4CvRGIg'
			}
		},
		'sizes': {
			'Your First Website': '6',
			'HTML Basics': '4',
			'CSS Basics': '3',
			'Blog Website': '8'
		}
	},
	'Java': {
		'title': 'Java',
		'desc': 'In this introduction to programming in java course, \
				 Sara WHitlock will cover the same topics as the \
				 AP Computer Science.',
		'author': 'Sara Whitlock',
		'playlists': {
			'Your First Program': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U'
			},
			'Java Basics': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2019 Promo': 'z-Bk09yXVBo',
				'THON 2019 Weekend Recap': 'oh3vsFDIa7U',
				'THON 2020 Weekend Recap': 'oh3vsFDIa7U'
			},
			'Java Applications': {
				'This Is Michigan': 'UqoJmSF235E',
				'THON 2016 Promo': 'z-Bk09yXVBo',
				'THON 2016 Weekend Recap': 'oh3vsFDIa7U'
			}
		},
		'sizes': {
			'Your First Program': '3',
			'Java Basics': '6',
			'Java Applications': '3'
		}
	},
	'C++': {
		'title': 'C++',
		'desc': 'In the Introduction to C++ course, instructor Jared Miller \
				 will be covering the basics of coding in C++ up through the \
				 traditional intro course in University.',
		'author': 'Jared Miller',
		'playlists': {
			'Basics':  {
				'Part 0: Creating "Hello World!"': 'ikYXSabw9V0',
				'Part 1: Output & Comments': 'p-vsNAp6M6w',
				'Part 2: Variables & Input': 'Oze4Rja9gVw',
				'Part 3: Functions': 'fliui3TTFCc',
				'Part 4: Scope': 'yYQmJUEy91U',
				'Part 5: Math Operators': 'habMcH1SaQc',
				'Part 6: String Functions': 'OD3-5j7MMkI',
				'Part 7: Booleans & Conditionals': 'ys5mCH8LCMU',
				'Part 8: If Statements': 'N4HRY-QUifU',
				'Part 9: While Loops': 'O3udG8-e4tE',
				'Part 10: For Loops': 'RHh2bQS3DtU',
				'Part 11: Arrays': 'Nn9nqV1H3Jg',
				'Part 12: Vectors': '3joCytKMix0'
			},
			'Data Structures':  {
				'Part 0: Classes': 'ikYXSabw9V0',
				'Part 1: Arrays in Memory': 'p-vsNAp6M6w',
				'Part 2: Linked Lists': 'Oze4Rja9gVw',
				'Part 3: Doubly Linked Lists': 'fliui3TTFCc',
				'Part 4: Maps': 'yYQmJUEy91U',
			}
		},
		'sizes': {
			'Basics': '13',
			'Data Structures': '5',
		}
	}
}

teammembers = {
	'Jared Miller': 'Jared Miller is a sophomore persuing an Honors Major \
					 in Computer Science at the University of Michigan in \
					 Ann Arbor, MI. Outside of class, Jared is on the \
					 Central Planning Team of Dance Marathon at the \
					 University of Michigan and has a passion for impacting \
					 the world through technology.',
	'Sanaan Akhter': 'Sanaan Akhter is a sophomore persuing an Honors \
				     Major in computer science at Rutgers University \
				     in New Brunswick, NJ. He enjoys taking classes on \
				     everything STEM and, outside of the classroom, \
				     loves going to the gym and playing basketball with \
				     his friends.',
	'Sara Whitlock': 'Sanaan Akhter is a sophomore persuing an Honors \
					 Major in computer science at Rutgers University \
				     in New Brunswick, NJ. He enjoys taking classes on \
				     everything STEM and, outside of the classroom, \
				     loves going to the gym and playing basketball with \
				     his frien  ds.',
	'Chinmay Savanur': 'Chinmay Savanur is a sophomore persuing an Honors \
				   	 Major in computer science at Rutgers University \
				  	 in New Brunswick, NJ. He enjoys taking classes on \
				     everything STEM and, outside of the classroom, \
				  	 loves going to the gym and playing basketball with \
				  	 his friends.',
	'Nick Anderson': 'Nick Anderson is a sophomore persuing an Honors \
					 Major in computer science at Rutgers University \
				     in New Brunswick, NJ. He enjoys taking classes on \
				     everything STEM and, outside of the classroom, \
				     loves going to the gym and playing basketball with \
				     his frien  ds.',
	'Jared Glassband': 'Jared Glassband is a sophomore persuing an Honors \
				   	 Major in computer science at Rutgers University \
				  	 in New Brunswick, NJ. He enjoys taking classes on \
				     everything STEM and, outside of the classroom, \
				  	 loves going to the gym and playing basketball with \
				  	 his friends.'
}

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', teammembers=teammembers)

@app.route("/course/<string:title>")
def course(title):
	desc = courses[ title ].get("desc")
	author = courses[ title ].get("author")
	auth_desc = teammembers[ author ]
	playlists = courses[ title ].get("playlists")
	sizes = courses[ title ].get("sizes")
	return render_template('course.html', title=title, desc=desc, 
						   author=author, auth_desc=auth_desc, 
						   playlists=playlists, sizes=sizes)

@app.route("/soon/<string:title>")
def soon(title):
	return render_template('soon.html', title=title)

@app.route("/lesson/<string:title>/<string:lesson>/<string:current_vid>")
def lesson(title, lesson, current_vid):
	desc = courses[ title ].get("desc")
	playlists = courses[ title ].get("playlists")
	sizes = courses[ title ].get("sizes")
	course_lesson = title + " " + lesson
	return render_template('lesson.html', title=title, lesson=lesson,
						   course_lesson=course_lesson, video = current_vid, 
						   playlists=playlists, sizes=sizes)










