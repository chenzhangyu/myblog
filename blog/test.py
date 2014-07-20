[passageid, 
			[
				[userid, username, comment1, pubdate, 
														[[userid, username, originername, reply1, pubdate],..... ]
				], 
				[userid, username, comment1, pubdate, 
														[[userid, username, originername, reply1, pubdate],..... ]
				], ...........
			]
]



li = []
li.append(p.id)
coms = []
for x in p.comments:
	com = []
	com.append(x.user_id)	
    un = User.query.get(x.user_id).username
	com.append(un)
	com.append(x.content)
    ts = []
    for n in x.talks:
		t = []
	    t.append(n.user_id)
		t.append(User.query.get(n.user_id).username)
		t.append(un)
		t.append(n.content)
		t.append(n.pubdate)
		ts.append(t)
	com.append(ts)
	coms.append(com)
li.append(coms)
