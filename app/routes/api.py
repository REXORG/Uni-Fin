from flask import Blueprint, current_app, jsonify, request
bp = Blueprint("api", __name__)

@bp.post("/user/profile")
def set_profile():
    payload = request.get_json(force=True)
    user_id = payload.get("user_id", "u_ozel")
    current_app.config["USER_PROFILES"][user_id] = payload
    return jsonify({"message": "profil kaydedildi", "user_id": user_id})

@bp.post("/test/submit")
def submit_test():
    payload = request.get_json(force=True)
    user_id = payload["user_id"]
    profile = current_app.config["USER_PROFILES"].get(user_id)
    if not profile:
        return jsonify({"error": "kullanıcı bulunamadı"}), 404
    profile["attention_score"] = payload.get("attention_score", profile.get("attention_score", 0.5))
    profile["motivation_score"] = payload.get("motivation_score", profile.get("motivation_score", 0.5))
    profile["response_time_ms"] = payload.get("response_time_ms", profile.get("response_time_ms", 700))
    return jsonify({"message": "bilişsel test kaydedildi"})

@bp.get("/recommendations")
def recommendations():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id zorunludur"}), 400
    system = current_app.config["SYSTEM"]
    profile = current_app.config["USER_PROFILES"].get(user_id)
    if not profile:
        return jsonify({"error": "kullanıcı bulunamadı"}), 404
    c_score = system["cognitive_filter"].cognitive_score(profile.get("attention_score", 0.5), profile.get("response_time_ms", 700), profile.get("motivation_score", 0.5))
    cap = system["cognitive_filter"].cognitive_capacity(c_score)
    recs = system["recommendation_engine"].recommend(profile, system["content_items"], cap, top_k=10)
    return jsonify({"cognitive_score": round(c_score, 4), "capacity": cap, "recommendations": recs})

@bp.post('/recommend/psychometric')
def recommend_psychometric():
    payload = request.get_json(force=True)
    user = payload.get('user', {})
    name = user.get('name', 'anonim')
    responses = user.get('responses', [])
    system = current_app.config['SYSTEM']
    try:
        scored = system['psychometric_service'].score(responses)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    result = system['ai_recommendation_service'].build_output(name, scored)
    return jsonify(result)
