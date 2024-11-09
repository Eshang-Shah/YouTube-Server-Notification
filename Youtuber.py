import pika
import sys

class Youtuber:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.28.134.134'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='youtuber_requests')
        self.channel.queue_declare(queue='notifications')

    def publish_video(self, youtuber, video_name):
        self.channel.basic_publish(exchange='', routing_key='youtuber_requests', body=f"{youtuber} {video_name}")
        print("SUCCESS")
        self.send_notification(youtuber, video_name)

    def send_notification(self, youtuber, video_name):
        self.channel.basic_publish(exchange='', routing_key='notifications', body=f"{youtuber} uploaded {video_name}")

if __name__ == "__main__":
    youtuber_name = sys.argv[1]
    video_name = ' '.join(sys.argv[2:])
    youtuber = Youtuber()
    youtuber.publish_video(youtuber_name, video_name)
