# Psikolojik AI Öneri Motoru

Bu backend, 100 soruluk psikometrik yanıtları (Big Five + MBTI + davranış) işleyip vektör tabanlı gerçek dünya içerik önerileri üretir.

## Yeni Uç Nokta
- `POST /recommend/psychometric`

### Girdi
```json
{
  "user": {
    "name": "Ayşe",
    "responses": [1,2,3,4,5, ... toplam 100 değer]
  }
}
```

### Çıktı
- Sadece JSON döner.
- `summary.big_five`, `summary.mbti`, `summary.traits`
- `recommendations` altında `books/films/music/education/careers/habits`
- Her öneri gerçek dünya başlıklarından seçilir ve cosine similarity skoruna göre sıralanır.

## Notlar
- Kullanıcı vektörü: `[openness, structure, focus, empathy, social_energy, conscientiousness, extraversion, neuroticism]`
- Veri kaynağı: `app/data/real_world_catalog.json` (gerçek bilinen eserler)

## Dataset Sistemi (FAISS Uyumlu)
`dataset/` klasörü üretime hazır başlangıç verisi içerir:
- `books.json` (200)
- `films.json` (200)
- `music.json` (200)
- `courses.json` (200)
- `habits.json` (200)
- `careers.json` (200)

Toplam: 1200 kayıt.
Tüm kayıtlar aynı şemayı kullanır ve 8 boyutlu (0-1) vektör taşır.
