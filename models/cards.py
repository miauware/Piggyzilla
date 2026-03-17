from extensions import db


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # NOTE: 'debit','credit' or 'all'
    limit = db.Column(db.Integer)


def create_cards():
    if Cards.query.first() is None:  # INFO: table is empty
        db.session.add(Cards(name="Nubank", type="all", limit="300"))
        db.session.add(Cards(name="Picpay", type="all", limit="500"))
        db.session.add(Cards(name="Itau", type="all", limit="300"))
        db.session.add(Cards(name="Caixa", type="all", limit="300"))
        db.session.add(Cards(name="Bradesco", type="all", limit="300"))
        db.session.commit()
        print("Cards list created.")
