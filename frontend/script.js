// ============================================================================
// Content Writing Assistant - Frontend JavaScript
// ============================================================================

// Configuration
// Prefer same-origin backend in production; fall back to env override or localhost for local dev.
const apiFromOrigin = window.location.origin.startsWith('file')
    ? null
    : `${window.location.origin.replace(/\/$/, '')}/api`;

const API_BASE_URL =
    window.API_BASE_URL ||
    apiFromOrigin ||
    'http://localhost:5000/api';
let currentContent = '';
let currentMetadata = null;

// ============================================================================
// API CALLS
// ============================================================================

async function generateContent() {
    const topic = document.getElementById('topic').value.trim();
    const contentType = document.getElementById('contentType').value;
    const writingStyle = document.getElementById('writingStyle').value;
    const targetAudience = document.getElementById('targetAudience').value.trim();
    const includeSEO = document.getElementById('includeSEO').checked;
    const includeHashtags = document.getElementById('includeHashtags').checked;
    const includeCTA = document.getElementById('includeCTA').checked;

    // Validation
    if (!topic) {
        showError('Please enter a topic');
        return;
    }
    if (!contentType) {
        showError('Please select a content type');
        return;
    }
    if (!writingStyle) {
        showError('Please select a writing style');
        return;
    }

    // Show loading state
    showLoading();

    try {
        const response = await axios.post(`${API_BASE_URL}/generate-content`, {
            topic,
            content_type: contentType,
            writing_style: writingStyle,
            target_audience: targetAudience,
            include_seo: includeSEO,
            include_hashtags: includeHashtags,
            include_cta: includeCTA
        });

        if (response.data.success) {
            currentContent = response.data.content;
            currentMetadata = response.data.metadata;
            
            displayContent(currentContent, currentMetadata);
            showSuccess('Content generated successfully!');
        } else {
            showError(response.data.error || 'Failed to generate content');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.response?.data?.details || 'Error generating content. Make sure backend is running on http://localhost:5000');
    }
}

async function analyzeContent() {
    if (!currentContent) {
        showError('Please generate content first');
        return;
    }

    showLoading();

    try {
        const response = await axios.post(`${API_BASE_URL}/analyze-content`, {
            content: currentContent,
            analysis_type: 'all'
        });

        if (response.data.success) {
            displayAnalysis(response.data.analysis);
            showSuccess('Analysis complete!');
        } else {
            showError('Analysis failed');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error analyzing content');
    }
}

async function generateVariations() {
    if (!currentContent) {
        showError('Please generate content first');
        return;
    }

    showLoading();

    try {
        const response = await axios.post(`${API_BASE_URL}/generate-variations`, {
            content: currentContent,
            num_variations: 3,
            variation_type: 'tone'
        });

        if (response.data.success) {
            displayVariations(response.data.variations);
            showSuccess('Variations generated!');
        } else {
            showError('Failed to generate variations');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error generating variations');
    }
}

async function getSEOSuggestions() {
    if (!currentContent) {
        showError('Please generate content first');
        return;
    }

    const topic = document.getElementById('topic').value;
    showLoading();

    try {
        const response = await axios.post(`${API_BASE_URL}/get-seo-suggestions`, {
            title: topic,
            content: currentContent,
            target_keywords: []
        });

        if (response.data.success) {
            displaySEOSuggestions(response.data.seo_suggestions);
            showSuccess('SEO suggestions generated!');
        } else {
            showError('Failed to get SEO suggestions');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error getting SEO suggestions');
    }
}

// ============================================================================
// DISPLAY FUNCTIONS
// ============================================================================

function displayContent(content, metadata) {
    const container = document.getElementById('outputContainer');
    const actionButtons = document.getElementById('actionButtons');
    const metadataContainer = document.getElementById('metadataContainer');

    // Format and display content
    const formattedContent = markdownToHTML(content);
    
    container.innerHTML = `
        <div class="fade-in">
            <h3 class="text-2xl font-bold gradient-text mb-4">
                <i class="fas fa-star"></i> Generated Content
            </h3>
            <div class="content-output rounded-lg p-6 prose prose-sm max-w-none">
                ${formattedContent}
            </div>
        </div>
    `;

    // Show action buttons
    actionButtons.classList.remove('hidden');

    // Display metadata
    if (metadata) {
        displayMetadata(metadata);
    }

    // Scroll to output
    container.scrollIntoView({ behavior: 'smooth' });
}

function displayMetadata(metadata) {
    const container = document.getElementById('metadataContainer');
    const content = document.getElementById('metadataContent');

    let html = '';

    if (metadata.word_count) {
        html += `<div class="flex justify-between items-center">
            <span class="text-gray-600">📝 Word Count:</span>
            <strong>${metadata.word_count}</strong>
        </div>`;
    }

    if (metadata.readability_score !== undefined) {
        html += `<div class="flex justify-between items-center">
            <span class="text-gray-600">📊 Readability Score:</span>
            <strong>${Math.round(metadata.readability_score)}/100</strong>
        </div>`;
    }

    if (metadata.seo_keywords && metadata.seo_keywords.length > 0) {
        html += `<div>
            <span class="text-gray-600">🔍 SEO Keywords:</span>
            <div class="flex flex-wrap gap-2 mt-2">
                ${metadata.seo_keywords.map(kw => `<span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">${kw}</span>`).join('')}
            </div>
        </div>`;
    }

    if (metadata.hashtags && metadata.hashtags.length > 0) {
        html += `<div>
            <span class="text-gray-600">#️⃣ Hashtags:</span>
            <div class="flex flex-wrap gap-2 mt-2">
                ${metadata.hashtags.map(tag => `<span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">${tag}</span>`).join('')}
            </div>
        </div>`;
    }

    if (metadata.cta_suggestions && metadata.cta_suggestions.length > 0) {
        html += `<div>
            <span class="text-gray-600">🎯 CTA Suggestions:</span>
            <div class="flex flex-wrap gap-2 mt-2">
                ${metadata.cta_suggestions.slice(0, 3).map(cta => `<span class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">${cta}</span>`).join('')}
            </div>
        </div>`;
    }

    content.innerHTML = html || '<p class="text-gray-500">No metadata available</p>';
    container.classList.remove('hidden');
}

function displayAnalysis(analysis) {
    const container = document.getElementById('outputContainer');

    // Normalize in case backend sends a JSON string blob
    const normalizeAnalysis = (raw) => {
        const clean = (text = '') => text.replace(/```[a-zA-Z]*\n?/g, '').replace(/```/g, '').trim();
        if (typeof raw === 'string') {
            try {
                raw = JSON.parse(clean(raw));
            } catch (_) {
                return { tone_analysis: clean(raw) };
            }
        }
        // Ensure shapes
        return {
            grammar_issues: raw.grammar_issues || [],
            tone_analysis: clean(raw.tone_analysis || raw.tone || ''),
            readability_score: Number(raw.readability_score ?? raw.readability ?? 0),
            quality_score: Number(raw.quality_score ?? 0),
            suggestions: raw.suggestions || [],
            overall_assessment: clean(raw.overall_assessment || '')
        };
    };

    const a = normalizeAnalysis(analysis || {});

    let html = `
        <div class="fade-in">
            <h3 class="text-2xl font-bold gradient-text mb-4 flex items-center gap-2">
                <i class="fas fa-microscope"></i> Content Analysis
            </h3>
            <div class="space-y-4">
    `;

    if (a.quality_score) {
        html += `
            <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-800">Quality Score</span>
                    <span class="text-2xl font-bold gradient-text">${a.quality_score}/100</span>
                </div>
                <div class="w-full bg-slate-200 rounded-full h-2 mt-3 overflow-hidden">
                    <div class="bg-gradient-to-r from-blue-500 to-emerald-500 h-2 rounded-full" style="width: ${a.quality_score}%"></div>
                </div>
            </div>
        `;
    }

    if (a.readability_score) {
        html += `
            <div class="bg-sky-50 rounded-xl p-4 border border-sky-100">
                <div class="flex justify-between items-center">
                    <span class="font-semibold text-slate-800">📖 Readability</span>
                    <span class="font-bold text-sky-700">${a.readability_score}/100</span>
                </div>
            </div>
        `;
    }

    if (a.tone_analysis) {
        html += `
            <div class="bg-amber-50 rounded-xl p-4 border border-amber-100">
                <span class="font-semibold text-slate-800">Tone</span>
                <p class="text-slate-700 mt-2 leading-relaxed whitespace-pre-line">${a.tone_analysis}</p>
            </div>
        `;
    }

    if (a.grammar_issues && a.grammar_issues.length > 0) {
        html += `
            <div class="bg-rose-50 rounded-xl p-4 border border-rose-100">
                <span class="font-semibold text-slate-800">✏️ Grammar Issues</span>
                <ul class="list-disc list-inside mt-2 space-y-1 text-slate-700">
                    ${a.grammar_issues.map(g => `<li>${g}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    if (a.suggestions && a.suggestions.length > 0) {
        html += `
            <div class="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                <span class="font-semibold text-slate-800">💡 Suggestions</span>
                <ul class="list-disc list-inside mt-2 space-y-1 text-slate-700">
                    ${a.suggestions.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    html += '</div></div>';
    container.innerHTML = html;
}

function displayVariations(variations) {
    const container = document.getElementById('outputContainer');

    let html = `
        <div class="fade-in">
            <h3 class="text-2xl font-bold gradient-text mb-4 flex items-center gap-2">
                <i class="fas fa-clone"></i> Content Variations
            </h3>
            <div class="space-y-4">
    `;

    variations.forEach((v, index) => {
        const rendered = markdownToHTML(v.content || '');
        html += `
            <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                    <h4 class="font-bold text-slate-900">Variation ${v.variation || index + 1}</h4>
                    <span class="text-xs font-semibold text-slate-500">Preview</span>
                </div>
                <div class="prose prose-sm max-w-none text-slate-800 leading-relaxed">${rendered}</div>
                <button onclick="copyText(\`${(v.content || '').replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)" class="mt-3 inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm font-semibold">
                    <i class="fas fa-copy"></i> Copy full text
                </button>
            </div>
        `;
    });

    html += '</div></div>';
    container.innerHTML = html;
}

function displaySEOSuggestions(suggestions) {
    const container = document.getElementById('outputContainer');

    let html = `
        <div class="fade-in">
            <h3 class="text-2xl font-bold gradient-text mb-4 flex items-center gap-2">
                <i class="fas fa-search"></i> SEO Optimization
            </h3>
            <div class="space-y-4">
    `;

    if (suggestions.seo_score) {
        html += `
            <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-sm">
                <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-800">SEO Score</span>
                    <span class="text-2xl font-bold text-emerald-600">${suggestions.seo_score}/100</span>
                </div>
                <div class="w-full bg-slate-200 rounded-full h-2 mt-3 overflow-hidden">
                    <div class="bg-emerald-500 h-2 rounded-full" style="width: ${suggestions.seo_score}%"></div>
                </div>
            </div>
        `;
    }

    if (suggestions.meta_description) {
        html += `
            <div class="bg-sky-50 rounded-xl p-4 border border-sky-100">
                <span class="font-semibold text-slate-800">📝 Meta Description</span>
                <p class="text-slate-700 mt-2 text-sm leading-relaxed">${suggestions.meta_description}</p>
            </div>
        `;
    }

    if (suggestions.recommendations && suggestions.recommendations.length > 0) {
        html += `
            <div class="bg-amber-50 rounded-xl p-4 border border-amber-100">
                <span class="font-semibold text-slate-800">💡 Recommendations</span>
                <ul class="list-disc list-inside mt-2 space-y-1 text-slate-700 text-sm leading-relaxed">
                    ${suggestions.recommendations.slice(0, 5).map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    html += '</div></div>';
    container.innerHTML = html;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function markdownToHTML(markdown) {
    let html = markdown
        .replace(/^### (.*?)$/gm, '<h3 class="text-lg font-bold mt-4 mb-2">$1</h3>')
        .replace(/^## (.*?)$/gm, '<h2 class="text-xl font-bold mt-4 mb-2">$1</h2>')
        .replace(/^# (.*?)$/gm, '<h1 class="text-2xl font-bold mt-4 mb-2">$1</h1>')
        .replace(/\*\*(.*?)\*\*/gm, '<strong class="font-bold">$1</strong>')
        .replace(/\*(.*?)\*/gm, '<em class="italic">$1</em>')
        .replace(/^- (.*?)$/gm, '<li class="ml-4">$1</li>')
        .replace(/(<li.*?<\/li>)/s, '<ul class="list-disc my-2">$1</ul>')
        .replace(/\n\n/g, '</p><p class="my-4">')
        .replace(/^/gm, '<p class="my-2">');

    return html;
}

function copyToClipboard() {
    if (!currentContent) {
        showError('No content to copy');
        return;
    }
    
    navigator.clipboard.writeText(currentContent).then(() => {
        showSuccess('Copied to clipboard!');
    }).catch(() => {
        showError('Failed to copy');
    });
}

function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showSuccess('Copied!');
    }).catch(() => {
        showError('Failed to copy');
    });
}

function downloadAsText() {
    if (!currentContent) {
        showError('No content to download');
        return;
    }

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(currentContent));
    element.setAttribute('download', 'content.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    showSuccess('Content downloaded!');
}

function showLoading() {
    const container = document.getElementById('outputContainer');
    container.innerHTML = `
        <div class="flex flex-col items-center justify-center py-12">
            <div class="spinner mb-4"></div>
            <p class="text-gray-500 font-semibold">Generating your content...</p>
        </div>
    `;
}

function showError(message) {
    const toast = document.getElementById('errorToast');
    const messageEl = document.getElementById('errorMessage');
    messageEl.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 4000);
}

function showSuccess(message) {
    const toast = document.getElementById('successToast');
    const messageEl = document.getElementById('successMessage');
    messageEl.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 4000);
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Content Writing Assistant loaded!');
    console.log('Make sure backend is running at http://localhost:5000');
});