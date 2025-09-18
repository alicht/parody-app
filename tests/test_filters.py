import pytest
from app.filters import is_tragedy


class TestIsTragedyFunction:
    
    def test_detects_deadly_keyword(self):
        assert is_tragedy("Deadly storm hits coast") is True
        assert is_tragedy("DEADLY virus spreads") is True
    
    def test_detects_attack_keyword(self):
        assert is_tragedy("Attack on embassy reported") is True
        assert is_tragedy("Cyber attack disrupts services") is True
    
    def test_detects_crash_keyword(self):
        assert is_tragedy("Plane crash in mountains") is True
        assert is_tragedy("Car crash blocks highway") is True
    
    def test_detects_explosion_keyword(self):
        assert is_tragedy("Explosion rocks downtown area") is True
        assert is_tragedy("Gas explosion in residential building") is True
    
    def test_detects_earthquake_keyword(self):
        assert is_tragedy("Earthquake strikes California") is True
        assert is_tragedy("Major earthquake predicted") is True
    
    def test_detects_flood_keyword(self):
        assert is_tragedy("Flood warnings issued") is True
        assert is_tragedy("Historic flooding continues") is True
    
    def test_detects_disaster_keyword(self):
        assert is_tragedy("Natural disaster declared") is True
        assert is_tragedy("Disaster relief efforts underway") is True
    
    def test_detects_massacre_keyword(self):
        assert is_tragedy("Massacre investigation continues") is True
        assert is_tragedy("Historic massacre remembered") is True
    
    def test_detects_tragedy_keyword(self):
        assert is_tragedy("Tragedy strikes small town") is True
        assert is_tragedy("Community mourns tragedy") is True
    
    def test_detects_shooting_keyword(self):
        assert is_tragedy("Shooting reported at mall") is True
        assert is_tragedy("Police investigate shooting") is True
    
    def test_case_insensitive_detection(self):
        assert is_tragedy("DEADLY Storm Approaches") is True
        assert is_tragedy("deadly storm approaches") is True
        assert is_tragedy("DeAdLy storm approaches") is True
    
    def test_keyword_within_larger_text(self):
        assert is_tragedy("Breaking: Deadly hurricane makes landfall in Florida") is True
        assert is_tragedy("Officials respond to massive earthquake in Japan") is True
    
    def test_returns_false_for_non_tragedy_headlines(self):
        assert is_tragedy("Stock market reaches new high") is False
        assert is_tragedy("Local team wins championship") is False
        assert is_tragedy("New restaurant opens downtown") is False
        assert is_tragedy("Technology company announces new product") is False
        assert is_tragedy("Weather forecast: Sunny skies ahead") is False
    
    def test_empty_string(self):
        assert is_tragedy("") is False
    
    def test_string_with_only_whitespace(self):
        assert is_tragedy("   ") is False
        assert is_tragedy("\n\t") is False
    
    def test_partial_keyword_matches_not_detected(self):
        assert is_tragedy("Attacking the problem head-on") is False
        assert is_tragedy("Crash course in programming") is False
        assert is_tragedy("Flooding the market with products") is False


def test_function_type_signature():
    """Test that the function has the correct type signature"""
    assert callable(is_tragedy)
    assert is_tragedy.__annotations__ == {'article_title': str, 'return': bool}