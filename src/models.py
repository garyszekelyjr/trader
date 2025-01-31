from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Ticker(Base):
    __tablename__ = "ticker"

    ticker: Mapped[str] = mapped_column(unique=True)
    cik_str: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
