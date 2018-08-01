Run Selection tools
===================

Contributors: Gersende, Lisa, Eric, Tanner, Stefan

## Requirements
  - Python 2.7.10
  - Python modules: [requests](http://docs.python-requests.org), [psycopg2](http://initd.org/psycopg/docs/)

#### Install only the python packages

`$ pip install -r requirements`

#### Install using a virtual environment

###### Requirements
  - [pyenv](https://github.com/pyenv/pyenv)
    - sample install
  ```sh
  $ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  $ [sudo] echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  $ [sudo] echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  $ [sudo] echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  $ exec $SHELL
  ```

  - Python modules: [virtualenv](https://virtualenv.pypa.io), [vritualenvwrapper](https://virtualenvwrapper.readthedocs.io)
    - sample install
  ```sh
  $ [sudo] pip install virtualenv
  $ [sudo] pip install virtualenvwrapper
  ```

###### Configure
`$ . env_install.sh`.

###### Load
`$ . env_load.sh`.
