from app.sentiment import local_analyze_feedback

def test_local_sentiment():
    result=local_analyze_feedback("The food was excellent but the waiting time was too long.")
    assert result["sentiment"]=="Mixed"
