The app flow should be like this:

0 - The program is triggered by crontab
1 - It checks if there's a need for a backup (max time between backups elapsed)
    1.1 - If yes: checks that the server is online
        1.1.1 - if yes: performs the backup
            1.1.1.1 - If there are any errors it shows them
            1.1.1.2 - Logs the backup output in a file in a hidden folder (.albt)
        1.1.2 - if not: shows a message similar to "server is offline, please turn it on a try again"
            1.1.2.1 - if the user says OK: go back to 1.1
            1.1.2.2 - if the user says Cancel: the program is terminated
    1.2 - if not: it quits




Rsync command:

rsync --archive --compress --delete --dry-run --progress --partial /home/.ecryptfs/michele/.Private michele@silverbox:/mnt/3tbdrive/backup/silverone_michele/


Configuration example:
{
    "backup_server" :"silverbox",
    "home_dir" :"/home/michele/.albt",
    "log_dir" :"/home/michele/.albt",
    "max_time_bween_backups" :"1234556",
    "log_level" :"debug",
    "rsync_cmd" : "rsync --archive --compress --delete --dry-run --progress --partial /home/.ecryptfs/michele/.Private michele@silverbox:/mnt/3tbdrive/backup/silverone_michele/"
}


Configuration notes

max_time_bween_backups is expressed in seconds (e.g. 2 days will be 2*24*60*60)

available log_levels:
    - critical
    - error
    - warn
    - warning
    - info
    - debug
    - notset


