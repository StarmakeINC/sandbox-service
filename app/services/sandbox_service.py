from sqlalchemy.orm import Session
from ..models import Scenario
from ..schemas import ScenarioCreate

class Sandbox:
    @classmethod
    def create_scenario(cls, db: Session, user_id: int, scenario_data: ScenarioCreate):
        scenario = Scenario(user_id=user_id, text=scenario_data.text, temp_id=scenario_data.temp_id)
        db.add(scenario)
        db.commit()
        db.refresh(scenario)
        return scenario

    @classmethod
    def get_scenarios_by_user(cls, db: Session, user_id: int):
        return db.query(Scenario).filter(Scenario.user_id == user_id).all()

    @classmethod
    def get_last_script(cls, db: Session, user_id: int):
        last_script = (
            db.query(Scenario).filter(Scenario.user_id == user_id).order_by(Scenario.id.desc()).limit(1).first()
        )
        if last_script:
            return {"text": last_script.text}
        return {"text": "У вас нет сохраненных сценариев."}