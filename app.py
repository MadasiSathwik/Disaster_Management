#As A senior Software Developer, I have Disaster in My area So i want to develop a Disaster Management System to help people in need. The system will have the following features:
#1. User Registration and Login: Users can create an account and log in to access the system.
#2. Disaster Reporting: Users can report disasters in their area, including details such as location, type of disaster, and severity.
#3. Resource Management: The system will allow users to request and offer resources such as food, water, shelter, and medical supplies.
#4. Emergency Alerts: The system will send emergency alerts to users in the affected area, providing information on the disaster and safety instructions.
#5.Volunteer Coordination: The system will facilitate the coordination of volunteers who want to help in disaster relief efforts.
#6. Data Analytics: The system will analyze the reported disasters and resource requests to identify patterns and trends, helping authorities to better prepare for future disasters.
#7. Communication Platform: The system will provide a communication platform for users to connect with each other, share information, and coordinate efforts during a disaster.
#8. Mobile App: The system will have a mobile app version to allow users to access the system on the go and receive real-time updates during a disaster.
#9. Integration with Government Agencies: The system will integrate with government agencies and emergency services to provide accurate and timely information to users and facilitate coordination during disaster response efforts.
#10. Multilingual Support: The system will support multiple languages to ensure accessibility for users from different linguistic backgrounds.
#11. User Feedback and Improvement: The system will have a feedback mechanism to allow users to provide suggestions and report issues, enabling continuous improvement of the system.
#12. Data Security and Privacy: The system will implement robust security measures to protect user data and ensure privacy, especially during sensitive situations like disasters.
#13. Offline Functionality: The system will have offline functionality to allow users to access critical information and report disasters even when they do not have internet connectivity, ensuring that help can be requested and provided in areas with limited network access.
#14. Real-time Location Tracking: The system will utilize GPS technology to track the location of users and resources in real-time, allowing for efficient coordination and response during disasters.
#15. AI-Powered Disaster Prediction: The system will leverage artificial intelligence to analyze historical data and predict potential disasters, enabling authorities and users to take proactive measures to mitigate the impact of future disasters.
#16. Social Media Integration: The system will integrate with social media platforms to allow users to share information about disasters and coordinate relief efforts, increasing awareness and engagement during disaster situations.
#17. Community Forums: The system will include community forums where users can discuss disaster-related topics, share experiences, and provide support to each other during and after disasters.
#18. Resource Allocation Optimization: The system will use algorithms to optimize the allocation of resources based on the severity of the disaster and the needs of the affected population, ensuring that resources are distributed efficiently and effectively.
#19. Disaster Recovery Planning: The system will provide tools and resources to help users create disaster recovery plans, including checklists, templates, and guidelines to ensure that individuals and communities are prepared for potential disasters.
#20. Collaboration with NGOs and Relief Organizations: The system will collaborate with non-governmental organizations (NGOs) and relief organizations to facilitate the coordination of disaster response efforts and ensure that aid reaches those in need in a timely manner.
#21. Training and Education: The system will offer training materials and educational resources to help users understand disaster preparedness, response, and recovery, empowering them to take informed actions during disasters.
from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from extensions import db

# import models so that SQLAlchemy registers them
from models import Camp, Victim


def create_app():
    """Application factory for Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize extensions
    db.init_app(app)
    # TODO: initialize migrate, login manager, etc.

    with app.app_context():
        db.create_all()  # create tables if not exist

    # register blueprints
    from routes.auth_routes import auth_bp
    from routes.camp_routes import camp_bp
    from routes.victim_routes import victim_bp
    from routes.resource_routes import resource_bp
    from routes.report_routes import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(camp_bp, url_prefix='/camps')
    app.register_blueprint(victim_bp, url_prefix='/victims')
    app.register_blueprint(resource_bp, url_prefix='/resources')
    app.register_blueprint(report_bp, url_prefix='/reports')

    # error handlers
    @app.errorhandler(404)
    def not_found(e):
        flash('Page not found', 'warning')
        return redirect(url_for('report.dashboard'))

    @app.errorhandler(500)
    def server_error(e):
        flash('Internal server error', 'danger')
        return redirect(url_for('report.dashboard'))

    @app.route('/')
    def index():
        return redirect(url_for('report.dashboard'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# TODO: Add CLI commands for migrations and other utilities
# TODO: Add authentication blueprint and login logic
# TODO: Add Docker support
# TODO: Add unit tests
# TODO: Add REST API endpoints
