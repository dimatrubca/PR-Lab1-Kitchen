# Kitchen WebServer
This is a component for the Restauram Simulation project.<br>
Dinning Hall component: <a href="https://github.com/dimatrubca/PR-Lab1-Kitchen">link</a>

## Usage
Create bridge network: ```docker network create kitchen-nt```<br>
Create kitchen-image: ```docker build -t kitchen-image .```<br>
Create and run the container: ```docker run --net kitchen-nt -p 5000:5000 --name kitchen-container kitchen-image```
