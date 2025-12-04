from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class ScientificArticle(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text)
    arxiv_id: Mapped[str] = mapped_column(String(100))
    file_path: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)

    # 💥 RELATION CORRIGÉE
    author: Mapped["Author"] = relationship(back_populates="article", uselist=False)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))

    # 💥 RELATION CORRIGÉE
    article: Mapped[ScientificArticle] = relationship(back_populates="author")
