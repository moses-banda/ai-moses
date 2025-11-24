"""
AI Moses Voice Agent - Main Flask Application
Handles incoming Twilio calls and manages AI responses
"""

# MUST load env variables FIRST before any other imports
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from datetime import datetime

from .twilio_handler import handle_incoming_call
from .voice_agent import VoiceAgent
from .database import Database
from .status_manager import StatusManager

# Initialize Flask app
app = Flask(__name__)

# Initialize database
db = Database()

# Initialize managers
status_manager = StatusManager()
voice_agent = VoiceAgent()


# ═══════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/incoming-call', methods=['POST'])
def incoming_call():
    """Handle incoming Twilio calls"""
    try:
        phone_number = request.form.get('From')
        call_sid = request.form.get('CallSid')
        
        # Get caller profile
        caller = db.get_caller_profile(phone_number)
        
        # Get current status
        current_status = db.get_current_status()
        
        # Generate AI response
        ai_response = voice_agent.generate_response(
            caller_name=caller.get('name'),
            caller_relationship=caller.get('relationship'),
            caller_tone=caller.get('tone'),
            status=current_status.get('activity')
        )
        
        # Log the call
        db.log_call(
            phone_number=phone_number,
            call_sid=call_sid,
            incoming_text="Incoming call",
            ai_response=ai_response
        )
        
        # Handle the call and return TwiML
        return handle_incoming_call(request, ai_response)
    
    except Exception as e:
        print(f"Error handling incoming call: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    }), 200


@app.route('/caller-profile/<phone_number>', methods=['GET'])
def get_caller_profile(phone_number):
    """Get caller profile by phone number"""
    try:
        profile = db.get_caller_profile(phone_number)
        return jsonify(profile), 200
    except Exception as e:
        print(f"Error getting caller profile: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/add-contact', methods=['POST'])
def add_contact():
    """Add a new contact"""
    try:
        data = request.get_json()
        
        success = db.add_caller_profile(
            phone_number=data.get('phone_number'),
            name=data.get('name'),
            relationship=data.get('relationship'),
            tone=data.get('tone'),
            topics=data.get('topics')
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f"Contact {data.get('name')} added successfully"
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to add contact'
            }), 400
    
    except Exception as e:
        print(f"Error adding contact: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/update-status', methods=['POST'])
def update_status():
    """Update your current activity status"""
    try:
        data = request.get_json()
        activity = data.get('activity', 'Busy')
        
        db.update_status(activity)
        
        return jsonify({
            'status': 'success',
            'activity': activity,
            'updated_at': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/current-status', methods=['GET'])
def get_current_status():
    """Get your current activity status"""
    try:
        status = db.get_current_status()
        return jsonify(status), 200
    except Exception as e:
        print(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/call-history/<phone_number>', methods=['GET'])
def get_call_history(phone_number):
    """Get call history for a contact"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db.get_call_history(phone_number, limit=limit)
        
        return jsonify({
            'phone_number': phone_number,
            'call_count': len(history),
            'calls': history
        }), 200
    
    except Exception as e:
        print(f"Error getting call history: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/all-contacts', methods=['GET'])
def get_all_contacts():
    """Get all contacts in database"""
    try:
        contacts = db.get_all_contacts()
        return jsonify({
            'contact_count': len(contacts),
            'contacts': contacts
        }), 200
    
    except Exception as e:
        print(f"Error getting all contacts: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/voice-recording', methods=['POST'])
def add_voice_recording():
    """Add a voice recording to database"""
    try:
        data = request.get_json()
        
        success = db.add_voice_recording(
            phone_number=data.get('phone_number'),
            call_sid=data.get('call_sid'),
            file_path=data.get('file_path'),
            duration=data.get('duration'),
            transcription=data.get('transcription')
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Voice recording saved'
            }), 201
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save recording'
            }), 400
    
    except Exception as e:
        print(f"Error adding voice recording: {e}")
        return jsonify({'error': str(e)}), 500


# ═══════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


# ═══════════════════════════════════════════════════════════════════════════
# APP STARTUP
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("🚀 AI Moses Voice Agent Starting...")
    print("📱 Listening on http://localhost:5000")
    print("📋 Using SQLite database: ai_moses.db")
    print("\nEndpoints ready:")
    print("  ✅ /health")
    print("  ✅ /incoming-call")
    print("  ✅ /caller-profile/<phone>")
    print("  ✅ /add-contact")
    print("  ✅ /update-status")
    print("  ✅ /current-status")
    print("  ✅ /call-history/<phone>")
    print("  ✅ /all-contacts")
    print("  ✅ /voice-recording")
    print("\n🔗 Next: Configure Twilio webhook to http://localhost:5000/incoming-call")
    print("   (Use ngrok for testing: ngrok http 5000)\n")
    
    app.run(
        host='localhost',
        port=5000,
        debug=True,
        use_reloader=True
    )