class Payment:
    def __init__(self, payment_id, amount, comment):
        self.id = payment_id
        self.amount = amount
        self.comment = comment

    def __repr__(self):
        return f"( [ID{self.id}] amount: [{self.amount}] comment: [{self.comment}] )"
