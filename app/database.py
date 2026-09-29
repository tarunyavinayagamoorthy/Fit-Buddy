from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(String(20), nullable=False)
    goal = Column(String(100), nullable=False)
    intensity = Column(String(20), nullable=False)


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)

    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)

    nutrition_tip = Column(Text, nullable=True)

    feedback = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def save_user(
    db,
    user_id,
    username,
    age,
    weight,
    goal,
    intensity
):
    user = User(
        user_id=user_id,
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def save_plan(
    db,
    user_id,
    original_plan,
    nutrition_tip
):
    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return plan


def get_user(db, user_id):
    return db.query(User).filter(
        User.user_id == user_id
    ).first()


def get_original_plan(db, user_id):
    plan = db.query(Plan).filter(
        Plan.user_id == user_id
    ).first()

    if plan:
        return plan.original_plan

    return None


def update_plan(
    db,
    user_id,
    updated_plan,
    feedback
):
    plan = db.query(Plan).filter(
        Plan.user_id == user_id
    ).first()

    if plan:
        plan.updated_plan = updated_plan
        plan.feedback = feedback

        db.commit()
        db.refresh(plan)

    return plan


def get_plan(db, user_id):
    return db.query(Plan).filter(
        Plan.user_id == user_id
    ).first()


def get_all_users(db):
    return db.query(User).all()


def get_all_plans(db):
    return db.query(Plan).all()