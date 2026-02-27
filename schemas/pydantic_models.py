from pydantic import BaseModel, Field
from typing import List

class HeroSection(BaseModel):
    headline: str = Field(description="Main headline of the landing page")
    subheadline: str = Field(description="Supporting text below the headline")
    cta_button_text: str = Field(description="Call to action button label e.g. Get Started")

class FeatureItem(BaseModel):
    title: str = Field(description="Feature title")
    description: str = Field(description="One sentence describing the feature")

class WireframeAndCopy(BaseModel):
    brand_name: str = Field(description="The name of the business or product")
    color_theme: str = Field(description="Tailwind color e.g. blue, green, rose, purple")
    hero: HeroSection
    features: List[FeatureItem] = Field(description="List of 3 features", min_length=3, max_length=3)
    testimonial_quote: str = Field(description="A short customer testimonial quote")
    testimonial_author: str = Field(description="Name and title of the testimonial author")