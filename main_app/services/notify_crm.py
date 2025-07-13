import requests
import json
from typing import Dict, Any, Optional
from flask import current_app
import logging

class CRMNotificationService:
    """Service for sending notifications to the CRM microservice"""
    
    def __init__(self, base_url: Optional[str] = None, auth_token: Optional[str] = None):
        """
        Initialize the CRM notification service
        
        Args:
            base_url (str, optional): Base URL of the CRM microservice
            auth_token (str, optional): Bearer token for authentication
        """
        self.base_url = base_url or current_app.config.get('CRM_BASE_URL', 'http://localhost:5001')
        self.auth_token = auth_token or current_app.config.get('CRM_AUTH_TOKEN', 'your-static-bearer-token-here')
        self.logger = logging.getLogger(__name__)
    
    def send_booking_notification(self, 
                                 booking_id: int,
                                 user_id: int,
                                 session_id: int,
                                 action: str,
                                 additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a booking notification to the CRM service
        
        Args:
            booking_id (int): ID of the booking
            user_id (int): ID of the user
            session_id (int): ID of the session
            action (str): Action performed (e.g., 'created', 'cancelled', 'reactivated')
            additional_data (dict, optional): Additional data to include
            
        Returns:
            dict: Response from the CRM service
        """
        try:
            # Get user and session details from database
            from main_app.models.user import User
            from main_app.models.session import Session
            
            user = User.query.get(user_id)
            session = Session.query.get(session_id)
            
            if not user or not session:
                raise Exception("User or session not found")
            
            # Prepare the notification payload in the format expected by CRM service
            payload = {
                'booking_id': booking_id,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                },
                'event': {
                    'id': session.parent_event.id,
                    'title': session.parent_event.title,
                    'start_date': session.parent_event.start_date.isoformat()
                },
                'facilitator_id': session.facilitator_id
            }
            
            # Add additional data if provided
            if additional_data:
                payload['additional_data'] = additional_data
            
            # Prepare headers with authentication
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.auth_token}'
            }
            
            # Make the POST request to CRM service
            url = f"{self.base_url}/notify"
            self.logger.info(f"Sending booking notification to {url}: {action} for booking {booking_id}")
            
            response = requests.post(
                url=url,
                json=payload,
                headers=headers,
                timeout=10  # 10 second timeout
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse and return response
            result = response.json()
            self.logger.info(f"Booking notification sent successfully: {result}")
            return result
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout while sending booking notification to CRM service"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error while sending booking notification to CRM service"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code} while sending booking notification: {e.response.text}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from CRM service: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error sending booking notification: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def send_notification(self, 
                         notification_type: str,
                         user_id: int,
                         message: str,
                         additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a general notification to the CRM microservice
        
        Args:
            notification_type (str): Type of notification (e.g., 'booking_created', 'booking_cancelled')
            user_id (int): ID of the user related to the notification
            message (str): Notification message
            additional_data (dict, optional): Additional data to include in the notification
            
        Returns:
            dict: Response from the CRM service
            
        Raises:
            Exception: If the request fails
        """
        try:
            # Prepare the notification payload
            payload = {
                'notification_type': notification_type,
                'user_id': user_id,
                'message': message,
                'timestamp': None  # Will be set by CRM service
            }
            
            # Add additional data if provided
            if additional_data:
                payload['additional_data'] = additional_data
            
            # Prepare headers with authentication
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.auth_token}'
            }
            
            # Make the POST request to CRM service
            url = f"{self.base_url}/notify"
            self.logger.info(f"Sending notification to {url}: {notification_type} for user {user_id}")
            
            response = requests.post(
                url=url,
                json=payload,
                headers=headers,
                timeout=10  # 10 second timeout
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse and return response
            result = response.json()
            self.logger.info(f"Notification sent successfully: {result}")
            return result
            
        except requests.exceptions.Timeout:
            error_msg = f"Timeout while sending notification to CRM service"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error while sending notification to CRM service"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code} while sending notification: {e.response.text}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from CRM service: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"Unexpected error sending notification: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
    
    def send_event_notification(self,
                               event_id: int,
                               user_id: int,
                               action: str,
                               additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send an event-related notification to the CRM service
        
        Args:
            event_id (int): ID of the event
            user_id (int): ID of the user
            action (str): Action performed (e.g., 'created', 'updated', 'deleted')
            additional_data (dict, optional): Additional data to include
            
        Returns:
            dict: Response from the CRM service
        """
        notification_type = f"event_{action}"
        message = f"Event {event_id} {action}"
        
        # Prepare additional data
        notification_data = {
            'event_id': event_id,
            'action': action
        }
        
        if additional_data:
            notification_data.update(additional_data)
        
        return self.send_notification(
            notification_type=notification_type,
            user_id=user_id,
            message=message,
            additional_data=notification_data
        )
    
    def test_connection(self) -> bool:
        """
        Test the connection to the CRM microservice
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"CRM service connection test failed: {str(e)}")
            return False
