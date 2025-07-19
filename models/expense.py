


from sqlalchemy import Column, Integer, String, Float, Date
from db.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<Expense id={self.id} "
            f"date={self.date} "
            f"category={self.category!r} "
            f"amount={self.amount}>"
        )

    def __str__(self) -> str:
        desc = f" • {self.description}" if self.description else ""
        return f"{self.date} | {self.category} | {self.amount:.2f}{desc}"