"""
Content Writing Agent Logic
Handles all content generation and analysis using Gemini API
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from agents.prompts import PROMPTS
from agents.tools import (
    generate_seo_keywords,
    calculate_readability_score,
    extract_hashtags,
    generate_cta_phrases
)

load_dotenv()

class ContentWritingAgent:
    def __init__(self):
        """Initialize the Gemini API and setup agent"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file!")
        
        genai.configure(api_key=api_key)
        # Use a generally available Gemini model for text generation.
        # If you have access to a different model, you can change this string.
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        print("✅ Gemini API configured successfully!")
    
    def generate_content(self, topic, content_type, writing_style, 
                        include_seo=True, include_hashtags=True, 
                        include_cta=True, target_audience='General audience'):
        """
        Generate content based on parameters
        
        Args:
            topic: Main topic/subject
            content_type: 'blog', 'social', 'email', 'product'
            writing_style: 'formal', 'casual', 'technical', 'creative'
            include_seo: Whether to optimize for SEO
            include_hashtags: Whether to include hashtags
            include_cta: Whether to include call-to-action
            target_audience: Description of target audience
        
        Returns:
            Dictionary with generated content and metadata
        """
        try:
            # Get appropriate prompt template
            prompt_template = PROMPTS.get(f"{content_type}_{writing_style}")
            if not prompt_template:
                prompt_template = PROMPTS['default']
            
            # Build the prompt
            system_prompt = f"""
You are an expert content writer and digital marketing specialist. Your task is to create 
high-quality, engaging content that resonates with the target audience.

Target Audience: {target_audience}
Writing Style: {writing_style}
Content Type: {content_type}

Guidelines:
- Write compelling and original content
- Use appropriate tone for the style
- Include relevant keywords naturally
- Make content scannable with proper formatting
- Ensure engagement and call-to-action
- Keep grammar and spelling perfect
"""
            
            user_prompt = f"""
{prompt_template}

Topic: {topic}
Target Audience: {target_audience}

Please generate content that is:
1. Engaging and original
2. Properly formatted with markdown
3. SEO-friendly if applicable
4. Appropriate for {content_type}
5. Written in {writing_style} style
"""
            
            # Generate content using Gemini
            response = self.model.generate_content([
                system_prompt,
                user_prompt
            ])
            
            generated_content = response.text
            
            # Post-processing and analysis
            seo_keywords = generate_seo_keywords(topic) if include_seo else []
            readability_score = calculate_readability_score(generated_content)
            hashtags = extract_hashtags(topic) if include_hashtags else []
            cta_phrases = generate_cta_phrases() if include_cta else []
            
            # Build response
            result = {
                "success": True,
                "content": generated_content,
                "metadata": {
                    "content_type": content_type,
                    "writing_style": writing_style,
                    "target_audience": target_audience,
                    "word_count": len(generated_content.split()),
                    "character_count": len(generated_content),
                    "readability_score": readability_score,
                    "seo_keywords": seo_keywords,
                    "hashtags": hashtags,
                    "cta_suggestions": cta_phrases
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate content"
            }
    
    def analyze_content(self, content, analysis_type='all'):
        """
        Analyze content for grammar, tone, readability
        
        Args:
            content: Content to analyze
            analysis_type: 'grammar', 'tone', 'readability', 'all'
        
        Returns:
            Analysis results
        """
        try:
            prompt = f"""
Analyze the following content for {analysis_type}.

Content to analyze:
"{content}"

Please provide:
1. Grammar and spelling check
2. Tone analysis
3. Readability score (1-100)
4. Suggestions for improvement
5. Overall quality score (1-100)

Format your response as JSON with these fields:
{{
    "grammar_issues": ["issue1", "issue2"],
    "tone_analysis": "description of tone",
    "readability_score": number,
    "quality_score": number,
    "suggestions": ["suggestion1", "suggestion2"],
    "overall_assessment": "summary"
}}
"""
            
            response = self.model.generate_content(prompt)
            
            try:
                analysis = json.loads(response.text)
            except:
                analysis = {
                    "grammar_issues": [],
                    "tone_analysis": response.text,
                    "readability_score": calculate_readability_score(content),
                    "quality_score": 75,
                    "suggestions": [],
                    "overall_assessment": "Content analysis completed"
                }
            
            return {
                "success": True,
                "analysis": analysis
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to analyze content"
            }
    
    def generate_variations(self, content, num_variations=3, variation_type='tone'):
        """
        Generate different variations of content
        
        Args:
            content: Original content
            num_variations: Number of variations to generate
            variation_type: 'tone', 'length', 'audience'
        
        Returns:
            Multiple variations of the content
        """
        try:
            prompt = f"""
Generate {num_variations} different variations of the following content.

Original content:
"{content}"

Variation type: {variation_type}

For {variation_type} variation:
- If 'tone': Create versions with different tones (formal, casual, friendly, etc.)
- If 'length': Create short, medium, and long versions
- If 'audience': Create versions for different audiences

Return as a JSON array with 'variations' key containing a list of variations.
Each variation should be a complete, standalone piece of content.

Format:
{{
    "variations": [
        {{"variation": 1, "content": "..."}},
        {{"variation": 2, "content": "..."}},
        {{"variation": 3, "content": "..."}}
    ]
}}
"""
            
            response = self.model.generate_content(prompt)
            
            try:
                result = json.loads(response.text)
            except:
                result = {
                    "variations": [
                        {"variation": 1, "content": response.text}
                    ]
                }
            
            return {
                "success": True,
                "variations": result.get('variations', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate variations"
            }
    
    def get_seo_suggestions(self, title, content, target_keywords=None):
        """
        Get SEO optimization suggestions
        
        Args:
            title: Content title/meta title
            content: Main content
            target_keywords: List of keywords to target
        
        Returns:
            SEO suggestions and improvements
        """
        try:
            keywords_str = ', '.join(target_keywords) if target_keywords else 'auto-detect'
            
            prompt = f"""
Provide SEO optimization suggestions for this content.

Title: {title}

Content: {content[:1000]}...

Target keywords: {keywords_str}

Analyze and provide:
1. SEO score (1-100)
2. Keyword optimization
3. Meta description suggestion
4. Heading optimization
5. Internal linking suggestions
6. Image alt text suggestions
7. Overall recommendations

Format as JSON:
{{
    "seo_score": number,
    "keyword_optimization": {{}},
    "meta_description": "string",
    "heading_optimization": ["suggestion1"],
    "internal_links": ["suggestion1"],
    "image_alt_text": ["suggestion1"],
    "recommendations": ["recommendation1"]
}}
"""
            
            response = self.model.generate_content(prompt)
            
            try:
                suggestions = json.loads(response.text)
            except:
                suggestions = {
                    "seo_score": 75,
                    "meta_description": "Your content here - optimize for SEO",
                    "recommendations": [response.text]
                }
            
            return {
                "success": True,
                "seo_suggestions": suggestions
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to get SEO suggestions"
            }