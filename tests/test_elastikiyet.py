import pytest
from modules.elastikiyet.elastikiyet_motor import ElastikiyetMotoru

def test_elastikiyet_yukle():
    motor = ElastikiyetMotoru()
    assert 'DEFAULT' in motor.elastikiyet_tablosu
    assert motor.elastikiyet_tablosu['DEFAULT']['elastikiyet'] > 0

def test_satis_tahmini():
    motor = ElastikiyetMotoru()
    tahmin = motor.satis_tahmini(
        mevcut_satis=100,
        mevcut_indirim=50,
        yeni_indirim=60,
        elastikiyet=3.5
    )
    
    assert tahmin['yeni_satis'] > 100
    assert tahmin['satis_artis'] > 0

def test_kategori_getir():
    motor = ElastikiyetMotoru()
    maskara = motor.kategori_getir('MASKARA')
    assert maskara['elastikiyet'] > 0
    assert maskara['optimal_indirim'] > 0
