import pika
import sys

class User:
    def __init__(self, username):
        self.username = username
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.28.134.134'))
        self.channel = self.connection.channel()
        self.queue_name = f"{username}_queue"
        self.channel.queue_declare(queue=self.queue_name)
        self.channel.queue_declare(queue='notifications')

    def perform_action(self, action, youtuber=None):
        if action == 'login':
            print(f"{self.username} logged in")
        elif action in ['subscribe', 'unsubscribe']:
            self.update_subscription(action, youtuber)
        else:
            print("Invalid action")

    def update_subscription(self, action, youtuber):
        self.channel.basic_publish(exchange='', routing_key='user_requests', body=f"{self.username} {action[0]} {youtuber}")
        print(f"{self.username} {action}d to {youtuber}")

    def receive_notifications(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(f"Waiting for notifications for {self.username}...")
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(body.decode())

if __name__ == "__main__":
    username = sys.argv[1]
    user = User(username)

    if len(sys.argv) == 2:
        user.perform_action('login')
    elif len(sys.argv) == 4:
        action = sys.argv[2]
        youtuber = sys.argv[3]
        user.perform_action(action, youtuber)
        if action == 'subscribe':
            user.receive_notifications()
    
    user.receive_notifications()
