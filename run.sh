mkdir -p ~/logs
export GUNC_ACCESS_LOG=~/logs/guncacc.log
export GUNC_LOG=~/logs/gunc.log

cd sources
gunicorn --access-logfile $GUNC_ACCESS_LOG --log-file $GUNC_LOG --log-level debug run:app -b 0.0.0.0:8000 &
