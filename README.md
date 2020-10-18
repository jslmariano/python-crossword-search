# Python Crossword Search

Docker running Python.

## Overview

1. [Install prerequisites](#install-prerequisites)

    Before installing project make sure the following prerequisites have been met.

2. [Clone the project](#clone-the-project)

    We’ll download the code from its repository on GitHub.

3. [Run the application](#run-the-application)

    By this point we’ll have all the project pieces in place.

___

## Install prerequisites

To run the docker commands without using **sudo** you must add the **docker** group to **your-user**:

```
sudo usermod -aG docker your-user
```

For now, this project has been mainly created for Unix `(Linux/MacOS)`. Perhaps it could work on Windows.

All requisites should be available for your distribution. The most important are :

* [Git](https://git-scm.com/downloads)
* [Docker](https://docs.docker.com/engine/installation/)
* [Docker Compose](https://docs.docker.com/compose/install/)

Check if `docker-compose` is already installed by entering the following command :

```sh
which docker-compose
```

Check Docker Compose compatibility :

* [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)

On Ubuntu and Debian these are available in the meta-package build-essential. On other distributions, you may need to install the GNU C++ compiler separately.

```sh
sudo apt install build-essential
```

### Images to use

* [Python Slim](https://hub.docker.com/_/python/)

___

## Clone the project

To install [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git), download it and install following the instructions :

```sh
git clone https://github.com/jslmariano/python-crossword-search.git
```

Go to the project directory :

```sh
cd python-crossword-search
```

### Project tree

```sh
.
├── result.sh
├── README.md
├── docker_compose
│   └── app
│       ├── Dockerfile
│       └── .env
├── docker-compose.yml
└── web
    ├── htmlconv
    ├── outputs
    │   |── lostDuck.out
    │   |── puzzle1.out
    │   |── puzzle_far_inputs.out
    │   |── puzzle_has_blank_each_inputs.out
    │   ├── sample.out
    │   └── suits.out
    └── puzzles  <------- PLEASE PUT PUZZLE FILES HERE
    │   |── lostDuck.pzl
    │   |── puzzle1.pzl
    │   |── puzzle_far_inputs.pzl
    │   |── puzzle_has_blank_each_inputs.pzl
    │   ├── sample.pzl
    │   └── suits.pzl
    ├── puzzle.py
    ├── test.py
    ├── WordSearch.py
    └── requirements.txt
```

___

## Run the application

1. Start the application :

    ```sh
    docker-compose up -d --build
    ```

    **Please wait this might take a several minutes...**

    ```sh
    docker-compose logs -f # Follow log output
    ```

2. After the build check the python version :

    ```
    docker-compose exec -T app python --version
    ```

3. Run the word search with argument of puzzle file name :

    **Make sure your puzzle files exists in puzzles directory**
    
    ```sh
    python-crossword-search/web/puzzles/*.pzl
    ```
    **Run within the docker container**
    
    ```sh
    docker-compose exec -T app python WordSearch.py puzzle1.pzl
    ```

4. Run Tests with code coverage :

    **Run the test within the docker container**
    
    ```sh
    docker-compose exec -T app python test.py
    ```
    
    **Run the test cli with code coverage**
    
    ```sh
    docker-compose exec -T app coverage run test.py
    docker-compose exec -T app coverage report
    docker-compose exec -T app coverage html
    ```

    **After tests is complete, code coverage is located in**

    ```sh
    python-crossword-search/web/htmlconv/*
    ```

5. Stop and clear services

    ```sh
    docker-compose down -v
    ```

