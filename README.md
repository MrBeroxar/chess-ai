# Chess AI

Basic chess ai that uses minimax to search for the best move to make.
Given that it's written in python, the depth is very shallow
(currently max depth is 3).

## Getting started

Set up the project locally.

### Prerequisites

You will need `python3` and `git`. I would recommend `python3.10` but others should work
too.

### Install

The following instructions are for linux. If you don't know how to apply them for your OS
(i.e. windows or mac), consider prompting ChatGPT to translate them to your OS.

```
git clone https://github.com/PraxTube/chess-ai.git
cd chess-ai
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

if everything went well, you should be able to run the project with

```
python src/chess_ai/main.py
```

## Contributing

How you can add your changes to this repo.

### Set up

In order to contribute to this repo, you will need to set up and SSH key for you github
account. You can follow these steps
[here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).
Note that you will want to change your `git remote origin` in your `chess-ai` folder. If
you don't know how to do this, then you can simply run
`git clone git@github.com:PraxTube/chess-ai.git` and then follow the steps above to set it
up.

### Adding a Pull Request

In order to make changes you will need to work on your own [branch](https://git-scm.com/docs/git-branch).
Once you created your local branch, you can [push it to github](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository).
When every task is completed, you can [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
This will get reviewed and after potentially having to fix some issues, your branch will get merged in the master branch.

### Conventions

We are using [black](https://github.com/psf/black) and [flake8](https://github.com/PyCQA/flake8)
to format our python code. You can run the following commands when you are in you venv

```
black .
flake8 .
```

The first one will automatically format you code in-place. If you prefer to see
if it would change anything, you can use the flag `--check`.

### CI

This repo uses [github actions](https://docs.github.com/en/actions)
to automatically run specific tests, see [here](https://github.com/PraxTube/chess-ai/actions).
These tests will check the following:

- Run unit tests
- Check with black
- Lint with flake8

if any of these fail, then you will not be able to merge your PR into master.
You should check if your commit passed the tests.

Note that your branch will **only** be tested if you have an open **pull request** into master.

## Milestone II - Basic AI

The deadline for this is the **18th Mai**.

- [x] Alpha-beta search
- [x] ~~Sophisticated~~ Better evaluation function
- [x] Unit tests for legal moves
- [x] ~~Unit tests for chess engine~~
- [x] Benchmarks that test different depths
