"""
Prompt templates for different content types and writing styles
Used by the content agent to guide Gemini API responses
"""

PROMPTS = {
    # BLOG POSTS
    'blog_formal': """
Create a professional blog post about the given topic. 

Structure:
1. Engaging headline (H1)
2. Brief introduction (2-3 sentences)
3. Table of contents (if long)
4. Main sections with H2/H3 headings
5. Key points and insights
6. Conclusion
7. Call-to-action

Style: Professional, informative, data-backed
Length: 1000-1500 words
Include: Statistics, examples, actionable insights
""",
    
    'blog_casual': """
Write a conversational, engaging blog post about the topic.

Structure:
1. Catchy headline
2. Personal introduction
3. Main points with relatable examples
4. Engaging stories or anecdotes
5. Practical tips
6. Conclusion with personal touch
7. Call-to-action

Style: Friendly, conversational, relatable
Length: 800-1200 words
Include: Personal experiences, humor, real examples
""",
    
    'blog_technical': """
Write a technical blog post with detailed explanations.

Structure:
1. Technical headline
2. Problem statement
3. Solution overview
4. Step-by-step explanation
5. Code examples or technical details
6. Best practices
7. Conclusion
8. Further reading

Style: Technical, detailed, precise
Length: 1200-1800 words
Include: Technical details, examples, code snippets
""",
    
    'blog_creative': """
Write a creative, visually descriptive blog post.

Structure:
1. Compelling hook
2. Narrative introduction
3. Descriptive sections
4. Engaging examples
5. Insights and lessons
6. Creative conclusion
7. Inspiration call-to-action

Style: Creative, descriptive, engaging
Length: 900-1300 words
Include: Vivid descriptions, storytelling, emotional connection
""",
    
    # SOCIAL MEDIA
    'social_formal': """
Create a professional social media post about the topic.

Format:
- Clear and concise message
- Professional tone
- Relevant hashtags
- Call-to-action
- Suitable for LinkedIn/corporate accounts

Length: 150-280 characters
Include: Professional tone, industry insights, engagement CTA
""",
    
    'social_casual': """
Create an engaging, casual social media post.

Format:
- Fun and relatable message
- Conversational tone
- Popular hashtags
- Emoji usage (appropriate)
- Engagement-focused

Length: 100-250 characters
Include: Conversational tone, humor, trending hashtags, emojis
""",
    
    'social_technical': """
Create a technical social media post (for developers/tech audience).

Format:
- Code insight or technical tip
- Technical terminology
- Developer community hashtags
- Link to resources
- Problem-solution focus

Length: 150-280 characters
Include: Technical insight, code reference, #hashtags, resources
""",
    
    'social_creative': """
Create a creative, visually inspiring social media post.

Format:
- Inspiring message
- Vivid language
- Aesthetic appeal
- Storytelling element
- Motivational tone

Length: 100-250 characters
Include: Inspiring tone, descriptive language, creative hashtags
""",
    
    # EMAIL CAMPAIGNS
    'email_formal': """
Write a professional email campaign about the topic.

Structure:
1. Professional subject line
2. Greeting
3. Main message (value proposition)
4. Benefits and features
5. Call-to-action
6. Professional closing
7. Signature

Tone: Professional, persuasive, value-focused
Length: 200-400 words
Include: Clear benefits, professional tone, strong CTA
""",
    
    'email_casual': """
Write a friendly, engaging email campaign.

Structure:
1. Catchy subject line
2. Warm greeting
3. Relatable introduction
4. Main benefits
5. Social proof if applicable
6. Friendly call-to-action
7. Warm closing

Tone: Friendly, personable, conversational
Length: 150-350 words
Include: Personal touch, conversational tone, warm engagement
""",
    
    'email_technical': """
Write a technical email campaign for a technical audience.

Structure:
1. Clear subject line (technical)
2. Technical introduction
3. Problem explanation
4. Solution details
5. Technical specifications
6. Documentation links
7. Technical support CTA

Tone: Technical, detailed, solution-focused
Length: 250-450 words
Include: Technical details, solutions, documentation links
""",
    
    'email_creative': """
Write a creative, engaging email campaign.

Structure:
1. Compelling subject line
2. Engaging opening
3. Narrative or story element
4. Value proposition
5. Emotional connection
6. Creative call-to-action
7. Memorable closing

Tone: Creative, engaging, memorable
Length: 180-380 words
Include: Storytelling, emotional appeal, creative messaging
""",
    
    # PRODUCT DESCRIPTIONS
    'product_formal': """
Write a professional product description.

Structure:
1. Product name and headline
2. What it is
3. Key features
4. Benefits
5. Specifications
6. Use cases
7. Call-to-action

Tone: Professional, informative, persuasive
Include: Features, benefits, specifications, professional tone
""",
    
    'product_casual': """
Write a friendly, engaging product description.

Structure:
1. Catchy product headline
2. What makes it special
3. Key features (bullet points)
4. Benefits (relatable)
5. Why customers love it
6. Quick specs
7. Call-to-action

Tone: Friendly, relatable, enthusiastic
Include: Benefits, customer appeal, enthusiasm, engagement
""",
    
    'product_technical': """
Write a detailed technical product description.

Structure:
1. Product name
2. Technical overview
3. Technical specifications
4. Features (detailed)
5. Performance metrics
6. Compatibility
7. Documentation/Support
8. Call-to-action

Tone: Technical, detailed, specifications-focused
Include: Tech specs, features, compatibility, performance
""",
    
    'product_creative': """
Write a creative, visually appealing product description.

Structure:
1. Compelling headline
2. Emotional hook
3. Descriptive features
4. Benefits (lifestyle)
5. Unique selling points
6. Inspirational message
7. Call-to-action

Tone: Creative, inspiring, lifestyle-focused
Include: Vivid descriptions, lifestyle appeal, emotional connection
""",
    
    # DEFAULT FALLBACK
    'default': """
Create original, high-quality content about the given topic.
Use appropriate formatting and structure.
Ensure engagement and clarity.
Include relevant details and insights.
"""
}

# Content type descriptions for frontend
CONTENT_TYPES = {
    'blog': 'Long-form blog posts with detailed insights',
    'social': 'Social media posts (Twitter, LinkedIn, Instagram)',
    'email': 'Email campaigns and newsletters',
    'product': 'Product descriptions and marketing copy'
}

# Writing style descriptions for frontend
WRITING_STYLES = {
    'formal': 'Professional and corporate tone',
    'casual': 'Friendly and conversational tone',
    'technical': 'Detailed and technical tone',
    'creative': 'Imaginative and descriptive tone'
}