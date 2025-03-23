import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import json
import re
import math
from datetime import datetime, timedelta

class AIInfluenceRater:
    def __init__(self):
        # Initialize a simple model for influence prediction
        # In a real implementation, this would be trained on historical data
        self.influence_model = RandomForestRegressor(n_estimators=100, random_state=42)
        
        # Mock training data
        self._train_model()
        
    def _train_model(self):
        # Mock training data - in a real implementation, this would be actual historical data
        # Features: [credibility_score, years_active, engagement_rate, controversy_count, sentiment_score]
        X_train = np.array([
            [85, 12, 0.08, 1, 0.8],
            [40, 0.5, 0.15, 3, 0.6],
            [90, 8, 0.05, 0, 0.9],
            [60, 3, 0.12, 2, 0.5],
            [70, 5, 0.07, 1, 0.7],
            [78, 6, 0.06, 2, 0.75],
            [45, 1, 0.18, 4, 0.45],
            [88, 10, 0.04, 0, 0.92]
        ])
        
        # Target: overall influence score
        y_train = np.array([82, 55, 78, 63, 72, 76, 51, 84])
        
        # Train the model
        self.influence_model.fit(X_train, y_train)
    
    def _calculate_credibility_score(self, profile):
        """
        Calculate credibility score based on credentials, citations, and public trust
        """
        # Base credibility factors
        credential_score = profile.get('credential_score', 50)
        citation_score = profile.get('citation_score', 50)
        
        # Controversies reduce credibility
        controversy_count = profile.get('controversy_incidents', 0)
        controversy_penalty = min(controversy_count * 5, 30)
        
        # Check verification status
        verification_bonus = 10 if profile.get('verified', False) else 0
        
        # Calculate final score
        raw_score = credential_score * 0.4 + citation_score * 0.4 + verification_bonus - controversy_penalty
        return max(min(raw_score, 100), 0)
    
    def _calculate_longevity_score(self, profile):
        """
        Calculate longevity score based on years active and consistency
        """
        years_active = profile.get('years_active', 1)
        
        # Logarithmic scaling to reward long-term presence
        longevity_base = min(math.log(max(years_active, 0.5) + 1, 2) * 20, 80)
        
        # Consistency bonus
        consistency_score = profile.get('consistency_score', 50)
        consistency_factor = consistency_score * 0.2
        
        return longevity_base + consistency_factor
    
    def _calculate_engagement_score(self, profile):
        """
        Calculate engagement score based on metrics and quality
        """
        engagement_rate = profile.get('engagement_rate', 0.05)
        meaningful_ratio = profile.get('meaningful_engagement_ratio', 0.5)
        
        # Calculate score (engagement rates are typically small decimals)
        rate_score = min(engagement_rate * 500, 70)
        quality_score = meaningful_ratio * 30
        
        return rate_score + quality_score
    
    def _analyze_content_sentiment(self, profile):
        """
        Analyze sentiment score (simulated)
        """
        # In a real implementation, this would use NLP on content and comments
        return profile.get('sentiment_score', 0.7) * 100
    
    def _detect_artificial_engagement(self, profile):
        """
        Detect potentially fake engagement patterns (simulated)
        """
        # In a real implementation, this would analyze patterns in data
        follower_volatility = profile.get('follower_volatility', 0.1)
        engagement_consistency = profile.get('engagement_consistency', 0.2)
        
        # Calculate risk score (lower is better)
        risk_score = follower_volatility * 0.5 + engagement_consistency * 0.5
        
        # Convert to authenticity score (higher is better)
        return (1 - min(risk_score, 1)) * 100
    
    def calculate_influence_score(self, profile):
        """
        Calculate comprehensive influence score
        """
        # Calculate base scores
        credibility = self._calculate_credibility_score(profile)
        longevity = self._calculate_longevity_score(profile)
        engagement = self._calculate_engagement_score(profile)
        
        # AI analysis scores
        sentiment = self._analyze_content_sentiment(profile)
        authenticity = self._detect_artificial_engagement(profile)
        
        # Use the model for prediction with advanced features
        features = np.array([[
            credibility,
            profile.get('years_active', 1),
            profile.get('engagement_rate', 0.05),
            profile.get('controversy_incidents', 0),
            sentiment / 100  # Normalize to 0-1
        ]])
        
        # Get base prediction from model
        predicted_score = self.influence_model.predict(features)[0]
        
        # Adjust based on authenticity
        authenticity_factor = authenticity / 100
        adjusted_score = predicted_score * (0.8 + 0.2 * authenticity_factor)
        
        # Return all component scores
        return {
            "overall": round(adjusted_score, 1),
            "credibility": round(credibility, 1),
            "longevity": round(longevity, 1),
            "engagement": round(engagement, 1),
            "sentiment": round(sentiment, 1),
            "authenticity": round(authenticity, 1)
        }

    def rate_influencers(self, profiles):
        """
        Process multiple influencer profiles
        """
        results = []
        for profile in profiles:
            scores = self.calculate_influence_score(profile)
            
            # Add to results
            results.append({
                "id": profile.get("id", 0),
                "name": profile.get("name", "Unknown"),
                "image_url": profile.get("image_url", ""),
                "category": profile.get("category", "General"),
                "bio": profile.get("bio", ""),
                "scores": scores,
                # Pass through additional data needed for visualization
                "monthly_data": profile.get("monthly_data", {}),
                "content_quality": profile.get("content_quality", {}),
                "platform_presence": profile.get("platform_presence", {})
            })
        
        # Sort by overall score
        results.sort(key=lambda x: x["scores"]["overall"], reverse=True)
        return results

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_profiles = [
        {
            "id": 1,
            "name": "Tech Visionary",
            "category": "Technology",
            "credential_score": 85,
            "citation_score": 80,
            "years_active": 12,
            "consistency_score": 75,
            "engagement_rate": 0.08,
            "meaningful_engagement_ratio": 0.7,
            "controversy_incidents": 1,
            "verified": True,
            "sentiment_score": 0.85,
            "follower_volatility": 0.1,
            "engagement_consistency": 0.1
        },
        {
            "id": 2,
            "name": "Viral Creator",
            "category": "Entertainment",
            "credential_score": 40,
            "citation_score": 35,
            "years_active": 0.5,
            "consistency_score": 30,
            "engagement_rate": 0.18,
            "meaningful_engagement_ratio": 0.4,
            "controversy_incidents": 3,
            "verified": False,
            "sentiment_score": 0.65,
            "follower_volatility": 0.8,
            "engagement_consistency": 0.3
        }
    ]
    
    rater = AIInfluenceRater()
    results = rater.rate_influencers(sample_profiles)
    print(json.dumps(results, indent=2))