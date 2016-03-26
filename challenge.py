class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.String(80))
    user2 = db.Column(db.String(80))
    start = db.Column(db.DateTime)

    def __init__(self, u1, u2, start):
        self.user1 = u1
        self.user2 = u2
        self.start = start

    def __repr__(self):
        return '<(%r and %r) at %r>' % (self.user1, self.user2, self.start)

