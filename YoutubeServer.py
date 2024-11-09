import pika

class YouTubeServer:
    youtuber_names = set()
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user_requests')
        self.channel.queue_declare(queue='youtuber_requests')
        self.channel.queue_declare(queue='notifications')
        self.subscriptions = {}

    def consume_user_requests(self, ch, method, properties, body):
        username, action, youtuber_name = body.decode().split()
        if action == 's':
            self.subscribe_user(username, youtuber_name)
        elif action == 'u':
            self.unsubscribe_user(username, youtuber_name)
        else:
            print(f"{username} logged in")

    def consume_youtuber_requests(self, ch, method, properties, body):
        youtuber_name, video_name = body.decode().split(maxsplit=1)
        self.upload_video(youtuber_name, video_name)
        self.youtuber_names.add(youtuber_name)

    def notify_users(self, youtuber_name, video_name):
        if youtuber_name in self.subscriptions:
            for username in self.subscriptions[youtuber_name]:
                self.channel.basic_publish(exchange='', routing_key=f"{username}_queue", body=f"{youtuber_name} uploaded {video_name}")
                print(f"Notification sent to {username}: {youtuber_name} uploaded {video_name}")

    def subscribe_user(self, username, youtuber_name):
        if youtuber_name not in self.youtuber_names:
            print(f"{youtuber_name} does not exist")
        else:                        
            if youtuber_name not in self.subscriptions:
                self.subscriptions[youtuber_name] = set()
            self.subscriptions[youtuber_name].add(username)
            print(f"{username} subscribed to {youtuber_name}")

    def unsubscribe_user(self, username, youtuber_name):
        if youtuber_name in self.subscriptions and username in self.subscriptions[youtuber_name]:
            self.subscriptions[youtuber_name].remove(username)
            print(f"{username} unsubscribed to {youtuber_name}")

    def upload_video(self, youtuber_name, video_name):
        print(f"{youtuber_name} uploaded {video_name}")
        self.notify_users(youtuber_name, video_name)

    def run_server(self):
        self.channel.basic_consume(queue='user_requests', on_message_callback=self.consume_user_requests, auto_ack=True)
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=self.consume_youtuber_requests, auto_ack=True)
        print("Server is running...")
        self.channel.start_consuming()

if __name__ == "__main__":
    server = YouTubeServer()
    server.run_server()
