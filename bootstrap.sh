if [[ ! -e env ]]
then
    virtualenv -p `which python3` env
fi
if [[ ! $VIRTUAL_ENV ]]
then
    source env/bin/activate
fi
pip install -r dev-requirements.txt
