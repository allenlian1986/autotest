# autotest
a simple frameworks for web test

pip install pytest-selenium
pip install pytest-rerunfailures
pip install pytest-variables
pip install pytest-html

py.test -q sample.py --rerun 2 --driver Remote --host XXXX --port 4444 --variables capabilities.json --html=a.html
