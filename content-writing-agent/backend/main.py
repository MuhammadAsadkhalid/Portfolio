"""
Content Writing Assistant Agent - Flask Backend
Main server file that handles API requests and agent logic
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import traceback
from agents.content_agent import ContentWritingAgent

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize the Content Writing Agent
try:
    agent = ContentWritingAgent()
    print("✅ Content Writing Agent initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize agent: {e}")
    agent = None

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "Content Writing Assistant API is running!"
    }), 200


@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """
    Main endpoint to generate content
    
    Request body:
    {
        "topic": "string",
        "content_type": "blog|social|email|product",
        "writing_style": "formal|casual|technical|creative",
        "include_seo": boolean,
        "include_hashtags": boolean,
        "include_cta": boolean,
        "target_audience": "string"
    }
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['topic', 'content_type', 'writing_style']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate content_type
        valid_types = ['blog', 'social', 'email', 'product']
        if data['content_type'] not in valid_types:
            return jsonify({
                "error": f"Invalid content_type. Must be one of: {', '.join(valid_types)}"
            }), 400
        
        # Validate writing_style
        valid_styles = ['formal', 'casual', 'technical', 'creative']
        if data['writing_style'] not in valid_styles:
            return jsonify({
                "error": f"Invalid writing_style. Must be one of: {', '.join(valid_styles)}"
            }), 400
        
        # Check if agent is initialized
        if not agent:
            return jsonify({"error": "Agent not initialized. Check API key."}), 500
        
        # Call agent to generate content
        result = agent.generate_content(
            topic=data['topic'],
            content_type=data['content_type'],
            writing_style=data['writing_style'],
            include_seo=data.get('include_seo', True),
            include_hashtags=data.get('include_hashtags', True),
            include_cta=data.get('include_cta', True),
            target_audience=data.get('target_audience', 'General audience')
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error in generate_content: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": "Failed to generate content",
            "details": str(e)
        }), 500


@app.route('/api/analyze-content', methods=['POST'])
def analyze_content():
    """
    Analyze existing content for grammar, tone, readability
    
    Request body:
    {
        "content": "string",
        "analysis_type": "grammar|tone|readability|all"
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        if 'content' not in data or not data['content']:
            return jsonify({"error": "Missing required field: content"}), 400
        
        if not agent:
            return jsonify({"error": "Agent not initialized"}), 500
        
        analysis_type = data.get('analysis_type', 'all')
        result = agent.analyze_content(
            content=data['content'],
            analysis_type=analysis_type
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error in analyze_content: {str(e)}")
        return jsonify({
            "error": "Failed to analyze content",
            "details": str(e)
        }), 500


@app.route('/api/generate-variations', methods=['POST'])
def generate_variations():
    """
    Generate different variations of content
    
    Request body:
    {
        "content": "string",
        "num_variations": 3,
        "variation_type": "tone|length|audience"
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        if 'content' not in data:
            return jsonify({"error": "Missing required field: content"}), 400
        
        if not agent:
            return jsonify({"error": "Agent not initialized"}), 500
        
        num_variations = data.get('num_variations', 3)
        variation_type = data.get('variation_type', 'tone')
        
        result = agent.generate_variations(
            content=data['content'],
            num_variations=num_variations,
            variation_type=variation_type
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error in generate_variations: {str(e)}")
        return jsonify({
            "error": "Failed to generate variations",
            "details": str(e)
        }), 500


@app.route('/api/get-seo-suggestions', methods=['POST'])
def get_seo_suggestions():
    """
    Get SEO optimization suggestions
    
    Request body:
    {
        "title": "string",
        "content": "string",
        "target_keywords": ["keyword1", "keyword2"]
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        
        if not agent:
            return jsonify({"error": "Agent not initialized"}), 500
        
        result = agent.get_seo_suggestions(
            title=data.get('title', ''),
            content=data.get('content', ''),
            target_keywords=data.get('target_keywords', [])
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error in get_seo_suggestions: {str(e)}")
        return jsonify({
            "error": "Failed to get SEO suggestions",
            "details": str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    print("\n" + "="*60)
    print("🚀 Content Writing Assistant Agent - Starting Server")
    print("="*60)
    print(f"Port: {port}")
    print(f"Debug Mode: {debug}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)