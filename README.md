# Apyllon
Apyllon is a shared music player, hosted on a local machine. Each logged in client user is able to: 
* upload local files to the server or to provide links, pointing to a song on Youtube.
* create playlists
* control the player

## Getting Started
Clone the repository and navigate into it
```
git clone https://github.com/Biskit1943/Apyllon.git && cd Apyllon
```
Start with Docker
``` docker-compose up ```
* Open Browser and navigate to localhost:80 to test the frontend
* Open Browser on localhost:8080/apidocs to test the backend

For the initial login to the frontend, use the username: "admin" and the generated password, 
printed in the docker-compose console. As soon as you logged in for the first time, 
it is **highly recommended** to change the admin password.

### Prerequisites

Docker
```
sudo pacman -S docker
sudo apt-get install docker
```

Docker Compose
```
sudo pacman -S docker-compose
sudo apt-get install docker-compose
```


### Installing

Clone the repository and navigate into it
```
git clone https://github.com/Biskit1943/Apyllon.git && cd Apyllon
```
Start with Docker
``` docker-compose up ```
And you're ready to go

## Built With

* [Flask](http://flask.pocoo.org/) - The python server used
* [Flasgger](https://github.com/rochacbruno/flasgger) - For building swagger documentation
* [Angular](https://angular.io/docs) - The web framework used for the frontend
* [vlc](https://wiki.videolan.org/PythonBinding) - Music player
* [youtube-dl](https://github.com/rg3/youtube-dl/blob/master/README.md#readme) - Library for downloading songs from youtube

## Authors

* **Maximilian Konter** - [Biskit1943](https://github.com/Biskit1943)
* **Michael Schwab** - [Schwub](https://github.com/Schwub)
* **Tim Köhler** - [TimKoehler](https://github.com/TimKoehler)

See also the list of [contributors](https://github.com/Biskit1943/Apyllon/contributors) who participated in this project.
