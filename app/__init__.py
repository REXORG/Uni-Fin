from flask import Flask

from .routes.api import bp as api_bp
from .services.cognitive_filter import CognitiveFilter
from .services.data_service import load_content, load_users
from .services.ml_service import MLCompatibilityModel
from .services.recommendation_engine import RecommendationEngine
from .services.vectorization_service import VectorizationService
from .services.psychometric_service import PsychometricService
from .services.ai_recommendation_service import AIRecommendationService
from .services.test_engine import CompositeTestEngine
from .utils.logger import configure_logging


def create_app() -> Flask:
    configure_logging()
    app = Flask(__name__)

    content_items = load_content()
    users = load_users()

    vectorizer = VectorizationService()
    ml_model = MLCompatibilityModel(vectorizer)
    ml_model.train(users, content_items)

    recommender = RecommendationEngine(vectorizer, ml_model)

    app.config["USER_PROFILES"] = {u["user_id"]: u for u in users}
    app.config["SYSTEM"] = {
        "content_items": content_items,
        "cognitive_filter": CognitiveFilter(),
        "recommendation_engine": recommender,
        "psychometric_service": PsychometricService(),
        "ai_recommendation_service": AIRecommendationService(),
        "composite_test_engine": CompositeTestEngine(PsychometricService()),
    }

    app.register_blueprint(api_bp)
    return app
