# voice-synthesizer
Simple text-to-speach service based on Django and RHVoice

### Installation

Check that you have installed RHVoice. To install you can simply clone this repository on your PC and run this command to install dependencies: 
```sh
voice-synthesizer$ pip3 install -r 
```
Then you can deploy the project on the server or run it as a normal Django project.

voice-synthesizer is very easy to install and deploy in a Docker container: 
```sh
$ docker push bm0computer/voice-synthesizer
```
This will create the voice-synthesizer image and pull in the necessary dependencies.
After starting the container service will be available at ```127.0.0.1:8000```

For more detailed settings, see Dockerfile. 
You only need to forward some folders from a container on your machine.
