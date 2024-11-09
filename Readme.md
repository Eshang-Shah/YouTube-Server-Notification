
# YouTube Notification System

This project implements a simplified version of a YouTube application using RabbitMQ. It consists of three components: Youtuber, User, and YouTubeServer.

## Requirements

- Python 3.x
- RabbitMQ

## Setup

1. Install RabbitMQ. You can download it from [here](https://www.rabbitmq.com/download.html) and follow the installation instructions for your operating system.

2. Install the required Python libraries by running:
   ```
   pip install pika
   ```

3. Clone or download this repository.

## Running the Program

### 1. YouTube Server (YouTubeServer.py)

The YouTube server manages the communication between YouTubers and Users. It consumes messages from Users and YouTubers and stores them as data.

To run the YouTube server, execute the following command:
```
python YouTubeServer.py
```

### 2. Youtuber (Youtuber.py)

The Youtuber service allows YouTubers to publish videos on the YouTube server. It takes two command-line arguments: the YouTuber's name and the video they want to publish.

To publish a video as a Youtuber, run the following command:
```
python Youtuber.py <Youtuber Name> <Video Name>
```
Replace `<Youtuber Name>` with the name of the YouTuber (without spaces) and `<Video Name>` with the name of the video.

### 3. User (User.py)

The User service allows users to subscribe or unsubscribe to YouTubers and receive real-time notifications when a YouTuber they subscribe to uploads a new video. It takes one or three command-line arguments:
- The first argument is the name of the user.
- The second argument (optional) is either `s` to subscribe or `u` to unsubscribe.
- The third argument (optional) is the name of the YouTuber.

To log in as a user, run the following command:
```
python User.py <Username>
```
Replace `<Username>` with your name.

To subscribe or unsubscribe to a YouTuber, include the action (`s` or `u`) and the Youtuber's name as arguments:
```
python User.py <Username> <subscribe/unsubscribe> <Youtuber Name>
```

## Examples

- Log in, subscribe to a YouTuber, and receive notifications:
  ```
  python User.py username subscribe TomScott
  ```

- Log in, unsubscribe to a YouTuber, and receive notifications:
  ```
  python User.py username unsubscribe TomScott
  ```

- Log in and receive notifications:
  ```
  python User.py username
  ```

## Notes

- Make sure RabbitMQ is running before executing the scripts.
- You can customize the names of YouTubers, videos, and users according to your preferences.
```
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
