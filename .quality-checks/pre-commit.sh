git stash -q --keep-index
./.quality-checks/check-all.sh
RESULT=$?
git stash pop -q
[ $RESULT -ne 0 ] && echo "Verification failed. Rerun with '--no-verify' to force this commit." && exit 1
exit 0
