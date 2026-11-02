from app.extensions import db
from app.models import Notification


class NotificationService:

    @staticmethod
    def notify(title, message, user_id=None, category='order', icon='🔔'):
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            icon=icon
        )
        db.session.add(notif)
        db.session.commit()
        return notif
