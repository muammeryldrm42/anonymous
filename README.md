# Football Manager (Prototype)

Bu depo, konuştuğumuz futbol menajer oyununun **ilk prototip altyapısını** içerir. Şu an temel bir
oyun çekirdeği, basit maç simülasyonu ve CLI giriş noktası vardır. Amaç, hızlıca oynanabilir bir
iskelet oluşturup adım adım genişletmektir.

## Özellikler (v0)
- Takım, oyuncu ve menajer modelleri
- Basit maç simülasyonu
- Lig formatında fikstür ve puan tablosu
- Komut satırından tek sezon simülasyonu

## Çalıştırma
```bash
python -m football_manager.cli
```

## Klasör Yapısı
```
src/football_manager/
  __init__.py
  models.py
  engine.py
  cli.py
```

## Sonraki Adımlar (Öneri)
- Çoklu dil (localization) altyapısı
- Transfer pazarı ve sözleşmeler
- Finans ve kulüp yönetimi
- Gelişmiş maç motoru
