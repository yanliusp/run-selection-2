pyenv install 2.7.10
pyenv local 2.7.10 # this should run in the root directory of the repository

export WORKON_HOME=~/Envs
# check if folder exits
mkdir -p $WORKON_HOME
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

# is it necessary to point to this python version if pyenv global is set to the same one? Yes? It should matter for modules installed with pip.
mkvirtualenv srs -p /home/stefan/.pyenv/versions/2.7.10/bin/python
#otherwise
# mkvirtualenv srs
workon srs

export PROJECT_HOME=~/run-selection/run_selection-upgrade
cd $PROJECT_HOME

pip install -r requirements
