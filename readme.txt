The app flow should be like this:

0 - The program is triggered by crontab
1 - It checks if there's a need for a backup (max time between backups elapsed)
    1.1 - If yes: checks that the server is online
        1.1.1 - if yes: performs the backup
            1.1.1.1 - If there are any errors show them
            1.1.1.2 - Log the backup output in a hidden folder (.albt)
        1.1.2 - if not: shows a message similar to "server is offline, please turn it on a try again"
            1.1.2.1 - if the user says OK: go back to 1.1
            1.1.2.2 - if the user says Cancel: the program is terminated
    1.2 - if not: it quits


Notes:

rsync --archive --compress --delete --dry-run --progress --partial /home/.ecryptfs/michele/.Private michele@silverbox:/mnt/3tbdrive/backup/silverone_michele/


