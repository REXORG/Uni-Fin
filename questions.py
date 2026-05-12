"""Question bank definitions for composite psychometric testing."""

from __future__ import annotations

from typing import Dict, List

LIKERT_OPTIONS = [
    {"value": 1, "label": "Kesinlikle Katılmıyorum"},
    {"value": 2, "label": "Katılmıyorum"},
    {"value": 3, "label": "Kararsızım"},
    {"value": 4, "label": "Katılıyorum"},
    {"value": 5, "label": "Kesinlikle Katılıyorum"},
]

BIG_FIVE_QUESTIONS: List[Dict] = [
    {"id": f"bf_{i}", "type": "big_five", "text": text, "trait": trait, "reverse": reverse, "options": LIKERT_OPTIONS}
    for i, (text, trait, reverse) in enumerate([
        ("Kalabalık ortamlarda enerji kazanırım.", "extraversion", False),
        ("Günlük planlarımı düzenli tutarım.", "conscientiousness", False),
        ("Yeni fikirlere karşı meraklıyımdır.", "openness", False),
        ("Başkalarının duygularını kolayca anlarım.", "agreeableness", False),
        ("Stres altında çabuk gerilirim.", "neuroticism", False),
        ("Yalnız kalmayı sosyal ortamlara tercih ederim.", "extraversion", True),
        ("Sorumluluklarımı son dakikaya bırakırım.", "conscientiousness", True),
        ("Soyut fikirlerle vakit geçirmekten hoşlanırım.", "openness", False),
        ("Tartışmalarda uzlaşmaya önem veririm.", "agreeableness", False),
        ("Küçük aksilikler bile beni uzun süre etkiler.", "neuroticism", False),
    ] * 5, start=1)
][:50]

MBTI_QUESTIONS: List[Dict] = [
    {"id": f"mbti_{i}", "type": "mbti", "text": text, "dimension": dim, "direction": direction, "options": LIKERT_OPTIONS}
    for i, (text, dim, direction) in enumerate([
        ("Yeni insanlarla tanışmak bana enerji verir.", "EI", "E"),
        ("Gerçekçi detaylara soyut fikirlerden daha çok güvenirim.", "SN", "S"),
        ("Karar verirken mantığı duyguların önüne koyarım.", "TF", "T"),
        ("Planlı hareket etmeyi spontane olmaya tercih ederim.", "JP", "J"),
        ("Uzun süre yalnız çalışmak beni yormaz.", "EI", "I"),
        ("Büyük resmi ayrıntılardan önce görürüm.", "SN", "N"),
        ("İnsan ilişkilerinde empatiyi mantığın önünde tutarım.", "TF", "F"),
        ("Açık uçlu seçenekler sabit planlardan daha rahattır.", "JP", "P"),
        ("Toplantılarda konuşmayı dinlemekten daha çok severim.", "EI", "E"),
        ("Somut kanıt olmadan karar almam.", "SN", "S"),
    ] * 2, start=1)
][:20]
