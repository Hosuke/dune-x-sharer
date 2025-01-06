from flask import Flask, request, jsonify, render_template
import os
import glob
from dune_sharer import DuneSharer

app = Flask(__name__)

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
SCREENSHOTS_DIR = os.path.join(STATIC_DIR, 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def cleanup_screenshots():
    """Clean up screenshot files"""
    try:
        # Delete all files in screenshots directory
        files = glob.glob(os.path.join(SCREENSHOTS_DIR, '*'))
        for f in files:
            try:
                os.remove(f)
            except Exception as e:
                app.logger.error(f"Error deleting file {f}: {str(e)}")
    except Exception as e:
        app.logger.error(f"Error cleaning up screenshots: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/share', methods=['POST'])
def share_dashboard():
    """Share a Dune Analytics dashboard"""
    try:
        # Clean up old screenshots
        cleanup_screenshots()
        
        # Get dashboard URL
        dashboard_url = request.form.get('dashboard_url')
        if not dashboard_url:
            return jsonify({'status': 'error', 'message': 'No dashboard URL provided'}), 400
        
        # Validate URL format
        if not dashboard_url.startswith('https://dune.com/'):
            return jsonify({'status': 'error', 'message': 'Invalid Dune Analytics URL'}), 400
        
        # Create DuneSharer instance and set screenshots directory
        sharer = DuneSharer(screenshots_dir=SCREENSHOTS_DIR)
        
        try:
            # Download and process dashboard
            screenshots = sharer.download_dune_dashboard(dashboard_url)
            
            if not screenshots:
                return jsonify({
                    'status': 'error',
                    'message': 'No charts or lists found in the dashboard'
                }), 400
            
            # Share on Twitter/X
            sharer.share_on_twitter(dashboard_url, screenshots)
            
            return jsonify({
                'status': 'success',
                'message': f'Successfully captured and shared {len(screenshots)} items',
                'screenshots': screenshots
            })
            
        except Exception as e:
            # Clean up screenshots on error
            cleanup_screenshots()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        # Clean up screenshots on error
        cleanup_screenshots()
        return jsonify({
            'status': 'error',
            'message': 'Internal server error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
