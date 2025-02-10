#! /bin/bash
# shellcheck disable=SC2046
ask() {
    local prompt default reply
    if [[ ${2:-} = 'Y' ]]; then
        prompt='Y/n'; default='Y';
    elif [[ ${2:-} = 'N' ]]; then
        prompt='y/N'; default='N';
    else
        prompt='y/n'; default='';
    fi

    while true; do
        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read -r reply </dev/tty

        # Default?
        if [[ -z $reply ]]; then
            reply=$default
        fi

        # Check if the reply is valid
        case "$reply" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac
    done
}


export HLO_PROD=false
export $(grep -v '^#' .env-dev | xargs -d '\n')
ask "nuke static? [$HLO_STATIC_ROOT]" "N" && {
  rm -r "$HLO_STATIC_ROOT";
  mkdir "$HLO_STATIC_ROOT";
  ./manage.py collectstatic --no-input;
}
ask "nuke media? [$HLO_MEDIA_ROOT]" "N" && {
  rm -r "$HLO_MEDIA_ROOT";
  mkdir "$HLO_MEDIA_ROOT";
}
ask "nuke db? [$HLO_SQLITE3_FILE]" "N" && {
  export HLO_PROD=false;
  rm -f "$HLO_SQLITE3_FILE";
  ./manage.py migrate;
  # We do not care about password, RemoteUserMiddleware
  DJANGO_SUPERUSER_PASSWORD=$(pwgen 50 1) \
    DJANGO_SUPERUSER_USERNAME=hildenae@gmail.com \
    DJANGO_SUPERUSER_EMAIL=hildenae@gmail.com \
    ./manage.py createsuperuser --noinput;
}
ask "start runserver?" "N" && ./manage.py runserver
