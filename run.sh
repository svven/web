mkdir -p ~/svven/logs
export GUNC_ACCESS_LOG=~/svven/logs/guncacc.log
export GUNC_LOG=~/svven/logs/gunc.log

cd sources
gunicorn --access-logfile $GUNC_ACCESS_LOG --log-file $GUNC_LOG --log-level debug run:app -b 0.0.0.0:8000 &
