# VPN_Service

VPN_Service is a Django web application that allows users to browse external websites through a proxy, with the ability to track the number of transitions between pages and the amount of data sent and received.

# Getting Started
These instructions will help you set up and run the project locally. Before you begin, make sure you have Docker installed on your machine.

Prerequisites
Docker

# Installing
1.Clone the repository:
git clone https://github.com/RomanYefremov/VPN_Service.git
cd VPN_Service

2.Build the Docker image:
docker build -t vpn-service .

3.Run the Docker container:
docker run -p 8000:8000 vpn-service

4.Access the application in your browser:
http://localhost:8000/
http://0.0.0.0:8000/

# instructions for use: 
on the main page, click register, after you create your account, 
go to create a site, there you need to give a name to your site and give a link to it, 
for example https://ru.wikipedia.org/wiki/
after which, in your account, click on connect, and according to the name you gave, connect

# Contributing
If you'd like to contribute, please follow these steps:

1.Fork the repository on GitHub.
2.Create a new branch for your feature/fix.
3.Make your changes and commit them with descriptive commit messages.
4.Push your changes to your fork.
5.Open a pull request to the main branch of the original repository.
